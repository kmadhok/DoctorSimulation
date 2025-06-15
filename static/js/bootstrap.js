// PHASE-01 bootstrap entry – minimal wiring just to prove modules load
import { store } from './modules/state/store.js';
import { updateStatus } from './modules/ui/status-manager.js';

// Example usage: set status to Ready when page loads
updateStatus('Loading modules…');
window.addEventListener('DOMContentLoaded', () => {
  updateStatus('Ready');
}); 