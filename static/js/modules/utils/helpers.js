export const $ = (selector, scope = document) => scope.querySelector(selector);
export const $$ = (selector, scope = document) => [...scope.querySelectorAll(selector)];

export class EventBus {
  #listeners = {};
  on(event, fn) {
    (this.#listeners[event] ||= []).push(fn);
  }
  emit(event, payload) {
    (this.#listeners[event] || []).forEach(fn => fn(payload));
  }
} 