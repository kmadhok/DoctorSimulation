// copy-vad.js  (root of repo – runs during `npm install` on Heroku)

import { promises as fs } from 'node:fs';
import path from 'node:path';

const dest = path.join(process.cwd(), 'static', 'vad-model');

// List everything ONNX-runtime & VAD will ever request
const sources = [
  // worklet bundle
  'node_modules/@ricky0123/vad-web/dist/vad.worklet.bundle.min.js',

  // top-level MicVAD runtime
  'node_modules/@ricky0123/vad-web/dist/bundle.min.js',

  // both ONNX model variants
  'node_modules/@ricky0123/vad-web/dist/silero_vad_legacy.onnx',
  'node_modules/@ricky0123/vad-web/dist/silero_vad_v5.onnx',

  // wasm binaries **and** the .mjs loader stubs
  ...(
    await fs.readdir('node_modules/onnxruntime-web/dist')
  )
    .filter(f => f.startsWith('ort-wasm'))          // picks *.wasm and *.mjs
    .map(f => `node_modules/onnxruntime-web/dist/${f}`)
];

// make dest dir once
await fs.mkdir(dest, { recursive: true });

// copy one by one
await Promise.all(
  sources.map(async src => {
    const fileName = path.basename(src);
    await fs.copyFile(src, path.join(dest, fileName));
    console.log(`[VAD COPY] ${fileName} → ${dest}`);
  })
);
