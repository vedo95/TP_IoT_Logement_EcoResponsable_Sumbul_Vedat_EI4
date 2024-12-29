// static/js/main.js
document.addEventListener("DOMContentLoaded", () => {
  const burgerBtn = document.getElementById("burger-menu");
  const navList = document.getElementById("nav-list");

  if (burgerBtn) {
    burgerBtn.addEventListener("click", () => {
      // Toggle l’affichage du menu
      navList.classList.toggle("open");
    });
  }
});
