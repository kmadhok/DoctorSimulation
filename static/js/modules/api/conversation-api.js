export async function newConversation(){
  const res = await fetch('/api/conversations/new',{method:'POST'});
  if(!res.ok) throw new Error('Failed to create conversation');
  return res.json();
}

export async function listConversations(){
  const res = await fetch('/api/conversations');
  if(!res.ok) throw new Error('Failed to list conversations');
  return res.json();
}

export async function loadConversation(id){
  const res = await fetch(`/api/conversations/${id}/load`,{method:'POST'});
  if(!res.ok) throw new Error('Failed to load conversation');
  return res.json();
}

export async function deleteConversation(id){
  const res = await fetch(`/api/conversations/${id}`,{method:'DELETE'});
  if(!res.ok) throw new Error('Failed to delete conversation');
  return res.json();
}

export async function updateVoice(conversationId, voiceId){
  const res = await fetch('/api/update-voice',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({voice_id:voiceId, conversation_id:conversationId})
  });
  if(!res.ok) throw new Error('Failed to update voice');
  return res.json();
} 