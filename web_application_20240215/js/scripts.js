/*!
* Start Bootstrap - Landing Page v6.0.6 (https://startbootstrap.com/theme/landing-page)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-landing-page/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project



window.addEventListener('load', function() {
    window.scrollTo(0, 0); // Scroll to the top of the page
  });


document.addEventListener('scroll', function() {
    var navbar = document.querySelector('.navbar-nav');
    var scrollPosition = window.scrollY;
  
    if (scrollPosition >= 20) {
      navbar.style.position = 'fixed';
      navbar.style.top = '0';
      navbar.style.width = "100%"
    } else {
      navbar.style.position = 'relative';
      navbar.style.top = '20px'; // Keep the offset when back to relative position
    }
  });


