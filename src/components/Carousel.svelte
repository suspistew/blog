<script lang="ts">
    export let images: string[] = [];
    export let tile = 250;
    export let gap = 16;

    let current = 0;
    let lightboxIndex: number | null = null;

    const clamp = (n: number, a: number, b: number) => Math.min(b, Math.max(a, n));
    const prev = () => current = clamp(current - 1, 0, images.length - 2);
    const next = () => current = clamp(current + 1, 0, images.length - 2);

    const openLightbox = (i: number) => lightboxIndex = i;
    const closeLightbox = () => lightboxIndex = null;
    const prevLightbox = () => lightboxIndex = (lightboxIndex! - 1 + images.length) % images.length;
    const nextLightbox = () => lightboxIndex = (lightboxIndex! + 1) % images.length;

    $: offset = -(current * (tile + gap));
</script>

<style>
    .carousel {
        position: relative;
        overflow: hidden;
        width: 100%;
        max-width: 850px;
        padding: 0 3rem 0rem 3rem;
        box-sizing: border-box;
        background: #fafafa;
        border-radius:0.2rem;
    }
    .viewport {
        overflow: hidden;
    }
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

    .slide img:hover {
        opacity: 0.8; cursor:pointer;
    }
    .slide img:active {
        opacity: 0.9;
    }
    .nav {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        background: rgba(0,0,0,0.4);
        border: 0;
        color: #fff;
        font-size: 1.4rem;
        cursor: pointer;
        padding: 0.25rem 0.6rem 0.25rem 0.5rem;
        user-select: none;
        border-radius: 0.2rem;
    }

    .nav:hover{
        background: rgba(0,0,0,0.6);
    }
    .nav:active{
        background: rgba(0,0,0,0.7);
    }
    .prev { left: 8px;
        padding: 0.25rem 0.65rem 0.25rem 0.5rem;}
    .next { right: 8px;
        padding: 0.25rem 0.6rem 0.25rem 0.65rem;}

    /* Lightbox */
    .lightbox {
        position: fixed; inset: 0;
        background: rgba(0,0,0,0.85);
        display: flex; align-items: center; justify-content: center;
        z-index: 9999;
    }
    .lightbox img { max-width: 90%; max-height: 90%; border-radius: 6px; }
    .lightbox .close, .lightbox .prev, .lightbox .next {
        position: absolute; top: 50%; transform: translateY(-50%);
        background: rgba(0,0,0,0.5); border: 0; color: #fff;
        font-size: 2rem; cursor: pointer; padding: 0.4rem 0.8rem; border-radius: 50%;
    }
    .lightbox .close { top: 20px; right: 20px; transform: none; }
    .lightbox .prev { left: 20px; }
    .lightbox .next { right: 20px; }
</style>

<div class="carousel" style={`--tile:${tile}px; --gap:${gap}px`}>
    <div class="viewport">
        <div class="track" style={`transform: translateX(${offset}px);`}>
            {#each images as src, i}
                <div class="slide" on:click={() => openLightbox(i)} aria-label="ouvrir l’image">
                    <img src={src} alt="image du carrousel" />
                </div>
            {/each}
        </div>
    </div>

    {#if images.length > 1}
        <button class="nav prev" on:click={prev} aria-label="précédent">&#10094;</button>
        <button class="nav next" on:click={next} aria-label="suivant">&#10095;</button>
    {/if}
</div>

{#if lightboxIndex !== null}
    <div class="lightbox" on:click={closeLightbox}>
        <button class="close" on:click|stopPropagation={closeLightbox}>✕</button>
        <button class="prev" on:click|stopPropagation={prevLightbox}>&#10094;</button>
        <img src={images[lightboxIndex]} alt="image agrandie" on:click|stopPropagation />
        <button class="next" on:click|stopPropagation={nextLightbox}>&#10095;</button>
    </div>
{/if}
