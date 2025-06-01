// copy-vad.js  (run by the postinstall script)
const { mkdirSync, cpSync } = require('fs');
const path = require('path');

const out = path.join(__dirname, 'static', 'vad-model');
mkdirSync(out, { recursive: true });

const VAD   = path.dirname(require.resolve('@ricky0123/vad-web/package.json'));
const ORT   = path.dirname(require.resolve('onnxruntime-web/package.json'));

// 1) worklet + onnx
cpSync(path.join(VAD, 'dist', 'vad.worklet.bundle.min.js'), out + '/vad.worklet.bundle.min.js');
cpSync(path.join(VAD, 'dist', 'silero_vad_legacy.onnx'   ), out + '/silero_vad_legacy.onnx');
cpSync(path.join(VAD, 'dist', 'silero_vad_v5.onnx'       ), out + '/silero_vad_v5.onnx');

// 2) wasm files
['ort-wasm.wasm', 'ort-wasm-simd.wasm', 'ort-wasm-simd-threaded.wasm'].forEach(f =>
  cpSync(path.join(ORT, 'dist', f), out + '/' + f)
);

console.log('[VAD COPY] assets -> static/vad-model ✓');
