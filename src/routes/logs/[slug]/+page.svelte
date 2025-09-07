<script>
    import axios from "axios";
    import {onMount} from "svelte";
    import {page} from '$app/stores';

    let log = {
        date: "Loading",
        title: "Loading",
        description: "Loading",
        url: "Loading",
    };

    let logContent = "";

    async function getLog() {
        const json = await axios.get("https://raw.githubusercontent.com/suspistew/blog-data/main/posts/src/" + $page.params.slug + "/meta.json");
        log = json.data;
        const html = await axios.get("https://raw.githubusercontent.com/suspistew/blog-data/main/posts/src/" + $page.params.slug + "/blog-post.html");
        logContent = html.data;
    }

    onMount(async () => {
        await getLog();
    });
</script>
<div class="home">
    <div>
        <h3 class="title">Suspistew</h3>
        <div>
            <a href="/">About</a>
            - <a href="/drawings">Dessins</a>
            - <a href="/logs">Logs</a>
            - <a href="/gaming-logs">Gaming logs</a>
        </div>
        <div class="log">
            <div class="log-title">
                {log.title}
            </div>
            <div class="log-title-separator">
            </div>
            <div class="log-date">
                {#each log.tags as tag}
                    <a href={"/logs?tag=" + tag.replace(/\s+/g, '-').toLowerCase()} class={"tag tag-clickable " + tag.replace(/\s+/g, '-').toLowerCase()} on:click={selectTag(tag.replace(/\s+/g, '-').toLowerCase())}>{tag}</a>
                {/each}
                <div>
                    {log.date}
                </div>
            </div>
            <div class="log-content">
                {@html logContent}
            </div>
        </div>
    </div>
</div>

<style>
    .title {
        font-weight: 500;
    }

    .home {
        height: 100%;
        width: 768px;
        margin: auto;
        font-weight: 200;
        font-size: 16px;
        display: flex;
        flex-direction: row;
    }

    @media (max-width: 1024px) {
        .home {
            width: 90%;
            margin:auto;
        }
    }

    .log {
        display: flex;
        flex-direction: column;
        gap: 15px;
        margin-top: 42px;
        background: white;
        padding: 2rem;
        border: 1px solid #555;
        border-radius: 0.4rem;
    }

    .log-title {
        font-weight: 600;
        font-size: 24px;
        text-align: center;
    }

    .log-title-separator {
        width: 50%;
        margin: 1rem auto 0 auto;
        height: 1px;
        border-bottom: 1px dashed #666;
    }

    .log-date {
        text-align: center;
        font-weight: 100;
        font-size: 12px;
    }

    .tag {
        border: 1px solid #444;
        display: inline-block;
        padding: 6px;
        border-radius: 4px;
        margin-bottom: 5px;
    }
    a{
        text-decoration: none;
    }


</style>