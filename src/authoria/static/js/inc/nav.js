const navIcon = document.getElementById('nav-button-open');
const closeIcon = document.getElementById('nav-button-close');
const slideMenu = document.getElementById('slideout-menu');


navIcon.addEventListener('click', () => {
    slideMenu.classList.add('open');
});

closeIcon.addEventListener('click', () => {
    slideMenu.classList.remove('open');
});
