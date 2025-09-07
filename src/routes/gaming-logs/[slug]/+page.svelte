<script>
    import axios from "axios";
    import {onMount} from "svelte";
    import {page} from '$app/stores';
    import RatingStars from "../../../components/RatingStars.svelte";
    import Carousel from "../../../components/Carousel.svelte";

    let log = {
        date: "Loading",
        title: "Loading",
        description: "Loading",
        url: "Loading",
        gallery: []
    };

    let logContent = "";

    async function getLog() {
        const json = await axios.get("https://raw.githubusercontent.com/suspistew/blog-data/refs/heads/main/gaming/src/" + $page.params.slug + "/meta.json");
        log = json.data;
        const html = await axios.get("https://raw.githubusercontent.com/suspistew/blog-data/refs/heads/main/gaming/src/" + $page.params.slug + "/gaming-post.html");
        logContent = html.data;
    }

    onMount(async () => {
        await getLog();
    });
</script>
<div class="home">
    <div style="width:100%;">
        <h3 class="title">Suspistew</h3>
        <div>
            <a href="/">About</a>
            - <a href="/drawings">Dessins</a>
            - <a href="/logs">Logs</a>
            - <a href="/gaming-logs">Gaming logs</a>
        </div>
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
                        <a href={"/gaming-logs?tag=" + tag.replace(/\s+/g, '-').toLowerCase()}
                           class={"tag tag-clickable " + tag.replace(/\s+/g, '-').toLowerCase()}
                           on:click={selectTag(tag.replace(/\s+/g, '-').toLowerCase())}>{tag}</a>
                    {/each}
                    <div>
                        {log.date}
                    </div>
                </div>
                <div class="log-content">
                    {@html logContent}
                </div>

                <div class="log-note">
                    <h3>Note</h3>
                    <RatingStars value={log.note}/>
                </div>
                {#if log.gallery}
                    <div class="log-gallery">
                        <h3>Gallerie d'images</h3>
                        <Carousel images={log.gallery}/>
                    </div>
                {/if}

                <div class="goback">
                <a href="/gaming-logs">Voir tous les tests de jeux</a>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .goback{
        text-align: right;
        font-size: 0.9rem;
        margin-top: 1rem;
    }
    .title {
        font-weight: 500;
    }

    .home {
        height: 100%;
        width: 850px;
        margin: auto;
        font-weight: 200;
        font-size: 16px;
        display: flex;
        flex-direction: row;
    }

    @media (max-width: 1024px) {
        .home {
            width: 90%;
            margin: auto;
        }
    }

    .log {
        margin-top: 1rem;
        display: flex;
        flex-direction: column;
        gap: 15px;
        background: white;
        border: 1px solid #555;
        border-radius: 0.4rem;
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
        font-size: 24px;
        text-align: center;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    .log-title-separator {
        width: 50%;
        margin: 0.2rem auto 1.4rem auto;
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

    a {
        text-decoration: none;
    }

</style>