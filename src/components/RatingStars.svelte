<script lang="ts">
    export let value = 0;
    export let max = 10;
    export let stars = 10;
    export let size = 24;

    const clamp = (n: number, a: number, b: number) => Math.min(b, Math.max(a, n));
    const uid = crypto?.randomUUID?.() ?? Math.random().toString(36).slice(2);

    $: step = max / stars;
    $: v = clamp(value, 0, max);
    $: fills = Array.from({ length: stars }, (_, i) => {
        const amt = (v - i * step) / step;
        return clamp(amt * 100, 0, 100);
    });
</script>

<style>
    .rating { display:inline-flex; gap:2px; line-height:0; }
    .empty { color: var(--star-empty, #d6d6d6); }
    .full  { color: var(--star-full,  #f5a623); }
    svg { width: var(--size); height: var(--size); display:block; }
    :host { --size:24px; }
</style>

<div class="rating" style={`--size:${size}px`} aria-label={`note ${v} sur ${max}`} title={`${value} / 10`}>
    {#each fills as pct, i}
        <svg viewBox="0 0 24 24" role="img" aria-hidden="true">
            <defs>
                <clipPath id={`clip-${uid}-${i}`}>
                    <rect x="0" y="0" width={`${pct}%`} height="100%"></rect>
                </clipPath>
            </defs>

            <path class="empty" fill="none" stroke="currentColor" stroke-width="1.5"
                  d="M12 3.6l2.7 5.46 6.03.88-4.37 4.26 1.03 6.01L12 17.77 6.61 20.21l1.03-6.01L3.27 9.94l6.03-.88L12 3.6z"/>
            <path class="full" fill="currentColor" clip-path={`url(#clip-${uid}-${i})`}
                  d="M12 3.6l2.7 5.46 6.03.88-4.37 4.26 1.03 6.01L12 17.77 6.61 20.21l1.03-6.01L3.27 9.94l6.03-.88L12 3.6z"/>
        </svg>
    {/each}
</div>
