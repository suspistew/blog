<script>
    import {onMount} from "svelte";
    import axios from "axios";

    let logs = [];
    let currentPageLogs = [];
    let currentPage = 0;
    let totalPages = 1;
    let pageSize = 4;
    let currentTagFilter = "";
    let totalElements = 0;

    function initPageFromURL() {
        const params = new URLSearchParams(window.location.search);
        const p = parseInt(params.get("page"));
        const t = params.get("tag");
        if (!isNaN(p) && p >= 1) {
            currentPage = p - 1;
        }
        if (t) {
            currentTagFilter = t.replace(/\s+/g, '-').toLowerCase();
        }
    }

    async function searchLogs() {
        return await axios
            .get(`https://raw.githubusercontent.com/jerthz/grzi.dev/main/posts/global_meta.json`)
            .then(function ({data}) {
                logs = data;
                let tmpLogs = logs.filter(l => !currentTagFilter || l.tag.replace(/\s+/g, '-').toLowerCase() === currentTagFilter);
                currentPageLogs = tmpLogs.slice(
                    currentPage * pageSize,
                    (currentPage + 1) * pageSize
                );
                totalElements = tmpLogs.length;
                totalPages = Math.ceil(tmpLogs.length / pageSize);
            });
    }

    onMount(async () => {
        initPageFromURL();
        await searchLogs();
    });

    $: startPage = Math.max(currentPage - 3, 0);
    $: endPage = Math.min(currentPage + 3, totalPages - 1);
    $: pages = Array.from(
        {length: endPage - startPage + 1},
        (_, i) => startPage + i
    );

    function goToPage(page) {
        if (page >= 0 && page < Math.ceil(logs.length / pageSize)) {
            currentPage = page;
            const url = new URL(window.location);
            url.searchParams.set("page", page + 1);
            if ((page+1) === 1){
                url.searchParams.delete("page");
            }
            window.history.pushState({}, "", url);
            let tmpLogs = logs.filter(l => !currentTagFilter || l.tag.replace(/\s+/g, '-').toLowerCase() === currentTagFilter);
            currentPageLogs = tmpLogs.slice(
                currentPage * pageSize,
                (currentPage + 1) * pageSize
            );
            totalElements = tmpLogs.length;
            totalPages = Math.ceil(tmpLogs.length / pageSize);
        }
    }

    function selectTag(tag){
        currentTagFilter = tag;
        currentPage = 0;
        const url = new URL(window.location);
        url.searchParams.set("tag", currentTagFilter);
        url.searchParams.delete("page");
        window.history.pushState({}, "", url);
        goToPage(currentPage);
    }

    function resetFilter(){
        currentTagFilter = "";
        currentPage = 0;
        const url = new URL(window.location);
        url.searchParams.delete("page");
        url.searchParams.delete("tag");
        window.history.pushState({}, "", url);
        goToPage(currentPage);
    }
</script>
<div class="home">
    <div>
        <h3 class="title">
            Suspistew - logs
        </h3>
        <div>
            <a href="/">About</a>
            - <a href="/projects">Projets</a>
            - <a href="/stats">Stats</a>
        </div>

        {#if currentTagFilter}
            <div class="tag-filter">
                Filtrage actuel sur le tag <div class={"tag " + currentTagFilter.replace(/\s+/g, '-').toLowerCase()}>{currentTagFilter}</div> - <a on:click={resetFilter}>Supprimer le filtre</a>
            </div>
        {/if}
        <div class="articles">
            {#each currentPageLogs as m}
                <div class="article">
                    <div class="article-flex">
                        <div class="article-img">
                            <div>
                                <img src="https://avatars.githubusercontent.com/u/3636719?v=4" style="height: 160px;"/>
                            </div>
                        </div>
                        <div style="width: 100%;">
                            <div class="article-title">
                                <a href={"/logs/" + m.uri}>{m.title}</a>
                            </div>
                            <div>{m.date}</div>
                            <br/>
                            <div class="article-description">{m.description}</div>

                            <div class={"article-tags"}>
                                <div class={"tag tag-clickable " + m.tag.replace(/\s+/g, '-').toLowerCase()} on:click={selectTag(m.tag.replace(/\s+/g, '-').toLowerCase())}>{m.tag}</div>
                            </div>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
        <nav style="text-align: center; margin-top: 2em;padding-bottom:20px;">
            {#if totalPages > 1}
                <button
                        on:click={() => goToPage(currentPage - 1)}
                        disabled={currentPage === 0}
                        style="margin-right:1em;padding:0.5rem;cursor:pointer; font-family: 'Chivo Mono', monospace;"
                >
                    ◀ Previous
                </button>

                {#if startPage > 0}
                    <span>..</span>
                {/if}

                {#each pages as page}
                    {#if page === currentPage}
                        <strong>[{page + 1}]</strong>
                    {:else}
                        <a
                                href="javascript:void(0)"
                                on:click={() => goToPage(page)}
                                style="margin:0 0.5em;"
                        >
                            {page + 1}
                        </a>
                    {/if}
                {/each}

                {#if endPage < totalPages - 1}
                    <span>..</span>
                {/if}

                <button
                        on:click={() => goToPage(currentPage + 1)}
                        disabled={currentPage === totalPages - 1}
                        style="margin-left:1em; padding:0.5rem;cursor:pointer;font-family: 'Chivo Mono', monospace;"
                >
                    Next ▶
                </button>
            {/if}
        </nav>
    </div>
</div>

<style>
    .home {
        height: 100%;
        width: 850px;
        margin: auto;
        font-weight: 200;
        font-size: 16px;
        display: flex;
        flex-direction: row;
    }

    .title {
        font-weight: 500;
    }

    .article-flex {
        box-sizing: border-box;
        padding: 1.5rem;
        background: white;
        border-radius: 10px;
    }

    .articles {
        display: flex;
        flex-direction: column;
        gap: 15px;
        margin-top: 42px;
        width: 100%;
    }

    .tag-filter{
        margin-top: 30px;
        font-size: 0.8rem;
    }

    .tag-filter a{
        cursor: pointer;
    }
    .tag-filter a:hover{
        text-decoration: underline;
        color: #1b4566;
    }

    .article-flex {
        display: flex;
        gap: 10px;
        width: 100%;
    }

    .article:not(:last-child)::after {
        content: '• • •';
        display: block;
        text-align: center;
        margin: 15px 0 0 0;
        color: #333;
    }

    .article-title {
        font-weight: 400;
    }

    .article-title a {
        color: black;
    }

    .article-title a:hover {
        color: #222299;
    }

    .article-tags {
        width: 100%;
        margin-top: 10px;
        font-size: 12px;
        font-weight: 200;
    }

    .tag {
        border: 1px solid #444;
        display: inline-block;
        padding: 6px;
        border-radius: 4px;
    }

    .tag-clickable:hover{
        cursor: pointer;
        opacity: 0.8;
    }

    .article-description {
        font-weight: 100;
        height: 69px;
    }

    @media (max-width: 850px) {
        .article-img {
            display: none;
        }

        .article-description {
            height: auto;
        }
    }

    .article-img {
        text-align: left;
        font-size: 16px;
        min-width: 160px;
        margin-right: 10px;
    }

    .article-img img {
        border: 4px solid #333;
    }

    @media (max-width: 1024px) {
        .home {
            width: 90%;
            margin: auto;
        }
    }

    .rétro-gaming {
        background: #803526;
        color: white;
    }

    .vidéo-game, .video-game {
        background: #467fab;
        color: white;
    }
</style>