class MyHead extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
        <head>
        <meta http-equiv="content-type" content="text/html">
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="stylesheet" href="/static/styles/home.css">
        <script src="/static/styles/home.js" defer></script> 
        <title>Club de Programación Competitiva</title>
        <link rel="stylesheet" href="https://unicons.iconscout.com/release/v4.0.0/css/line.css" />

    </head>
        `;
    }
}
customElements.define('my-head', MyHead);

class MyNav extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
        <nav>
            <nav class="nav" id="navbar">
                <i class="uil uil-bars navOpenBtn"></i>
                <a href="/"><img src="static/images/globos.jpg" alt="logo" class="logo"></a> <!-- ver xq no funciona cargar la imagen-->
                <ul class="nav-links">
                  <i class="uil uil-times navCloseBtn"></i>
                  <li><a href="/">Home</a></li>
                  <li><a href="/faq">FAQ</a></li>
                  <li><a href="blog">Blog</a></li>
                  <li><a href="sign_up" class="SignUp">Sign Up</a></li>
                  <li><a href="log_in" class="LogIn">Log In</a></li>
                </ul>
            </nav>
        </nav>
        `;
    }
}
customElements.define('my-nav', MyNav);