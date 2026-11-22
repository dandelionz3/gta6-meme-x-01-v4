// gta6-meme-x-01-v4 — variant 4 entry (Node 22, standard library only).
// The program copies POST.json from the repo root into /output/POST.json,
// where the house gate reads the X post address. The post itself is the
// entry — the house reads the meme and the caption straight from X.

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(outDir, { recursive: true });
const post = readFileSync(join(botDir, 'POST.json'), 'utf8');
writeFileSync(join(outDir, 'POST.json'), post);
