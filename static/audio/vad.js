// static/js/audio/vad.js
import { state } from '../core/state.js';

/**
 * Create and start a Silero VAD instance.
 * Returns a stop() cleanup fn.
 */
export async function startVAD({
  basePath = '/static/vad-model/',
  positiveSpeechThreshold = 0.8,
  negativeSpeechThreshold = 0.5,
  preSpeechPadFrames = 8,
  minSpeechFrames = 3,
  redemptionFrames = 10,
  onSpeechStart = () => {},
  onSpeechEnd   = () => {},
  onVADMisfire  = () => {}
} = {}) {

  const vadInstance = await vad.MicVAD.new({
    baseAssetPath:  basePath,
    onnxWASMBasePath: basePath,
    positiveSpeechThreshold,
    negativeSpeechThreshold,
    preSpeechPadFrames,
    minSpeechFrames,
    redemptionFrames,
    onSpeechStart,
    onSpeechEnd,
    onVADMisfire
  });

  await vadInstance.start();
  return () => vadInstance.destroy();
}
