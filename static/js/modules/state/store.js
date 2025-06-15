import { EventBus } from '../../utils/helpers.js';
import { DEFAULT_VOICE, MAX_DIAGNOSIS_ATTEMPTS } from '../../utils/constants.js';

class Store extends EventBus {
  currentConversationId = null;
  currentVoiceId        = DEFAULT_VOICE;
  currentSimulation     = null;
  diagnosisPanelVisible = false;
  diagnosisAttemptCount = 0;
  maxDiagnosisAttempts  = MAX_DIAGNOSIS_ATTEMPTS;
  audioContext          = null;

  set(key, value) {
    const old = this[key];
    this[key] = value;
    this.emit(`state:${key}`, { newValue: value, oldValue: old });
  }
}

export const store = new Store();

// Expose for debugging in dev only
if (window && window.location && window.location.hostname === 'localhost') {
  window.store = store;
} 