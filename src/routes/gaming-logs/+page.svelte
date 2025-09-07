<script>

    import axios from "axios";
    import {onMount} from "svelte";
    import RatingStars from "../../components/RatingStars.svelte";

    let logs = [];
let currentPageLogs = [];
let currentPage = 0;
let totalPages = 1;
let pageSize = 6;
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
        .get(`https://raw.githubusercontent.com/suspistew/blog-data/main/gaming/global_meta.json`)
        .then(function ({data}) {
            logs = data;
            let tmpLogs = logs.filter(l => !currentTagFilter || l.tags.some(t => t.replace(/\s+/g, '-').toLowerCase() === currentTagFilter));
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

function goToPage(page) {
    if (page >= 0 && page < Math.ceil(logs.length / pageSize)) {
        currentPage = page;
        const url = new URL(window.location);
        url.searchParams.set("page", page + 1);
        if ((page+1) === 1){
            url.searchParams.delete("page");
        }
        window.history.pushState({}, "", url);
        let tmpLogs = logs.filter(l => !currentTagFilter || l.tags.some(t=>t.replace(/\s+/g, '-').toLowerCase() === currentTagFilter));
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
            Suspistew - Gaming logs
        </h3>
        <div>
            <a href="/">About</a>
            - <a href="/logs">Logs</a>
            - <a href="/drawings">Dessins</a>
        </div>

        {#if currentTagFilter}
            <div class="tag-filter">
                Filtrage actuel sur le tag <div class={"tiny-tag tag " + currentTagFilter.replace(/\s+/g, '-').toLowerCase()}>{currentTagFilter}</div> - <a on:click={resetFilter}>Supprimer le filtre</a>
            </div>
        {/if}
        {#if !currentTagFilter}
            <div class="tag-filter">
                Aucun filtre
            </div>
        {/if}

        <div class="tags-list">
            <div class="tag tag-clickable tiny-tag nintendo-switch-2" on:click={selectTag("nintendo-switch-2".replace(/\s+/g, '-').toLowerCase())}>
                <div class="tag-flex">
                    <div>
                        Nintendo switch 2
                    </div>
                </div>
            </div>
            <div class="tag tag-clickable tiny-tag nintendo-switch" on:click={selectTag("nintendo-switch".replace(/\s+/g, '-').toLowerCase())}>
                <div class="tag-flex">
                    <div>
                        Nintendo switch
                    </div>
                </div>
            </div>
            <div class="tag tag-clickable tiny-tag snes" on:click={selectTag("snes".replace(/\s+/g, '-').toLowerCase())}>
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
    <div>
        <br/>
        <h2>Mes derniers jeux</h2>
    </div>
    <div class="articles">
        {#each currentPageLogs as m}
            {#if m.published}
                <a  href={"/gaming-logs/"+ m.uri} class="article">
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

                            <div class="note">
                                <RatingStars value={m.note} size={16}/>
                            </div>


                            <div class={"article-tags"}>
                                {#each m.tags as tag}
                                    <div class={"tag tag-clickable " + tag.replace(/\s+/g, '-').toLowerCase()} on:click={selectTag(tag.replace(/\s+/g, '-').toLowerCase())}>{tag}</div>
                                {/each}
                                <div class={"tag"}>Article</div>
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

                            <div class="note">
                                <RatingStars value={m.note} size={16}/>
                            </div>

                            <div class={"article-tags"}>
                                {#each m.tags as tag}
                                    <div class={"tag tag-clickable " + tag.replace(/\s+/g, '-').toLowerCase()} on:click={selectTag(tag.replace(/\s+/g, '-').toLowerCase())}>{tag}</div>
                                {/each}
                            </div>
                        </div>
                    </div>
                </div>
            {/if}

        {/each}
    </div>
    <nav style="text-align: center; margin-top: 2em;padding-bottom:20px;">
        {#if totalPages > 0}
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


<style>
    .note{
        margin: 1rem 0 1rem 0;
    }
    code{
        font-weight: 800;
    }


    .home {
        height: 100%;
        width: 850px;
        margin: auto;
        font-weight: 200;
        font-size: 16px;
        display: flex;
        flex-direction: column;
    }

    .description-page {
        margin-top: 2rem;
    }

    .tags-list {
        margin-top: 2rem;
        width: 100%;
    }

    .articles{
        display: flex;
        gap: 2rem;
        flex-wrap: wrap;
    }
    .articles a {
        text-decoration: none;
        color: #121212;
    }

    .article{
        flex: 1 1 calc(33.333% - 2rem);
        max-width: calc(33.333% - 2rem);
        background: #fff;
        border-radius: 0.5rem;
        border: 1px solid #ccc;
    }
    .article img{
        width: 100%;
        height: auto;
        border-top-right-radius: 0.5rem;
        border-top-left-radius: 0.5rem;
    }

    .article-date{
        font-size:0.9rem;
    }

    .article-title{
        font-size: 0.9rem;
        font-weight: 800;
    }
    .article-title a{
        text-decoration: none;
        color: #121212;
        text-transform: uppercase;
    }
    .article-description{
        font-size: 0.85rem;
        height: 95px;
    }
    .article:hover{
        background: #bbb;
        cursor:pointer;
    }
    .article:hover img{
        opacity: 0.9;
    }
    .article:active{
        background: #999;
        cursor:pointer;
    }
    .article:active img{
        opacity: 0.7;
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
</style>