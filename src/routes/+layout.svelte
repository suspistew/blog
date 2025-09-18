<script>
    import './style.css';
</script>

<div class="app">
    <div class="header">
        <div class="conteneur-header">
            <a href="/" class="homelink" title="Revenir à l'accueil">
                <img src="/static/logo3.png"/>
            </a>
            <a href="/" class="homelink logotexte" title="Revenir à l'accueil" >
                <img src="/static/logotexte.png"/>
            </a>
        </div>
    </div>
    <main>
        <slot/>
    </main>
    <div class="footer">
        Made with ❤️ - par Stew
    </div>
</div>

<style lang="scss">
  @media (max-width: 1024px) {
    .app {
      width: 100%;
      margin: auto;
    }
  }

  main {
    height: 100%;
    width: 1024px;
    margin: auto;
    padding-top: 6rem;
  }
  @media (max-width: 768px) {
    main {
      padding-top: 5rem;
    }
  }

  @media (max-width: 1024px) {
    main {
      width: 100%;
      margin: auto;
    }
  }

  .header {
    height: 5rem;
    background-color: #ccb298;
    box-sizing: border-box;
    border-bottom: 1px solid #a48875;
    color: white;
    position:fixed;
    width: 100%;
    z-index: 10000;
  }

  @media (max-width: 768px) {
    .header {
      height: 4rem;
    }
  }

  .conteneur-header {
    max-width: 1024px;
    margin: auto;
    height: 100%;
    display: flex;
    align-items: center;
  }

  .logo {
    margin-top: -0.8rem;
    font-weight: 900;
    font-size: 2.1rem;
    color: #4f381c;
    font-family: "Pacifico", cursive;
  }

  .accroche {
    margin-top: -0.2rem;
    font-weight: 400;
    font-size: 0.9rem;
    color: #695946;
  }

  @media (max-width: 768px) {
    .accroche {
      display: none;
    }

    .logotexte img{
      margin-top: 0.5rem;
    }
  }

  .footer{
    margin-top: 2rem;
    height: 3.5rem;
    background-color: #ccb298;
    box-sizing: border-box;
    border-top: 1px solid #a48875;
    color: white;
    padding: 1rem 0 0.6rem 0;
    text-align:center;
    width: 100%;
    font-weight: 100;
    font-size: 1.2rem;
    color: #695946;
    font-family: cursive;
  }
  .homelink{
    height: 100%;
  }
  .homelink:hover img{
    opacity:0.8;
    cursor:pointer;
  }
  .homelink img{
    height: 100%;
  }

  .logotexte img{
    margin-top: 0.7rem;
    margin-left: 1.5rem;
    height:70%
  }

  @media (max-width: 1024px) {
    .conteneur-header {
      width: 100%;
      padding: 0 1rem;
      box-sizing: border-box;
    }
    .logo {
      margin-top: 0.2rem;
      font-size: 1.5rem;
    }
    .accroche {
      font-size: 0.9rem;
    }
    .logotexte img{
      margin-top: 0.7rem;
    }
  }
</style>