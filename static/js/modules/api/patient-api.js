export async function submitDiagnosis(conversationId, user_diagnosis){
  const res = await fetch('/api/submit-diagnosis',{
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({conversation_id:conversationId, user_diagnosis})
  });
  if(!res.ok) throw new Error('Diagnosis submit failed');
  return res.json();
}

export async function generatePatientCase(caseData){
  const res = await fetch('/api/generate-patient-case',{
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify(caseData)
  });
  if(!res.ok) throw new Error('Generate patient case failed');
  return res.json();
}

export async function getCurrentPatientDetails(){
  const res = await fetch('/api/current-patient-details');
  if(!res.ok) throw new Error('Patient details failed');
  return res.json();
} 