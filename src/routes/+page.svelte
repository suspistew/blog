<script>

    import axios from "axios";
    import {onMount} from "svelte";
    import RatingStars from "../components/RatingStars.svelte";
    import Loader from "../components/Loader.svelte";
    import {afterNavigate} from "$app/navigation";

    let logs = [];
    let mainlog = [];
    let currentPageLogs = [];
    let currentPage = 0;
    let totalPages = 1;
    let pageSize = 6;
    let currentTagFilter = "";
    let totalElements = 0;
    let trigger;

    function initPageFromURL() {
        const params = new URLSearchParams(window.location.search);
        const p = parseInt(params.get("page"));
        const t = params.get("tag");
        if (!isNaN(p) && p >= 1) {
            currentPage = p - 1;
        } else {
            currentPage = 0;
        }
        if (t) {
            currentTagFilter = t.replace(/\s+/g, '-').toLowerCase();
        } else {
            currentTagFilter = "";
        }
    }

    async function searchLogs() {
        return await axios
            .get(`https://raw.githubusercontent.com/suspistew/blog-data/main/gaming/global_meta.json`)
            .then(function ({data}) {
                logs = data;
                let tmpLogs = logs
                    .filter((l, i) => i !== 0)
                    .filter(l => !currentTagFilter || l.tags.some(t => t.replace(/\s+/g, '-').toLowerCase() === currentTagFilter));
                currentPageLogs = tmpLogs.slice(
                    currentPage * pageSize,
                    (currentPage + 1) * pageSize
                );
                totalElements = tmpLogs.length;
                totalPages = Math.ceil(tmpLogs.length / pageSize);
                mainlog = logs[0];
            });
    }

    onMount(async () => {
        initPageFromURL();
        await searchLogs();
    });
    afterNavigate(async () => {
        initPageFromURL();
        await searchLogs();
    })

    function goToPage(page) {
        if (page >= 0 && page < Math.ceil(logs.length / pageSize)) {
            trigger?.(1200);
            setTimeout(() => {
                const anchor = document.getElementById("anchor");
                if (anchor) {
                    const y = anchor.getBoundingClientRect().top + window.scrollY;
                    const headerHeight = 70;
                    window.scrollTo({top: y - headerHeight, behavior: "smooth"});
                }
            }, 1250);
            currentPage = page;
            const url = new URL(window.location);
            url.searchParams.set("page", page + 1);
            if ((page + 1) === 1) {
                url.searchParams.delete("page");
            }
            window.history.pushState({}, "", url);
            let tmpLogs = logs
                .filter((l, i) => i !== 0)
                .filter(l => !currentTagFilter || l.tags.some(t => t.replace(/\s+/g, '-').toLowerCase() === currentTagFilter));
            currentPageLogs = tmpLogs.slice(
                currentPage * pageSize,
                (currentPage + 1) * pageSize
            );
            totalElements = tmpLogs.length;
            totalPages = Math.ceil(tmpLogs.length / pageSize);
        }
    }

    $: startPage = Math.max(currentPage - 3, 0);
    $: endPage = Math.min(currentPage + 3, totalPages - 1);
    $: pages = Array.from(
        {length: endPage - startPage + 1},
        (_, i) => startPage + i
    );


    function selectTag(tag) {
        currentTagFilter = tag;
        currentPage = 0;
        const url = new URL(window.location);
        url.searchParams.set("tag", currentTagFilter);
        url.searchParams.delete("page");
        window.history.pushState({}, "", url);
        goToPage(currentPage);
    }

    function resetFilter() {
        currentTagFilter = "";
        currentPage = 0;
        const url = new URL(window.location);
        url.searchParams.delete("page");
        url.searchParams.delete("tag");
        window.history.pushState({}, "", url);
        goToPage(currentPage);
    }

</script>

<svelte:head>
    <title>Daron Quest - Accueil</title>
    <meta name="description" content="Journal de bord d'un daron passionné par les jeux vidéo."/>
</svelte:head>

