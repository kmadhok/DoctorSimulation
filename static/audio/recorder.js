// static/js/audio/recorder.js
import { state } from '../core/state.js';
import { float32ToWav } from '../utils/helpers.js';
import { startVAD } from './vad.js';

let stopVAD = null;

/**
 * Attach Auto-Listen button behaviour.
 * @param {HTMLElement} btn  The #autoListenBtn element
 * @param {Function}    onAudioReady  cb(blob) when audio ready for backend
 * @param {Function}    setStatus(text)   UI status helper
 */
export function wireAutoListen(btn, onAudioReady, setStatus) {
  if (!btn) return;

  btn.addEventListener('click', async (e) => {
    e.preventDefault();

    try {
      if (!stopVAD) {
        // Lazy-create AudioContext once.
        if (!state.audioContext) {
          state.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }

        // Quick permission probe.
        await navigator.mediaDevices.getUserMedia({ audio: true })
                                    .then(str => str.getTracks().forEach(t => t.stop()));

        setStatus('Initializing voice detection…');
        btn.classList.add('recording');

        stopVAD = await startVAD({
          onSpeechStart()  { setStatus('Listening…'); },
          onSpeechEnd     : async (float32) => {
            setStatus('Processing…');
            const wavBlob = float32ToWav(float32);
            await onAudioReady(wavBlob);
            setStatus('Ready');
          }
        });

      } else {
        stopVAD();                // clean up
        stopVAD = null;
        btn.classList.remove('recording');
        setStatus('Paused');
      }

    } catch (err) {
      console.error('Auto-Listen error', err);
      btn.classList.remove('recording');
      stopVAD = null;
      setStatus('Error initializing voice detection');
    }
  });
}
