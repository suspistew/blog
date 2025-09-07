<!-- src/lib/PageLoader.svelte -->
<script lang="ts">
    import {onMount} from "svelte";
    import {beforeNavigate} from "$app/navigation";

    let show = true;
    onMount(async () => {
        setTimeout(() => { show = false; }, 1000);
    });
    beforeNavigate((nav) => {
        if (nav.type === 'link' && nav.to?.url.pathname.endsWith('/..')) return; // adapte ton test
        show = true;
        setTimeout(() => { show = false; }, 1000);
    });
</script>

<style>
    .overlay {
        position: fixed; inset: 0; z-index: 2147483647;
        display: flex; align-items: center; justify-content: center;
        background: rgba(255,255,255,0.6);
        backdrop-filter: blur(2px);
    }
    .spinner {
        width: 36px; height: 36px; border-radius: 50%;
        border: 3px solid rgba(0,0,0,0.15);
        border-top-color: #111;
        animation: spin 0.8s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
</style>

{#if show}
    <div class="overlay" role="status" aria-busy="true" aria-label="Chargement">
        <div class="spinner"></div>
    </div>
{/if}
