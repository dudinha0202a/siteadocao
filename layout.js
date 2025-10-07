async function include(selector, url) {
const el = document.querySelector(selector);
if (!el) return;
const res = await fetch(url);
const html = await res.text();
el.innerHTML = html;
}


// Em todas as páginas:
include('#header-include', 'partials/header.html');
include('#footer-include', 'partials/footer.html');