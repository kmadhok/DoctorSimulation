import { $ } from '../utils/helpers.js';

const convoContainer = $('#conversation');

export function addMessage(role, content){
  if(!convoContainer) return;
  const div = document.createElement('div');
  div.className = `message ${role}`;
  div.textContent = content;
  convoContainer.appendChild(div);
  convoContainer.scrollTop = convoContainer.scrollHeight;
}

export function clearMessages(){
  if(convoContainer) convoContainer.innerHTML = '';
} 