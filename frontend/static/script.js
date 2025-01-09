document.getElementById("visualizar-btn").addEventListener("click", () => {
    fetch("/visualizar")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("data-container");
            container.innerHTML = JSON.stringify(data.message, null, 2);
        })
        .catch(error => console.error("Error al obtener datos:", error));
});

function fetchAndPlotConsumo(idEsp) {
    fetch(`/consumo?ID_esp=${idEsp}`)
        .then(response => response.json())
        .then(data => {
            if (data.consumo) {
                const timestamps = data.consumo.map(row => row[0]); // Extraer Time_stam
                const consumos = data.consumo.map(row => row[1]); // Extraer Cantidad_agua

                // Actualizar o crear el gráfico
                if (consumoChart) {
                    consumoChart.data.labels = timestamps;
                    consumoChart.data.datasets[0].data = consumos;
                    consumoChart.update();
                } else {
                    consumoChart = new Chart(chartContext, {
                        type: "line",
                        data: {
                            labels: timestamps,
                            datasets: [{
                                label: "Consumo de Agua",
                                data: consumos,
                                borderColor: "rgba(75, 192, 192, 1)",
                                backgroundColor: "rgba(75, 192, 192, 0.2)",
                                borderWidth: 2,
                                tension: 0.4
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                legend: {
                                    position: "top"
                                }
                            },
                            scales: {
                                x: {
                                    title: {
                                        display: true,
                                        text: "Fecha y Hora"
                                    }
                                },
                                y: {
                                    title: {
                                        display: true,
                                        text: "Cantidad de Agua (L)"
                                    }
                                }
                            }
                        }
                    });
                }
            } else {
                console.error("No se encontraron datos de consumo.");
            }
        })
        .catch(error => console.error("Error al obtener datos de consumo:", error));
}

// Llamar a fetchAndPlotConsumo con un ID de ejemplo
fetchAndPlotConsumo(1); // Cambia el "1" por un ID válido para pruebas



document.getElementById("umbral-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const ID_esp = document.getElementById("umbral-id").value;
    const nuevo_umbral = document.getElementById("nuevo-umbral").value;
    const password = document.getElementById("password-umbral").value;

    fetch("/umbral", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ ID_esp, nuevo_umbral, password })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("umbral-status").textContent = data.message || data.detail;
        })
        .catch(error => console.error("Error al actualizar el umbral:", error));
});

document.getElementById("password-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const ID_esp = document.getElementById("password-id").value;
    const nueva_password = document.getElementById("nueva-password").value;

    fetch("/password", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ ID_esp, nueva_password })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("password-status").textContent = data.message || data.detail;
        })
        .catch(error => console.error("Error al actualizar la contraseña:", error));
});
