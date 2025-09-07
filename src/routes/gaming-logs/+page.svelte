<script>

import Snes from "../../components/tags/Snes.svelte";
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
        <div class="description-page">
            Un petit condensé des jeux auxquels je joue, que je note et dont je garde une trace précieusement dans
            mon périple de gamer.
        </div>
        <div class="tags-list">
            <div><b>Filtrer : </b></div><br/>
            <div class="tag tag-clickable tiny-tag nintendo-switch2">
                <div class="tag-flex">
                    <div>
                        <img
                                src="https://raw.githubusercontent.com/suspistew/blog-data-statics/refs/heads/main/static/switch2-tiny.png"
                                alt="logo switch"/>
                    </div>
                    <div>
                        Nintendo switch 2
                    </div>
                </div>
            </div>
            <div class="tag tag-clickable tiny-tag nintendo-switch">
                <div class="tag-flex">
                    <div>
                        <img
                                src="https://raw.githubusercontent.com/suspistew/blog-data-statics/refs/heads/main/static/switch-icon.png"
                                alt="logo switch"/>
                    </div>
                    <div>
                        Nintendo switch
                    </div>
                </div>
            </div>
            <Snes></Snes>
            <div class="tag tag-clickable tiny-tag ps5">
                <div class="tag-flex">
                    <div>
                        <img
                                src="https://raw.githubusercontent.com/suspistew/blog-data-statics/refs/heads/main/static/PS5_logo.png"
                                alt="logo ps5"/>
                    </div>
                </div>
            </div>
        </div>
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

    .description-page {
        margin-top: 2rem;
    }

    .tags-list {
        margin-top: 2rem;
        width: 100%;
    }
</style>