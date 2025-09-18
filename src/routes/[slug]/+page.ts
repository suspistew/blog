// src/routes/[slug]/+page.ts   // <- passe en +page.ts pour du full statique
import type { PageLoad } from './$types';

const metaMods = import.meta.glob('/content/*/meta.json', { eager: true });
const htmlMods = import.meta.glob('/content/*/gaming-post.html', { eager: true, query: '?raw', import: 'default' });


const metas: Record<string, any> = {};
const htmls: Record<string, string> = {};
for (const p in metaMods) {
    const slug = p.split('/').slice(-2, -1)[0];
    // @ts-ignore
    metas[slug] = (metaMods[p] as any).default ?? metaMods[p];
}
for (const p in htmlMods) {
    const slug = p.split('/').slice(-2, -1)[0];
    // @ts-ignore
    htmls[slug] = htmlMods[p] as string;
}

export const prerender = true;
// indispensable: liste explicite des pages à générer
export const entries = () => Object.keys(metas).map((s) => ({ slug: s }));

export const load: PageLoad = async ({ params }) => {
    const slug = params.slug;
    const log = metas[slug];
    const logContent = htmls[slug];

    const strip = (s?: string) => (s ?? '').replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
    const abs = (p?: string) => (p && /^https?:\/\//.test(p)) ? p : `https://daronquest.fr${p ?? ''}`;

    return {
        log: log ?? { title: slug.replace(/-/g,' '), description: 'Article indisponible', miniature: '/miniatures/default.jpg', url: slug, date: '2025-01-01', tags: [] },
        logContent: logContent ?? '<p>Contenu indisponible.</p>',
        meta: {
            title: `Daron Quest - ${(log?.title) ?? slug}`,
            description: strip(log?.description),
            image: abs(log?.miniature ?? '/miniatures/default.jpg'),
            url: `https://daronquest.fr/${slug}`,
            type: 'article'
        }
    };
};
