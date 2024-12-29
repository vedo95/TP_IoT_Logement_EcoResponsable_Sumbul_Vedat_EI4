// static/js/configuration.js

document.addEventListener("DOMContentLoaded", () => {
  console.log("configuration.js chargé.");


  //--------------------------------------------------
  // 1) Gestion du tableau des capteurs/actionneurs
  //--------------------------------------------------
  const capteursTableBody = document.querySelector("#capteurs-table tbody");

  function loadCapteurs() {
    fetch("/api/capteurs")
      .then((res) => res.json())
      .then((data) => {
        console.log("Capteurs reçus :", data);
        capteursTableBody.innerHTML = "";

        if (data.length === 0) {
          capteursTableBody.innerHTML = "<tr><td colspan='6'>Aucun capteur trouvé.</td></tr>";
          return;
        }

        data.forEach((capteur) => {
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

          // ID Pièce
          const tdPiece = document.createElement("td");
          tdPiece.setAttribute("data-label", "ID Pièce");
          tdPiece.textContent = capteur.id_piece || "N/A";
          tr.appendChild(tdPiece);

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
                .then((r) => {
                  if (!r.ok) {
                    return r.json().then(errData => { throw new Error(errData.error || 'Erreur lors de la suppression du capteur.'); });
                  }
                  return r.json();
                })
                .then((result) => {
                  if (result.message) {
                    alert(result.message);
                    loadCapteurs();
                  } else if (result.error) {
                    alert(`Erreur: ${result.error}`);
                  }
                })
                .catch((err) => {
                  console.error("Erreur lors de la suppression :", err);
                  alert(`Erreur: ${err.message}`);
                });
            }
          });

          tdAction.appendChild(btnDelete);
          tr.appendChild(tdAction);

          capteursTableBody.appendChild(tr);
        });
      })
      .catch((err) => {
        console.error("Erreur lors du chargement des capteurs :", err);
        capteursTableBody.innerHTML = "<tr><td colspan='6'>Erreur lors du chargement des capteurs.</td></tr>";
      });
  }

  // Charger les capteurs au démarrage
  loadCapteurs();

  //--------------------------------------------------
  // 2) Gestion du Modal d'ajout de capteur/actionneur
  //--------------------------------------------------
  const btnAddCapteur = document.getElementById("btn-add-capteur");
  const modalAddCapteur = document.getElementById("modal-add-capteur");
  const spanCloseCapteur = modalAddCapteur.querySelector(".close");
  const addCapteurForm = document.getElementById("add-capteur-form");

  // Ouvrir le modal d'ajout de capteur/actionneur
  if (btnAddCapteur) {
    btnAddCapteur.addEventListener("click", () => {
      modalAddCapteur.style.display = "block";
    });
  }

  // Fermer le modal d'ajout de capteur/actionneur
  if (spanCloseCapteur) {
    spanCloseCapteur.addEventListener("click", () => {
      modalAddCapteur.style.display = "none";
    });
  }

  // Fermer les modals si clic en dehors
  window.addEventListener("click", (event) => {
    if (event.target == modalAddCapteur) {
      modalAddCapteur.style.display = "none";
    }
    if (event.target == modalAddLogement) {
      modalAddLogement.style.display = "none";
    }
  });

  // Gestion du formulaire d'ajout de capteur/actionneur
  if (addCapteurForm) {
    addCapteurForm.addEventListener("submit", (event) => {
      event.preventDefault();

      const type = document.getElementById("type").value.trim();
      const port_communication = document.getElementById("port_communication").value.trim();
      const reference_commerciale = document.getElementById("reference_commerciale").value.trim();
      const id_piece = document.getElementById("id_piece").value.trim();

      if (!type || !port_communication || !reference_commerciale || !id_piece) {
        alert("Veuillez remplir tous les champs.");
        return;
      }

      // Envoi : POST /api/capteurs
      fetch("/api/capteurs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type, port_communication, reference_commerciale, id_piece }),
      })
        .then((res) => {
          if (!res.ok) {
            return res.json().then(errData => { throw new Error(errData.error || 'Erreur lors de l\'ajout du capteur.'); });
          }
          return res.json();
        })
        .then((data) => {
          if (data.message) {
            alert(data.message);
            modalAddCapteur.style.display = "none";
            addCapteurForm.reset();
            loadCapteurs();
          } else if (data.error) {
            alert(`Erreur: ${data.error}`);
          }
        })
        .catch((err) => {
          console.error("Erreur lors de l'ajout du capteur :", err);
          alert(`Erreur: ${err.message}`);
        });
    });
  }

  //--------------------------------------------------
  // 3) Gestion du tableau des logements
  //--------------------------------------------------
  const logementsTableBody = document.querySelector("#logements-table tbody");

  function loadLogements() {
    fetch("/api/logements")
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log("Logements reçus :", data);
        logementsTableBody.innerHTML = "";

        if (data.length === 0) {
          logementsTableBody.innerHTML = "<tr><td colspan='6'>Aucun logement trouvé.</td></tr>";
          return;
        }

        data.forEach((logement) => {
          const tr = document.createElement("tr");

          // ID
          const tdId = document.createElement("td");
          tdId.setAttribute("data-label", "ID");
          tdId.textContent = logement.id_logement;
          tr.appendChild(tdId);

          // Adresse
          const tdAdresse = document.createElement("td");
          tdAdresse.setAttribute("data-label", "Adresse");
          tdAdresse.textContent = logement.adresse || "N/A";
          tr.appendChild(tdAdresse);

          // Numéro de Téléphone
          const tdNumeroTelephone = document.createElement("td");
          tdNumeroTelephone.setAttribute("data-label", "Numéro de Téléphone");
          tdNumeroTelephone.textContent = logement.numero_telephone || "N/A";
          tr.appendChild(tdNumeroTelephone);

          // Adresse IP
          const tdAdresseIP = document.createElement("td");
          tdAdresseIP.setAttribute("data-label", "Adresse IP");
          tdAdresseIP.textContent = logement.adresse_ip || "N/A";
          tr.appendChild(tdAdresseIP);

          // Date d'Insertion
          const tdDateInsertion = document.createElement("td");
          tdDateInsertion.setAttribute("data-label", "Date d'Insertion");
          tdDateInsertion.textContent = logement.date_insertion || "N/A";
          tr.appendChild(tdDateInsertion);

          // Action (Supprimer)
          const tdAction = document.createElement("td");
          tdAction.setAttribute("data-label", "Action");
          const btnDelete = document.createElement("button");
          btnDelete.textContent = "Supprimer";
          btnDelete.classList.add("delete-btn"); // Ajout de la classe CSS
          btnDelete.dataset.id = logement.id_logement;

          btnDelete.addEventListener("click", () => {
            if (confirm("Êtes-vous sûr de vouloir supprimer ce logement?")) {
              fetch(`/api/logements/${logement.id_logement}`, { method: "DELETE" })
                .then((r) => {
                  if (!r.ok) {
                    return r.json().then(errData => { throw new Error(errData.error || 'Erreur lors de la suppression du logement.'); });
                  }
                  return r.json();
                })
                .then((result) => {
                  if (result.message) {
                    alert(result.message);
                    loadLogements();
                  } else if (result.error) {
                    alert(`Erreur: ${result.error}`);
                  }
                })
                .catch((err) => {
                  console.error("Erreur lors de la suppression :", err);
                  alert(`Erreur: ${err.message}`);
                });
            }
          });

          tdAction.appendChild(btnDelete);
          tr.appendChild(tdAction);

          logementsTableBody.appendChild(tr);
        });
      })
      .catch((err) => {
        console.error("Erreur lors du chargement des logements :", err);
        logementsTableBody.innerHTML = "<tr><td colspan='6'>Erreur lors du chargement des logements.</td></tr>";
      });
  }

  // Charger les logements au démarrage
  loadLogements();

  //--------------------------------------------------
  // 4) Gestion du Modal d'ajout de logement
  //--------------------------------------------------
  const btnAddLogement = document.getElementById("btn-add-logement");
  const modalAddLogement = document.getElementById("modal-add-logement");
  const spanCloseLogement = modalAddLogement.querySelector(".close");
  const addLogementForm = document.getElementById("add-logement-form");

  // Ouvrir le modal d'ajout de logement
  if (btnAddLogement) {
    btnAddLogement.addEventListener("click", () => {
      modalAddLogement.style.display = "block";
    });
  }

  // Fermer le modal d'ajout de logement
  if (spanCloseLogement) {
    spanCloseLogement.addEventListener("click", () => {
      modalAddLogement.style.display = "none";
    });
  }

  // Gestion du formulaire d'ajout de logement
  if (addLogementForm) {
    addLogementForm.addEventListener("submit", (event) => {
      event.preventDefault();

      const adresse = document.getElementById("logement-address").value.trim();
      const numero_telephone = document.getElementById("logement-phone").value.trim();
      const adresse_ip = document.getElementById("logement-ip").value.trim();

      if (!adresse || !numero_telephone || !adresse_ip) {
        alert("Veuillez remplir tous les champs.");
        return;
      }

      // Envoi : POST /api/logements
      fetch("/api/logements", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ adresse, numero_telephone, adresse_ip }),
      })
        .then((res) => {
          if (!res.ok) {
            return res.json().then(errData => { throw new Error(errData.error || 'Erreur lors de l\'ajout du logement.'); });
          }
          return res.json();
        })
        .then((data) => {
          if (data.message) {
            alert(data.message);
            modalAddLogement.style.display = "none";
            addLogementForm.reset();
            loadLogements();
          } else if (data.error) {
            alert(`Erreur: ${data.error}`);
          }
        })
        .catch((err) => {
          console.error("Erreur lors de l'ajout du logement :", err);
          alert(`Erreur: ${err.message}`);
        });
    });
  }
});
