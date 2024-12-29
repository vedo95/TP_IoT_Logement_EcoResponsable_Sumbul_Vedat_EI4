// static/js/meteo.js

document.addEventListener("DOMContentLoaded", () => {
  console.log("meteo.js - On va charger la météo via /meteo/<city> dans un iframe.");

  const form = document.getElementById("meteo-form");
  const cityInput = document.getElementById("city-input");
  const iframe = document.getElementById("meteo-iframe");

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const city = cityInput.value.trim();
    if (!city) return;

    // On construit l'URL /meteo/<city>
    const url = `/meteo/${encodeURIComponent(city)}`;
    // On l'affiche dans l'iframe
    iframe.src = url;
  });
});
