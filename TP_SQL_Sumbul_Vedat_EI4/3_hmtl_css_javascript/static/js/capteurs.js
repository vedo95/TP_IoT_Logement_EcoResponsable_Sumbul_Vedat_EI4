// static/js/capteurs.js

document.addEventListener("DOMContentLoaded", () => {
  console.log("capteurs.js - On va afficher le tableau des 20 derniers capteurs");

  const tableBody = document.querySelector("#capteurs-table tbody");

  // Charge le tableau des capteurs
  function loadCapteurs() {
    fetch("/api/capteurs")   // renvoie un JSON des 20 derniers capteurs
      .then(res => res.json())
      .then(data => {
        console.log("Capteurs reçus (20 derniers) :", data);
        tableBody.innerHTML = "";

        data.forEach(capteur => {
          const tr = document.createElement("tr");

          // ID
          const tdId = document.createElement("td");
          tdId.setAttribute("data-label", "ID");
          tdId.textContent = capteur.id;
          tr.appendChild(tdId);

          // Type
          const tdType = document.createElement("td");
          tdType.setAttribute("data-label", "Type");
          tdType.textContent = capteur.type || "N/A";
          tr.appendChild(tdType);

          // Port de Communication
          const tdPort = document.createElement("td");
          tdPort.setAttribute("data-label", "Port de Communication");
          tdPort.textContent = capteur.port_communication || "N/A";
          tr.appendChild(tdPort);

          // Référence Commerciale
          const tdRef = document.createElement("td");
          tdRef.setAttribute("data-label", "Référence Commerciale");
          tdRef.textContent = capteur.reference_commerciale || "N/A";
          tr.appendChild(tdRef);

          // Action (Supprimer)
          const tdAction = document.createElement("td");
          tdAction.setAttribute("data-label", "Action");
          const btnDelete = document.createElement("button");
          btnDelete.textContent = "Supprimer";
          btnDelete.classList.add("delete-btn"); // Ajout de la classe CSS
          btnDelete.dataset.id = capteur.id;

          btnDelete.addEventListener("click", () => {
            if (confirm("Êtes-vous sûr de vouloir supprimer ce capteur?")) {
              fetch(`/api/capteurs/${capteur.id}`, { method: "DELETE" })
                .then(r => r.json())
                .then(result => {
                  console.log("Capteur supprimé :", result);
                  // Recharger la liste
                  loadCapteurs();
                })
                .catch(err => console.error("Erreur lors de la suppression :", err));
            }
          });

          tdAction.appendChild(btnDelete);
          tr.appendChild(tdAction);

          // On ajoute la ligne au tableau
          tableBody.appendChild(tr);
        });
      })
      .catch(err => {
        console.error("Erreur /api/capteurs :", err);
        tableBody.innerHTML = "<tr><td colspan='5'>Erreur lors du chargement des capteurs.</td></tr>";
      });
  }

  // Appel initial pour charger la liste
  loadCapteurs();
});
