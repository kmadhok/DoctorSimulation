import { updateStatus } from '../ui/status-manager.js';

// For Phase-04 we keep legacy implementation in main.js; this wrapper just
// forwards the call via a CustomEvent so behaviour stays unchanged.
export async function processAudio(blob){
  return new Promise((resolve)=>{
    const evt = new CustomEvent('module:processAudio', { detail:{ blob, resolve } });
    window.dispatchEvent(evt);
  });
}

// --- Dev helper: if legacy handler not installed, warn ---
if(!window._moduleProcessAudioHook){
  window._moduleProcessAudioHook = true;
  window.addEventListener('module:processAudio', e=>{
    if(typeof window.processAudio === 'function'){
      window.processAudio(e.detail.blob).then(e.detail.resolve);
    }else{
      console.warn('Legacy processAudio not found; no-op');
      updateStatus('Error processing audio');
      e.detail.resolve();
    }
  });
} 