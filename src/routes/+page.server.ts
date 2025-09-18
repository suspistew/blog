import type { PageServerLoad } from './$types';
import fs from 'fs/promises';
import path from 'path';

export const load: PageServerLoad = async () => {
    const p = path.join(process.cwd(), 'content', 'global_meta.json');
    const raw = await fs.readFile(p, 'utf-8');
    const logs = JSON.parse(raw);
    return { logs };
};
