// IT WILL SHOW BAR WHEN THE SCREEN IS MINIMIZE
document.addEventListener('DOMContentLoaded', function() {
    const menuIcon = document.querySelector('#menu-icon');
    const home = document.querySelector('.home');
    const navbar = document.querySelector('.navbar');
    const navbg = document.querySelector('.nav-bg');

    console.log(menuIcon, home, navbar, navbg); // Debugging line

    if (menuIcon) {
        menuIcon.addEventListener('click', function() {
            console.log('Menu icon clicked'); // Debugging line
            menuIcon.classList.toggle('bx-x');
            home.classList.toggle('active');
            navbar.classList.toggle('active');
            navbg.classList.toggle('active');
        });
    }
});