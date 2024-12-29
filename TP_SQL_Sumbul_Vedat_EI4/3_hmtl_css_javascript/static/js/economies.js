document.addEventListener("DOMContentLoaded", () => {
  google.charts.load('current', { packages: ['corechart'] });
  google.charts.setOnLoadCallback(setupUI);

  function setupUI() {
    // Attacher l'événement sur le bouton
    const btnLoad = document.getElementById("btn-load");
    btnLoad.addEventListener("click", () => {
      const select = document.getElementById("scale-select");
      const scale = select.value; // "Mensuel" ou "Annuel"
      drawEconomiesChart(scale);  // on appelle la fonction d'affichage
    });

    // On dessine un premier graphique par défaut
    drawEconomiesChart("Mensuel");
  }

  function drawEconomiesChart(scale) {
    fetch(`/api/economies?scale=${scale}`)
      .then(response => response.json())
      .then(data => {
        console.log("Données économies reçues :", data);
        // Construction du tableau pour Google Charts
        const chartData = [["Type", "Économie"]];
        data.forEach(item => {
          chartData.push([item.type, item.economie || item.total || 0]);
        });

        const dataTable = google.visualization.arrayToDataTable(chartData);
        const options = {
          title: `Économies Réalisées (${scale})`,
          hAxis: { title: "Montant économisé en € " },
          vAxis: { title: "Type" },
          legend: { position: "right" }
        };

        const chartContainer = document.getElementById("chart-economies");
        const chart = new google.visualization.BarChart(chartContainer);
        chart.draw(dataTable, options);
      })
      .catch(err => {
        console.error("Erreur lors de /api/economies :", err);
      });
  }
});
