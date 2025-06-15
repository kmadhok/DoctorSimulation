// static/js/core/state.js
// One place to share things every slice might need.
export const state = {
    audioContext: null,          // created lazily
    currentAudioSource: null     // for interrupting playback
  };
  