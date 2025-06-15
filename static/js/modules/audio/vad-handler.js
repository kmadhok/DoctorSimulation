import { updateStatus } from '../ui/status-manager.js';
import { processAudio } from './audio-processor.js';

function float32ToWav(float32, sampleRate = 16000) {
  const buffer = new ArrayBuffer(44 + float32.length * 2);
  const view   = new DataView(buffer);
  const write  = (o,s)=>[...s].forEach((c,i)=>view.setUint8(o+i,c.charCodeAt(0)));
  write(0,'RIFF'); view.setUint32(4,36+float32.length*2,true);
  write(8,'WAVE'); write(12,'fmt ');
  view.setUint32(16,16,true); view.setUint16(20,1,true); view.setUint16(22,1,true);
  view.setUint32(24,sampleRate,true); view.setUint32(28,sampleRate*2,true);
  view.setUint16(32,2,true); view.setUint16(34,16,true); write(36,'data');
  view.setUint32(40,float32.length*2,true);
  float32.forEach((s,i)=>view.setInt16(44+i*2,Math.max(-1,Math.min(1,s))*0x7FFF,true));
  return new Blob([view],{type:'audio/wav'});
}

export class VADHandler{
  #vad; #stop;
  async init(){
    if(this.#vad) return;
    updateStatus('Initializing voice detection…');
    this.#vad = await vad.MicVAD.new({
      baseAssetPath: '/static/vad-model/',
      positiveSpeechThreshold:0.8,
      negativeSpeechThreshold:0.5,
      preSpeechPadFrames:8,
      minSpeechFrames:3,
      redemptionFrames:10,
      onSpeechStart: ()=>updateStatus('Listening…'),
      onSpeechEnd : async (audio)=>{
        updateStatus('Processing…');
        try{
          const wav = float32ToWav(audio);
          await processAudio(wav);
          updateStatus('Ready');
        }catch(err){
          console.error('VAD speechEnd error', err);
          updateStatus('Error processing audio');
        }
      }
    });
    this.#stop = ()=> this.#vad.destroy();
  }
  async start(){ await this.init(); await this.#vad.start(); }
  stop(){ this.#stop?.(); }
} 