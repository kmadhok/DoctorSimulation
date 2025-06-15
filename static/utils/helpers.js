# static/js/utils/helpers.js  (new file)
export function float32ToWav(float32, sampleRate = 16000) {
  const buffer = new ArrayBuffer(44 + float32.length * 2);
  const view   = new DataView(buffer);

  const write = (o, s) => s.split('').forEach((c, i) => view.setUint8(o + i, c.charCodeAt(0)));

  write(0,  'RIFF');
  view.setUint32(4, 36 + float32.length * 2, true);
  write(8,  'WAVE');
  write(12, 'fmt ');
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, 1, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * 2, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, 16, true);
  write(36, 'data');
  view.setUint32(40, float32.length * 2, true);

  for (let i = 0; i < float32.length; i++) {
    const s = Math.max(-1, Math.min(1, float32[i]));
    view.setInt16(44 + i * 2, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
  }
  return new Blob([view], { type: 'audio/wav' });
}
