import { store } from '../state/store.js';
import { updateStatus } from '../ui/status-manager.js';

export function ensureAudioContext(){
  if(!store.audioContext){
    const Ctx = window.AudioContext || window.webkitAudioContext;
    if(!Ctx){ console.error('WebAudio not supported'); return null; }
    store.set('audioContext', new Ctx());
  }
  return store.audioContext;
}

export async function playAudio(base64){
  try{
    if(!base64) return;
    const ctx = ensureAudioContext();
    if(!ctx) return;
    if(ctx.state==='suspended') await ctx.resume();

    const byteArray = Uint8Array.from(atob(base64), c=>c.charCodeAt(0));
    const buffer = await ctx.decodeAudioData(byteArray.buffer);
    const src = ctx.createBufferSource();
    src.buffer = buffer;
    src.connect(ctx.destination);
    src.start();
  }catch(err){
    console.error('playAudio error', err);
    updateStatus('Error playing audio');
  }
} 