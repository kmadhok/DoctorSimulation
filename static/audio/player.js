// static/js/audio/player.js
import { state } from '../core/state.js';
import { base64ToArrayBuffer } from '../utils/helpers.js';

export async function playBase64Audio(base64) {
  if (!base64) return;

  // Ensure we have a shared AudioContext.
  if (!state.audioContext) {
    state.audioContext = new (window.AudioContext || window.webkitAudioContext)();
  }

  // Abort any current playback.
  if (state.currentAudioSource) {
    state.currentAudioSource.stop();
    state.currentAudioSource = null;
  }

  const audioBuffer = await state.audioContext.decodeAudioData(
    base64ToArrayBuffer(base64)
  );

  const src = state.audioContext.createBufferSource();
  src.buffer = audioBuffer;
  src.connect(state.audioContext.destination);
  src.start(0);
  state.currentAudioSource = src;

  src.onended = () => { state.currentAudioSource = null; };
}
