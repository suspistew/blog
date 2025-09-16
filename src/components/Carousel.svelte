<script lang="ts">
    import { onMount } from "svelte";

    export let images: string[] = [];
    export let tile = 250;
    export let gap = 16;

    let current = 0;
    let lightboxIndex: number | null = null;

    let viewportEl: HTMLDivElement | null = null;
    let viewportWidth = 0;
    let ro: ResizeObserver | null = null;

    const clamp = (n: number, a: number, b: number) => Math.min(b, Math.max(a, n));
    const measure = () => { if (viewportEl) viewportWidth = viewportEl.clientWidth; };

    onMount(() => {
        measure();
        ro = new ResizeObserver(measure);
        if (viewportEl) ro.observe(viewportEl);
        return () => ro?.disconnect();
    });

    // # de slides visibles selon la largeur et l'espacement
    $: visible = Math.max(1, Math.floor((viewportWidth + gap) / (tile + gap)));

    // Dernier index autorisé selon le visible courant
    $: maxIndex = Math.max(0, images.length - visible);

    // Re-clamp si images/visible changent ou après resize
    $: current = clamp(current, 0, maxIndex);

    // Décalage horizontal
    $: offset = -(current * (tile + gap));

    const prev = () => current = clamp(current - 1, 0, maxIndex);
    const next = () => current = clamp(current + 1, 0, maxIndex);

    const openLightbox = (i: number) => lightboxIndex = i;
    const closeLightbox = () => lightboxIndex = null;
    const prevLightbox = () => lightboxIndex = (lightboxIndex! - 1 + images.length) % images.length;
    const nextLightbox = () => lightboxIndex = (lightboxIndex! + 1) % images.length;
</script>

<style>
    .carousel {
        position: relative;
        overflow: hidden;
        width: 100%;
        max-width: 1024px;
        padding: 0 3rem;
        box-sizing: border-box;
        background: #ebddcd;
        border-radius: 0.5rem;
    }

    .viewport { overflow: hidden; }

    .track {
        display: flex;
        gap: var(--gap);
        transition: transform 0.35s ease;
        will-change: transform;
    }

    .slide {
        flex: 0 0 auto;
        width: var(--tile);
        height: 200px;
        display: grid;
        place-items: center;
        cursor: pointer;
        border-radius: 8px;
    }

    .slide img {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
        display: block;
        border-radius: 6px;
    }

    .slide img:hover { opacity: 0.8; cursor: pointer; }
    .slide img:active { opacity: 0.9; }

    .nav {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        background: #d5c1ac;
        border: 0;
        color: #fff;
        font-size: 1.4rem;
        cursor: pointer;
        padding: 0.25rem 0.6rem 0.25rem 0.5rem;
        user-select: none;
        border-radius: 0.2rem;
    }
    .nav:hover { background: #bba18c; }
    .nav:active { background: #a48875; }
    .nav:disabled { opacity: 0.4; cursor: default; }

    .prev { left: 8px; padding: 0.25rem 0.65rem 0.25rem 0.5rem; }
    .next { right: 8px; padding: 0.25rem 0.6rem 0.25rem 0.65rem; }

    .lightbox {
        position: fixed; inset: 0; background: rgba(0,0,0,0.85);
        display: flex; align-items: center; justify-content: center; z-index: 19999;
    }
    .lightbox img { max-width: 90%; max-height: 90%; border-radius: 6px; }
    .lightbox .close, .lightbox .prev, .lightbox .next {
        position: absolute; top: 50%; transform: translateY(-50%);
        background: #d5c1ac; border: 0; color: #fff; font-size: 2rem;
        cursor: pointer; padding: 0.4rem 0.8rem; border-radius: 0.5rem;
    }
    .lightbox .close:hover, .lightbox .prev:hover, .lightbox .next:hover { background:#bba18c; }
    .lightbox .close:active, .lightbox .prev:active, .lightbox .next:active { background:#a48875; }
    .lightbox .close { top: 20px; right: 20px; transform: none; }
    .lightbox .prev { left: 20px; }
    .lightbox .next { right: 20px; }

    .bigimg{ border: 1px solid #42362c; }
    .tinyimg{ border: 1px solid #a48875; }
</style>

<div class="carousel" style={`--tile:${tile}px; --gap:${gap}px`}>
    <div class="viewport" bind:this={viewportEl}>
        <div class="track" style={`transform: translateX(${offset}px);`}>
            {#each images as src, i}
                <div class="slide" on:click={() => openLightbox(i)} aria-label="ouvrir l’image">
                    <img src={src} alt="image du carrousel" class="tinyimg" />
                </div>
            {/each}
        </div>
    </div>

    {#if images.length > 1}
        <button class="nav prev" on:click={prev} disabled={current === 0} aria-label="précédent">&#10094;</button>
        <button class="nav next" on:click={next} disabled={current === maxIndex} aria-label="suivant">&#10095;</button>
    {/if}
</div>

{#if lightboxIndex !== null}
    <div class="lightbox" on:click={closeLightbox}>
        <button class="close" on:click|stopPropagation={closeLightbox}>✕</button>
        <button class="prev" on:click|stopPropagation={prevLightbox}>&#10094;</button>
        <img src={images[lightboxIndex]} alt="image agrandie" on:click|stopPropagation class="bigimg" />
        <button class="next" on:click|stopPropagation={nextLightbox}>&#10095;</button>
    </div>
{/if}