<div class="home">
    <Loader onRegister={(fn) => (trigger = fn)}/>
    <div>
        <div>
            <h2>Dernier dossier</h2>
        </div>
        <div class="last-test">
            {#if mainlog}
                <a href={"/"+ mainlog.uri}>
                    <div>
                        <div class="last-test-img">
                            <div>
                                <img src={mainlog.miniature}/>
                            </div>
                        </div>
                        <div class="last-test-descr">
                            <div class="last-test-title">{mainlog.title}</div>
                            <div class="last-test-description">{mainlog.description}</div>
                            <div class="rating">
                                <RatingStars value={mainlog.note} size={24}/>
                            </div>
                        </div>
                    </div>
                </a>
            {/if}
        </div>

        <div class="tags-list">
            <div class="tag tag-clickable tiny-tag nintendo-switch-2"
                 on:click={selectTag("nintendo-switch-2".replace(/\s+/g, '-').toLowerCase())}>
                <div class="tag-flex">
                    <div>
                        Nintendo switch 2
                    </div>
                </div>
            </div>
            <div class="tag tag-clickable tiny-tag nintendo-switch"
                 on:click={selectTag("nintendo-switch".replace(/\s+/g, '-').toLowerCase())}>
                <div class="tag-flex">
                    <div>
                        Nintendo switch
                    </div>
                </div>
            </div>
            <div class="tag tag-clickable tiny-tag snes"
                 on:click={selectTag("snes".replace(/\s+/g, '-').toLowerCase())}>
                <div class="tag-flex">
                    <div>
                        SNES
                    </div>
                </div>
            </div>
            <div class="tag tag-clickable tiny-tag nes" on:click={selectTag("nes".replace(/\s+/g, '-').toLowerCase())}>
                <div class="tag-flex">
                    <div>
                        NES
                    </div>
                </div>
            </div>
            <div class="tag tag-clickable tiny-tag ps5" on:click={selectTag("ps5".replace(/\s+/g, '-').toLowerCase())}>
                <div class="tag-flex">
                    <div>
                        Playstation 5
                    </div>
                </div>
            </div>
            <div class="tag tag-clickable tiny-tag ps2" on:click={selectTag("ps2".replace(/\s+/g, '-').toLowerCase())}>
                <div class="tag-flex">
                    <div>
                        Playstation 2
                    </div>
                </div>
            </div>
            <div class="tag tag-clickable tiny-tag pc" on:click={selectTag("pc".replace(/\s+/g, '-').toLowerCase())}>
                <div class="tag-flex">
                    <div>
                        PC
                    </div>
                </div>
            </div>
        </div>
    </div>
    {#if currentTagFilter}
        <div class="tag-filter">
            Filtrage actuel sur le tag
            <div class={"tiny-tag tag " + currentTagFilter.replace(/\s+/g, '-').toLowerCase()}>{currentTagFilter}</div>
            - <a on:click={resetFilter}>Supprimer le filtre</a>
        </div>
    {/if}
    {#if !currentTagFilter}
        <div class="tag-filter">
            Aucun filtre
        </div>
    {/if}
    <div id="anchor">
        <br/>
        <h2>
            {#if currentTagFilter}
                Résultats
            {/if}
            {#if !currentTagFilter}
                Dossiers récents
            {/if}
            {#if currentPage !== 0}
                 (Page {currentPage+1})
            {/if}
        </h2>
    </div>
    <div class="articles">
        {#each currentPageLogs as m}
            {#if m.published}
                <a href={"/"+ m.uri} class="article">
                    <div class="article-flex">
                        <div class="article-img">
                            <div>
                                <img src={m.miniature}/>
                            </div>
                        </div>
                        <div style="box-sizing: border-box; width: 100%; padding:0.5rem 1rem 0.8rem 1rem;">
                            <div class="article-title">
                                <span>{m.title}</span>
                            </div>
                            <div class="article-date">{m.date}</div>
                            <br/>
                            <div class="article-description">{@html m.description}</div>

                            <div class="note rating">
                                <RatingStars value={m.note} size={24}/>
                            </div>


                            <div class={"article-tags"}>
                                {#each m.tags as tag}
                                    <div class={"tag tag-clickable " + tag.replace(/\s+/g, '-').toLowerCase()}
                                         on:click={selectTag(tag.replace(/\s+/g, '-').toLowerCase())}>{tag}</div>
                                {/each}
                                <div class={"tag articletag"}>Article</div>
                            </div>
                        </div>
                    </div>
                </a>
            {:else}
                <div class="article">
                    <div class="article-flex">
                        <div class="article-img">
                            <div>
                                <img src={m.miniature}/>
                            </div>
                        </div>
                        <div style="box-sizing: border-box; width: 100%; padding:0.5rem 1rem 0.8rem 1rem;">
                            <div class="article-title">
                                <span>{m.title}</span>
                            </div>
                            <div class="article-date">{m.date}</div>
                            <br/>
                            <div class="article-description">{@html m.description}</div>

                            <div class="note rating">
                                <RatingStars value={m.note} size={24}/>
                            </div>

                            <div class={"article-tags"}>
                                {#each m.tags as tag}
                                    <div class={"tag tag-clickable " + tag.replace(/\s+/g, '-').toLowerCase()}
                                         on:click={selectTag(tag.replace(/\s+/g, '-').toLowerCase())}>{tag}</div>
                                {/each}
                            </div>
                        </div>
                    </div>
                </div>
            {/if}

        {/each}
    </div>
    <nav style="text-align: center; margin-top: 2em;">
        {#if totalPages > 0}
            <button
                    on:click={() => goToPage(currentPage - 1)}
                    disabled={currentPage === 0}
                    style="margin-right:1em;padding:0.5rem;cursor:pointer; font-family: 'Noto Sans', monospace;"
            >
                Précédent
            </button>

            {#if startPage > 0}
                <span>..</span>
            {/if}

            {#each pages as page}
                {#if page === currentPage}
                    <button disabled style="margin:0 0.5em;">{page + 1}</button>
                {:else}
                    <button
                            on:click={() => goToPage(page)}
                            style="margin:0 0.5em;"
                    >
                        {page + 1}
                    </button>
                {/if}
            {/each}

            {#if endPage < totalPages - 1}
                <span>..</span>
            {/if}

            <button
                    on:click={() => goToPage(currentPage + 1)}
                    disabled={currentPage === totalPages - 1}
                    style="margin-left:1em; padding:0.5rem;cursor:pointer;"
            >
                Suivant
            </button>
        {/if}
    </nav>
</div>


<style>
    .note {
        margin: 1rem 0 1rem 0;
    }


    .home {
        height: 100%;
        width: 1024px;
        margin: auto;
        font-weight: 400;
        font-size: 16px;
        display: flex;
        flex-direction: column;
    }

    @media (max-width: 1024px) {
        .home {
            width: 95%;
            margin: auto;
        }
    }

    .description-page {
        margin-top: 2rem;
    }

    .tags-list {
        margin-top: 2rem;
        width: 100%;
    }

    @media (max-width: 1024px) {
        .tags-list {
            display: none;
        }
    }

    .articles {
        display: flex;
        gap: 2rem;
        flex-wrap: wrap;
    }

    .articles a {
        text-decoration: none;
        color: #121212;
    }

    .article {
        background: #ebddcd;
        border-radius: 0.5rem;
        border: 1px solid #a48875;
    }

    @media (max-width: 1024px) {
        .article {
            flex: 1 1 calc(50% - 2rem);
            max-width: calc(50%);
        }
    }

    @media (max-width: 680px) {
        .tag-filter {
            display: none;
        }

        .article {
            flex: 1 1 calc(100%);
            max-width: calc(100%);
        }
    }

    @media (min-width: 1024px) {
        .article {
            flex: 0 0 calc(33.333% - 2rem); /* largeur fixe = 1/3 */
            max-width: calc(33.333%);
        }
    }

    .article img {
        width: 100%;
        height: auto;
        border-top-right-radius: 0.5rem;
        border-top-left-radius: 0.5rem;
    }

    .article-date {
        font-size: 0.9rem;
    }

    .article-title {
        font-size: 0.9rem;
        font-weight: 800;
    }

    .article-title a {
        text-decoration: none;
        color: #121212;
        text-transform: uppercase;
    }

    .article-description {
        font-size: 0.85rem;
        height: 95px;
    }

    @media (max-width: 680px) {
        .article-description {
            font-size: 1rem;
            height: auto;
        }
    }

    .article:hover {
        background: #d5c1ac;
        cursor: pointer;
    }

    .article:hover img {
        opacity: 0.9;
    }

    .article:active {
        background: #bba18c;
        cursor: pointer;
    }

    .article:active img {
        opacity: 0.7;
    }

    .tag-filter {
        margin-top: 15px;
        font-size: 0.8rem;
    }

    .tag-filter a {
        cursor: pointer;
    }

    .tag-filter a:hover {
        text-decoration: underline;
        color: #1b4566;
    }

    .last-test {
        width: 100%;
        border-radius: 0.5rem;
        position: relative;
        text-decoration: none;
        color: white;
        border: 1px solid #a48875;
        padding: 0;
        margin: 0;
    }

    @media (min-width: 1024px) {
        .last-test {
            height: 576px;
        }
    }

    .last-test-img img {
        width: 100%;
        border-radius: 0.5rem;
        z-index: 3;
        display: block;
    }

    .last-test-descr {
        position: absolute;
        bottom: 0;
        z-index: 999;
        background: rgba(20, 20, 20, 0.7);
        width: 100%;
        height: 9rem;
        color: white;
        box-sizing: border-box;
        padding: 1rem;
        border-bottom-left-radius: 0.5rem;
        border-bottom-right-radius: 0.5rem;
    }

    @media (max-width: 680px) {
        .last-test-descr {
            height: auto;
            padding: 0.4rem 1rem;
            max-height: 100%;
        }
    }

    .last-test-title {
        font-weight: 800;
        font-size: 2rem;

    }

    @media (max-width: 680px) {
        .last-test-title {
            margin-top: 5px;
            font-size: 1.2rem !important;
        }

        .last-test-description {
            font-size: 1rem !important;
        }
    }

    @media (max-width: 310px) {
        .rating {
            display: none;
        }
    }

    .last-test-description {
        font-size: 0.9rem;
        font-weight: 300;
        margin-top: 5px;
        margin-bottom: 10px;
    }

    h2 {
        font-family: "Pacifico", cursive;
        font-weight: 100;
        color: #4f381c;
        margin: 0 0 1rem 0;
    }


    .last-test:hover {
        background: #d5c1ac;
        cursor: pointer;
    }

    .last-test:hover .last-test-title {
        text-decoration: underline;
    }

    .last-test:hover img {
        opacity: 0.9;
    }

    .last-test:active {
        background: #bba18c;
        cursor: pointer;
    }

    .last-test:active img {
        opacity: 0.7;
    }

    button {
        background: #ebddcd;
        border: 1px solid #a48875;
        border-radius: 0.3rem;
        font-size: 0.8rem;
        font-family: "Inter", monospace;
        font-weight: 400;
    }

    button:not(:disabled):hover {
        background: #d5c1ac;
        cursor: pointer;
    }

    button:not(:disabled):active {
        background: #bba18c;
        cursor: pointer;
    }
</style>