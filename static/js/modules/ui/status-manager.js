/* Phase-03: full implementation */
import { $ } from '../utils/helpers.js';

const statusEl = $('#status');

function applyStatusClass(text){
  if(!statusEl) return;
  statusEl.classList.remove('recording','processing','error');
  if(/recording/i.test(text))   statusEl.classList.add('recording');
  if(/processing/i.test(text))  statusEl.classList.add('processing');
  if(/error/i.test(text))       statusEl.classList.add('error');
}

export function updateStatus(text){
  if(!statusEl){ console.warn('Status element not found'); return; }
  statusEl.textContent = text;
  applyStatusClass(text);
} 