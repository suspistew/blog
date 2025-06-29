<script>
    import {onMount} from "svelte";
    import axios from "axios";

    let logs = [];
    let currentPageLogs = [];
    let currentPage = 0;
    let totalPages = 1;
    let pageSize = 4;
    let totalElements = 0;

    async function searchLogs() {
        return await axios
            .get(`https://raw.githubusercontent.com/jerthz/grzi.dev/main/posts/global_meta.json`)
            .then(function ({data}) {
                logs = data;
                currentPageLogs = logs.slice(
                    currentPage * pageSize,
                    (currentPage + 1) * pageSize
                );
                totalElements = logs.length;
                totalPages = Math.ceil(logs.length / pageSize);
            });
    }

    onMount(async () => {
        await searchLogs();
    });

    $: startPage = Math.max(currentPage - 3, 0);
    $: endPage = Math.min(currentPage + 3, totalPages - 1);
    $: pages = Array.from(
        { length: endPage - startPage + 1 },
        (_, i) => startPage + i
    );

    function goToPage(page) {
        if (page >= 0 && page < Math.ceil(logs.length / pageSize)) {
            currentPage = page;
            currentPageLogs = logs.slice(
                currentPage * pageSize,
                (currentPage + 1) * pageSize
            );
        }
    }
</script>
<div class="home">
    <div>
        <h3 class="title">
            Suspistew - logs
        </h3>
        <div>
            <a href="/">About</a> - <a href="https://github.com/suspistew/" target="_blank">Github</a>
            - <a href="/stats">Stats</a>
        </div>
        <div class="articles">
            {#each currentPageLogs as m}
                <div class="article">
                    <div class="article-flex">
                        <div class="article-img">
                            <div>
                                <img src="https://avatars.githubusercontent.com/u/3636719?v=4" style="height: 140px;"/>
                            </div>
                        </div>
                        <div style="width: 100%;">
                            <div class="article-title">
                                <a href={"/logs/" + m.uri}>{m.title}</a>
                            </div>
                            <div>{m.date}</div>
                            <br/>
                            <div class="article-description">{m.description}</div>

                            <div class="article-tags">
                                {m.tag}
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
        padding:1.5rem;
        background:white;
        border-radius: 10px;
    }
    .articles {
        display: flex;
        flex-direction: column;
        gap: 15px;
        margin-top: 42px;
        width: 100%;
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
        margin: 20px 0 5px 0;
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

    .article-description {
        font-weight: 100;
        height:69px;
    }
    @media (max-width: 850px) {
        .article-img {
            display:none;
        }
        .article-description {
            height:auto;
        }
    }

    .article-img {
        text-align: left;
        font-size: 16px;
        min-width: 140px;
        margin-right: 10px;
    }
    .article-img img{
        border: 4px solid #333;
    }

    @media (max-width: 1024px) {
        .home {
            width: 90%;
            margin: auto;
        }
    }
</style>