// copy-vad.js  (repo root)
import {join} from 'node:path';
import {fileURLToPath} from 'node:url';
import cpy from 'cpy';

const root = join(fileURLToPath(import.meta.url), '..');        // repo root
const VAD = join(root, 'node_modules/@ricky0123/vad-web/dist');
const ORT = join(root, 'node_modules/onnxruntime-web/dist');
const DEST = join(root, 'static', 'vad-model');

(async () => {
  await cpy(
    [
      `${VAD}/vad.worklet.bundle.min.js`,
      `${VAD}/*.onnx`,
      `${ORT}/*.wasm`
    ],
    DEST,
    {verbose: true}
  );
  console.log('[VAD COPY] Completed ✓');
})();
