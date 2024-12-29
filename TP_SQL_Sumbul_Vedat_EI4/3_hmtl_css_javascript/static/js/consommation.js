// static/js/consommation.js

document.addEventListener("DOMContentLoaded", () => {
  console.log("consommation.js chargé - on va afficher un camembert.");

  // 1) Charger la librairie Google Charts
  google.charts.load("current", { packages: ["corechart"] });
  // 2) Quand la lib est prête, exécuter drawConsommation
  google.charts.setOnLoadCallback(drawConsommation);

  function drawConsommation() {
    // Récupérer les données depuis /api/consommation
    fetch("/api/consommation")
      .then(res => res.json())
      .then(data => {
        console.log("Données conso reçues:", data);
        // data = ex. [ {type: "Eau", total: 60.78}, {type: "Électricité", total: 396.01}, ... ]

        // Convertir en tableau format Google Charts
        // ex. [["Type", "Consommation"], ["Eau", 60.78], ["Électricité", 396.01], ...]
        const chartData = [["Type", "Consommation"]];
        data.forEach(item => {
          chartData.push([item.type, item.total]);
        });

        // Transformer en DataTable
        const dataTable = google.visualization.arrayToDataTable(chartData);

        // Options
        const options = {
          title: "Répartition de la Consommation par Type",
          is3D: true,
          pieHole: 0,  // si vous voulez un donut, mettre >0
          width: 800,
          height: 500
        };

        // On dessine le camembert
        const chartContainer = document.getElementById("chart-consommation");
        const chart = new google.visualization.PieChart(chartContainer);
        chart.draw(dataTable, options);
      })
      .catch(err => {
        console.error("Erreur /api/consommation:", err);
      });
  }
});
