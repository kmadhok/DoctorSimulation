from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from typing import Dict, List, Optional, Any
import json
import logging
import random
from datetime import datetime
from .persona_system import get_all_personas, get_persona_by_id
from .groq_integration import get_groq_response

logger = logging.getLogger(__name__)

class ConversationMemoryTool(BaseTool):
    """Tool for agents to access conversation context"""
    
    name: str = "conversation_memory"
    description: str = "Access to shared conversation history and context"
    
    def _run(self, query: str) -> str:
        """Get relevant conversation context"""
        # This will be set by the orchestrator when creating tools
        return "No conversation history available yet."

class DirectResponseTool(BaseTool):
    """Tool for agents to speak directly in conversation"""
    
    name: str = "speak"
    description: str = "Speak directly to the group conversation"
    
    def _run(self, message: str) -> str:
        """Agent speaks directly"""
        return f"DIRECT_RESPONSE: {message}"

class MultiAgentConversationOrchestrator:
    """Orchestrates multi-agent conversations using CrewAI"""
    
    def __init__(self):
        self.agents: Dict[str, Dict] = {}  # Store agent info with persona data
        self.crew: Optional[Crew] = None  # CrewAI crew object
        self.conversation_history: List[Dict] = []
        self.turn_order: List[str] = []
        self.current_turn_index: int = 0
        self.conversation_context: str = ""
        
    def create_agent_from_persona(self, persona_id: str, persona_data: Dict) -> Agent:
        """Create a CrewAI agent from persona data"""
        
        characteristics = persona_data.get('characteristics', {})
        
        # Create agent role and goal based on persona
        role = f"{persona_data['name']} - {persona_data['description']}"
        
        goal = f"""Participate in a group conversation as {persona_data['name']}.
        Debate mode: take a clear stance, be concise, and avoid questions.
        Maintain your personality: {', '.join(characteristics.get('personality_traits', []))}.
        Speaking style: {characteristics.get('speaking_style', 'natural conversation')}.
        Background: {characteristics.get('background', 'No specific background')}.
        Worldview: {characteristics.get('worldview', 'Open-minded perspective')}.

        Response patterns:
        {chr(10).join(['• ' + pattern for pattern in characteristics.get('response_patterns', [])])}
        """
        
        backstory = f"""You are {persona_data['name']}, participating in a group conversation.

        Your personality: {', '.join(characteristics.get('personality_traits', []))}
        Your background: {characteristics.get('background', 'You have a rich life experience')}
        Your worldview: {characteristics.get('worldview', 'You see the world with optimism')}

        In conversations, you:
        {chr(10).join(['• ' + pattern for pattern in characteristics.get('response_patterns', [])])}

        Speak naturally as yourself, not as an AI assistant. Engage authentically with others in the conversation.
        Keep responses under 2 sentences. Take a clear, assertive stance.
        Do NOT ask questions or request clarification unless safety-critical.
        No meta commentary.
        """
        
        # Tools for the agent
        tools = [
            ConversationMemoryTool(),
            DirectResponseTool()
        ]
        
        agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools,
            verbose=False,
            allow_delegation=False,
            max_execution_time=30
        )
        
        return agent
    
    def add_agent(self, persona_id: str) -> bool:
        """Add an agent to the conversation"""
        try:
            persona_data = get_persona_by_id(persona_id)
            if not persona_data:
                logger.error(f"Persona {persona_id} not found")
                return False
            
            agent = self.create_agent_from_persona(persona_id, persona_data)
            
            # Store both agent and persona data
            self.agents[persona_id] = {
                'agent': agent,
                'persona_data': persona_data
            }
            
            self.turn_order.append(persona_id)
            
            # Recreate crew with updated agents
            self._update_crew()
            
            logger.info(f"Added agent {persona_data['name']} to conversation")
            return True
            
        except Exception as e:
            logger.error(f"Error adding agent {persona_id}: {str(e)}")
            return False
    
    def _update_crew(self):
        """Update the CrewAI crew with current agents"""
        try:
            if self.agents:
                agent_list = [agent_info['agent'] for agent_info in self.agents.values()]
                self.crew = Crew(
                    agents=agent_list,
                    tasks=[],  # Tasks will be created dynamically for each conversation
                    verbose=False
                )
        except Exception as e:
            logger.error(f"Error updating crew: {str(e)}")
    
    def remove_agent(self, persona_id: str) -> bool:
        """Remove an agent from the conversation"""
        if persona_id in self.agents:
            del self.agents[persona_id]
            if persona_id in self.turn_order:
                self.turn_order.remove(persona_id)
            
            # Update crew
            self._update_crew()
            
            logger.info(f"Removed agent {persona_id} from conversation")
            return True
        return False
    
    def process_user_message(self, user_message: str, addressed_to: Optional[str] = None) -> List[Dict]:
        """
        Process user message and generate agent responses
        
        Args:
            user_message: The user's message
            addressed_to: Specific agent ID if message is directed to someone
            
        Returns:
            List of response messages with agent info
        """
        responses = []
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user", 
            "content": user_message,
            "speaker": "User",
            "timestamp": self._get_timestamp()
        })
        
        try:
            # --- 1. Direct addressing takes precedence over moderator logic ---
            if addressed_to and addressed_to in self.agents:
                response = self._get_agent_response_simple(addressed_to, user_message, is_direct=True)
                if response:
                    responses.append(response)
            else:
                # --- 2. Use LLM "floor-manager" to decide turn taking ---
                next_speakers = self._moderator_pick(user_message)

                # Fallback – if moderator fails, keep previous simple logic
                if not next_speakers:
                    next_speakers = self._select_responding_agents(user_message, max_responses=2)

                for agent_id in next_speakers:
                    if agent_id not in self.agents:
                        continue
                    response = self._get_agent_response_simple(agent_id, user_message)
                    if response:
                        responses.append(response)
                        self.conversation_history.append(response)
        except Exception as e:
            logger.error(f"Error processing user message: {str(e)}")
            responses.append({
                "role": "assistant",
                "content": "Sorry, there was an error processing that message.",
                "speaker": "System",
                "agent_id": "system",
                "voice_id": "Fritz-PlayAI"
            })
        
        return responses
    
    def _orchestrate_group_response_simple(self, user_message: str, max_responses: int = 2) -> List[Dict]:
        """Simplified orchestration using direct LLM calls"""
        responses = []
        
        # Select which agents should respond
        responding_agents = self._select_responding_agents(user_message, max_responses)
        
        for agent_id in responding_agents:
            response = self._get_agent_response_simple(agent_id, user_message, is_direct=False)
            if response:
                responses.append(response)
                # Add to conversation history immediately
                self.conversation_history.append(response)
        
        return responses
    
    def _get_agent_response_simple(self, agent_id: str, user_message: str, is_direct: bool = False) -> Optional[Dict]:
        """Get agent response using direct Groq integration"""
        
        if agent_id not in self.agents:
            return None
        
        try:
            persona_data = self.agents[agent_id]['persona_data']
            characteristics = persona_data.get('characteristics', {})
            
            # Create context-aware prompt for the agent
            context = self._get_recent_context(6)
            
            personality_desc = f"""You are {persona_data['name']}, {persona_data['description']}.

Your personality: {', '.join(characteristics.get('personality_traits', []))}
Your speaking style: {characteristics.get('speaking_style', 'natural conversation')}
Your background: {characteristics.get('background', 'diverse life experience')}
Your worldview: {characteristics.get('worldview', 'balanced perspective')}

In conversations, you:
{chr(10).join(['• ' + pattern for pattern in characteristics.get('response_patterns', [])])}

Debate mode:
- Make a clear claim first, then one supporting reason or example.
- Avoid questions and clarification prompts; do not ask the user anything.
- Keep it 1–2 sentences, direct, and confident.
- No meta commentary or disclaimers.
Do not mention that you are an AI. You are simply {persona_data['name']} participating in a conversation."""
            
            # Create the full prompt
            prompt = f"""Context - Recent conversation:
{context}

User just said: "{user_message}"

Respond as {persona_data['name']} would respond naturally in this conversation.
Follow the Debate mode strictly. Provide a decisive stance, not a question:"""
            
            # Get response from Groq
            response_text = get_groq_response(
                input_text=prompt,
                # Use default model from utils.groq_integration
                system_prompt=personality_desc
            )
            
            if response_text:
                response = {
                    "role": "assistant",
                    "content": response_text,
                    "speaker": persona_data['name'],
                    "agent_id": agent_id,
                    "voice_id": persona_data['voice_id'],
                    "timestamp": self._get_timestamp()
                }
                
                return response
            
        except Exception as e:
            logger.error(f"Error getting response from agent {agent_id}: {str(e)}")
        
        return None
    
    def _select_responding_agents(self, user_message: str, max_responses: int) -> List[str]:
        """Select which agents should respond to the message"""
        
        # Simple strategy: rotate through agents, but bias toward relevance
        available_agents = list(self.agents.keys())
        
        if len(available_agents) <= max_responses:
            return available_agents
        
        # For now, simple rotation with some randomness
        selected = []
        
        # Try to include the "next" agent in rotation
        if self.turn_order and len(self.conversation_history) > 1:
            next_agent = self.turn_order[self.current_turn_index % len(self.turn_order)]
            selected.append(next_agent)
            self.current_turn_index += 1
        
        # Add one more agent randomly
        remaining = [a for a in available_agents if a not in selected]
        if remaining and len(selected) < max_responses:
            selected.append(random.choice(remaining))
        
        return selected[:max_responses]
    
    def _get_recent_context(self, num_messages: int = 6) -> str:
        """Get recent conversation context"""
        if not self.conversation_history:
            return "This is the start of the conversation."
        
        recent = self.conversation_history[-num_messages:]
        context_lines = []
        
        for msg in recent:
            speaker = msg.get('speaker', msg.get('role', 'Unknown'))
            content = msg.get('content', '')
            context_lines.append(f"{speaker}: {content}")
        
        return "\n".join(context_lines)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        return datetime.now().isoformat()
    
    def get_conversation_summary(self) -> Dict:
        """Get summary of current conversation state"""
        # Get participant names
        participants = []
        for agent_id in self.agents.keys():
            try:
                persona_data = get_persona_by_id(agent_id)
                participants.append(persona_data['name'])
            except:
                participants.append(agent_id)
        
        # Get recent messages
        recent_messages = self.conversation_history[-5:] if len(self.conversation_history) > 5 else self.conversation_history
        
        return {
            "total_messages": len(self.conversation_history),
            "participants": participants,
            "recent_messages": recent_messages,
            "active_agents": [
                {
                    "id": agent_id,
                    "name": get_persona_by_id(agent_id)['name'],
                    "voice_id": get_persona_by_id(agent_id)['voice_id']
                }
                for agent_id in self.agents.keys()
            ],
            "message_count": len(self.conversation_history),
            "turn_order": self.turn_order
        }
    
    def clear_conversation(self):
        """Clear conversation history and reset state"""
        self.conversation_history = []
        self.turn_order = []
        self.current_turn_index = 0
        self.conversation_context = ""

    # --- Automatic turn when the user is silent ---
    def generate_auto_turn(self, max_responses: int = 2) -> List[Dict]:
        """Let the moderator decide who should speak next without new user input."""
        try:
            next_speakers = self._moderator_pick(user_message="", max_attempts=1)
            if not next_speakers:
                next_speakers = self._select_responding_agents("", max_responses=max_responses)

            responses: List[Dict] = []
            for agent_id in next_speakers:
                if agent_id not in self.agents:
                    continue
                resp = self._get_agent_response_simple(agent_id, "", is_direct=False)
                if resp:
                    responses.append(resp)
                    self.conversation_history.append(resp)
            return responses
        except Exception as e:
            logger.error(f"Error generating auto turn: {e}")
            return []

    # ------------------------------------------------------------------
    # Floor-manager helper
    # ------------------------------------------------------------------
    def _moderator_pick(self, user_message: str, max_attempts: int = 1) -> List[str]:
        """Use an LLM call to decide the ordered list of agents who should
        speak next. Returns a list of agent IDs. If the LLM output cannot be
        parsed, returns an empty list so that fallback heuristics can apply.
        """

        try:
            # Build a short description of participants for the prompt
            participants_desc = []
            for aid, ainfo in self.agents.items():
                pdata = ainfo["persona_data"]
                participants_desc.append(f"{aid} – {pdata['name']}, {pdata['description']}")

            participants_block = "\n".join(participants_desc) if participants_desc else "(none)"

            context = self._get_recent_context(8)

            system_prompt = (
                "You are the floor-manager of a group conversation. "
                "Choose **at most one** agent for next_speakers. "
                "Return JSON ONLY, no prose. The format:\n"
                "{\n  \"next_speakers\": [<agent_id>, ...] \n}\n"
                "Return an empty list if no agent should speak yet."
            )

            user_prompt = (
                f"Participants:\n{participants_block}\n\n"
                f"Recent conversation:\n{context}\n\n"
                f"User just said: \"{user_message}\"\n"
                f"Respond with JSON now."
            )

            raw = get_groq_response(
                input_text=user_prompt,
                # Use default model from utils.groq_integration
                history=[],
                system_prompt=system_prompt
            )

            # Expect a small JSON blob. Try to parse first {...} found.
            json_start = raw.find("{")
            json_end = raw.rfind("}")
            if json_start == -1 or json_end == -1:
                raise ValueError("No JSON object found in moderator response")

            data = json.loads(raw[json_start:json_end+1])
            speakers = data.get("next_speakers", [])
            logger.debug(f"--Moderator chose: {speakers}   raw: {raw[:120]!r}")
            # Ensure we return only valid agent IDs and respect turn order
            return [s for s in speakers if s in self.agents]

        except Exception as e:
            logger.warning(f"Moderator pick failed: {e}")
            return [] 
