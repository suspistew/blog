<script>
    import RatingStars from "../../components/RatingStars.svelte";
    import Carousel from "../../components/Carousel.svelte";

    export let data;
    const { log, logContent, meta } = data;
    const mois = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"];
    const formatDate = d => { const [y,m,day]=d.split("-").map(Number); return `${day} ${mois[m-1]} ${y}`; };
</script>

<svelte:head>
    <title>{meta.title}</title>
    <meta name="description" content={meta.description} />
    <link rel="canonical" href={meta.url} />

    <meta property="og:type" content={meta.type} />
    <meta property="og:site_name" content="Daron Quest" />
    <meta property="og:title" content={meta.title} />
    <meta property="og:description" content={meta.description} />
    <meta property="og:image" content={meta.image} />
    <meta property="og:url" content={meta.url} />

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content={meta.title} />
    <meta name="twitter:description" content={meta.description} />
    <meta name="twitter:image" content={meta.image} />
    <meta property="og:image:width" content="480">
    <meta property="og:image:height" content="270">
</svelte:head>

<div class="home">
    <div style="width:100%;">
        <div class="log">
            <img src={log.full}/>
            <div class="log-fill">
                <div class="log-title">
                    {log.title}
                </div>
                <div class="log-title-separator">
                </div>
                <div class="log-date">
                    {#each log.tags as tag}
                        <a href={"/?tag=" + tag.replace(/\s+/g, '-').toLowerCase()}
                           class={"tag tag-clickable " + tag.replace(/\s+/g, '-').toLowerCase()}
                           on:click={selectTag(tag.replace(/\s+/g, '-').toLowerCase())}>{tag}</a>
                    {/each}
                    <div>
                        {formatDate(log.date)}
                    </div>
                </div>
                <div class="log-content">
                    {@html logContent}
                </div>
                {#if log.note}
                    <div class="log-note">
                        <h3>Note</h3>
                        <RatingStars value={log.note}/>
                    </div>
                {/if}
                {#if log.gallery && log.gallery.length > 0}
                    <div class="log-gallery">
                        <h3>Gallerie d'images</h3>
                        <Carousel images={log.gallery}/>
                    </div>
                {/if}

                <div class="goback">
                    <a href="/" class="buttonreturn">Revenir en arrière</a>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .goback {
        text-align: right;
        font-size: 0.9rem;
        margin-top: 1rem;
    }

    .title {
        font-weight: 500;
    }

    .home {
        height: 100%;
        width: 1024px;
        margin: auto;
        font-weight: 200;
        font-size: 16px;
        display: flex;
        flex-direction: row;
    }

    @media (max-width: 1024px) {
        .home {
            width: 95%;
            margin: auto;
        }
    }

    .log {
        margin-top: 1rem;
        display: flex;
        flex-direction: column;
        gap: 15px;
        background: #f3ebe5;
        border: 1px solid #555;
        border-radius: 0.4rem;
        font-weight: 400;
    }

    .log img {
        width: 100%;
        height: auto;
        border-top-right-radius: 0.3rem;
        border-top-left-radius: 0.3rem;
    }

    .log-fill {
        padding: 0 2rem 2rem 2rem;
        box-sizing: border-box;
    }

    .log-title {
        font-weight: 700;
        font-size: 32px;
        text-align: center;
        text-transform: capitalize;
        margin-bottom: 0.5rem;
    }

    .log-title-separator {
        width: 50%;
        margin: 0 auto 1.4rem auto;
        height: 1px;
        border-bottom: 1px solid #a48875;
    }

    .log-date {
        text-align: center;
        font-weight: 200;
        font-size: 14px;
    }

    .log-date div {
        margin-top: 8px;
        font-weight: 400;
    }

    .tag {
        border: 1px solid #444;
        display: inline-block;
        padding: 6px;
        border-radius: 4px;
        margin-bottom: 5px;
    }

    a {
        text-decoration: none;
    }

    .buttonreturn {
        background: #ebddcd;
        border: 1px solid #a48875;
        border-radius: 0.3rem;
        font-size: 0.8rem;
        font-family: "Inter", monospace;
        font-weight: 400;
        color: black;
        padding: 0.5rem;
    }

    .buttonreturn:hover {
        background: #d5c1ac;
        cursor: pointer;
    }

    .buttonreturn:active {
        background: #bba18c;
        cursor: pointer;
    }

</style>