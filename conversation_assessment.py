from explore_conversations import specific_conversation
from typing import Dict, List
from groq import Groq                     # <-- direct import
import json, os
from dotenv import load_dotenv

load_dotenv()

GROQ_MODEL = "llama3-8b-8192"

def call_groq_raw(system_prompt: str, user_prompt: str) -> str:
    """Minimal wrapper that sends exactly the text we want."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "🚫 GROQ_API_KEY not set."

    client = Groq(api_key=api_key)
    resp = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt}
        ]
    )
    return resp.choices[0].message.content

def analyze_conversation(patient_data: Dict, messages: List) -> Dict:
    """
    Analyze a conversation and return insights.
    """
    if not messages:
        return {"error": "No conversation data available"}

    analysis = {
        "total_messages": len(messages),
        "user_messages": 0,
        "assistant_messages": 0,
        "average_message_length": 0,
        "patient_details": patient_data,
        "conversation_summary": []
    }

    # Count message types and calculate average length
    total_length = 0
    for msg in messages:
        if msg[0] == "user":  # msg[0] is role
            analysis["user_messages"] += 1
        elif msg[0] == "assistant":
            analysis["assistant_messages"] += 1
        total_length += len(msg[1])  # msg[1] is content
        
        # Add to conversation summary
        analysis["conversation_summary"].append({
            "role": msg[0],
            "timestamp": msg[2],
            "content_preview": msg[1][:100] + "..." if len(msg[1]) > 100 else msg[1]
        })

    # Calculate average message length
    if analysis["total_messages"] > 0:
        analysis["average_message_length"] = total_length / analysis["total_messages"]

    return analysis

def main():
    patient_data, messages = specific_conversation()
    if not messages:
        print("No conversation found.")
        return

    # --- PROMPT: use a fixed placeholder instead of asking the user ---
    analyst_prompt = "analyze the conversation between the doctor and the patient. Grade the doctor on how empathetic they are. Give a score out of 10. Grade the doctor on how well the asked questions. Give a score out of 10"   # placeholder prompt
    # ------------------------------------------------------------------

    # Quick stats first (optional)
    # stats = analyze_conversation(patient_data, messages)
    # print("\n=== Quick Stats ===")
    # print(f"- Total messages: {stats['total_messages']}")
    # print(f"- User messages: {stats['user_messages']}")
    # print(f"- Assistant messages: {stats['assistant_messages']}")
    # print(f"- Avg. message length: {stats['average_message_length']:.2f} chars")

    # Build transcript & optional patient context
    transcript = "\n".join(f"{m[0].capitalize()}: {m[1]}" for m in messages)
    redacted_details = {
        k: v for k, v in patient_data.get("patient_details", {}).items()
        if k != "illness"
    } if patient_data else {}

    user_prompt = (
        f"{analyst_prompt}\n\n"
        f"Patient context:\n{json.dumps(redacted_details, indent=2)}\n\n"
        f"Conversation transcript:\n{transcript}"
    )

    system_prompt = (
        "You are a medical conversation analyst. "
        "Answer the user's request based only on the transcript provided."
    )

    print("\n=== Groq LLM Analysis ===")
    print(call_groq_raw(system_prompt, user_prompt))

if __name__ == "__main__":
    main()