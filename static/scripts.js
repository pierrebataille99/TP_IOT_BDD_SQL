document.addEventListener('DOMContentLoaded', () => {
    console.log('Site chargé avec succès!');

    const dropdownToggle = document.querySelector('.dropdown-toggle');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    if (dropdownToggle && dropdownMenu) {
        dropdownToggle.addEventListener('click', (event) => {
            event.preventDefault();
            // Afficher ou masquer le menu
            dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
        });
    } else {
        console.error('Menu déroulant introuvable.');
    }
});




document.addEventListener('DOMContentLoaded', () => {
    // Détecte la page active
    const currentPage = document.body.getAttribute('data-page'); // Attribut `data-page`

    // Actualise le contenu toutes les secondes
    setInterval(() => {
        if (currentPage === 'capteurs') {
            updateCapteurs();
        } else if (currentPage === 'consommation') {
            updateConsommation();
        } else if (currentPage === 'meteo') {
            updateMeteo();
        } else if (currentPage === 'gestion') {
            updateGestion();
        } else if (currentPage === 'données_bdd') {
            updateDonneesBDD();
        } else if (currentPage === 'graphique_capteur') {
            updateGraphiqueCapteur();
        }
    }, 1000); // Intervalle : 1 seconde

    // Fonction pour mettre à jour les capteurs
    function updateCapteurs() {
        fetch('/capteur/LOG001')
            .then(response => response.json())
            .then(data => {
                const sensorContainer = document.querySelector('.sensor-list');
                sensorContainer.innerHTML = '';
                data.forEach(capteur => {
                    sensorContainer.innerHTML += `
                        <div class="sensor-item">
                            <h2>${capteur.nom_capteur}</h2>
                            <p><strong>ID :</strong> ${capteur.id}</p>
                            <p><strong>Pièce :</strong> ${capteur.nom_piece}</p>
                            <p><strong>Unité de mesure :</strong> ${capteur.unite_mesure}</p>
                            <a href="/graphique_capteur/${capteur.id}">Voir le graphique du capteur</a>
                        </div>
                    `;
                });
            })
            .catch(error => console.error('Erreur lors de la mise à jour des capteurs :', error));
    }

    // Fonction pour mettre à jour les consommations
    function updateConsommation() {
        fetch('/consommation/LOG001')
            .then(response => response.json())
            .then(data => {
                const consommationTable = document.querySelector('table tbody');
                consommationTable.innerHTML = '';
                data.forEach(item => {
                    consommationTable.innerHTML += `
                        <tr>
                            <td>${item.type}</td>
                            <td>${item.valeur}</td>
                            <td>${item.unite}</td>
                            <td>${item.prix}</td>
                        </tr>
                    `;
                });
            })
            .catch(error => console.error('Erreur lors de la mise à jour des consommations :', error));
    }

    // Fonction pour mettre à jour la météo
    function updateMeteo() {
        fetch('/meteo/rueil-malmaison')
            .then(response => response.json())
            .then(data => {
                const forecastContainer = document.querySelector('.forecast-container');
                forecastContainer.innerHTML = '';
                Object.keys(data).forEach(day => {
                    forecastContainer.innerHTML += `
                        <div class="day-forecast">
                            <h2>${day}</h2>
                            <ul class="hourly-forecast">
                                ${data[day].map(forecast => `
                                    <li>
                                        <div class="hourly-time">${forecast.time}</div>
                                        <div class="hourly-temp">${forecast.temperature}°C</div>
                                        <div class="hourly-desc">${forecast.description}</div>
                                    </li>
                                `).join('')}
                            </ul>
                        </div>
                    `;
                });
            })
            .catch(error => console.error('Erreur lors de la mise à jour de la météo :', error));
    }

    // Fonction pour mettre à jour la gestion
    function updateGestion() {
        fetch('/gestion/LOG001')
            .then(response => response.text())
            .then(html => {
                document.querySelector('main').innerHTML = html;
            })
            .catch(error => console.error('Erreur lors de la mise à jour de la gestion :', error));
    }

    // Fonction pour mettre à jour les données BDD
    function updateDonneesBDD() {
        fetch('/données_bdd')
            .then(response => response.text())
            .then(html => {
                document.querySelector('main').innerHTML = html;
            })
            .catch(error => console.error('Erreur lors de la mise à jour des données BDD :', error));
    }

    // Fonction pour mettre à jour le graphique du capteur
    function updateGraphiqueCapteur() {
        const capteurId = window.location.pathname.split('/').pop();
        fetch(`/graphique_capteur/${capteurId}`)
            .then(response => response.text())
            .then(html => {
                document.querySelector('main').innerHTML = html;
            })
            .catch(error => console.error('Erreur lors de la mise à jour du graphique du capteur :', error));
    }
});
