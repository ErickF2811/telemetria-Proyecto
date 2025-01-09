document.getElementById("visualizar-btn").addEventListener("click", () => {
    fetch("/visualizar")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("data-container");
            container.innerHTML = JSON.stringify(data.message, null, 2);
        })
        .catch(error => console.error("Error al obtener datos:", error));
});

// Selecciona el canvas y define el contexto
const chartCanvas = document.getElementById("consumo-chart");
const chartContext = chartCanvas.getContext("2d");

// Variable global para el gráfico
let consumoChart;

// Intervalo para actualizar automáticamente
let autoUpdateInterval;

// Evento para enviar el formulario y obtener los datos
document.getElementById("rango-fechas-form").addEventListener("submit", (e) => {
    e.preventDefault(); // Evita el comportamiento predeterminado del formulario

    const ID_esp = document.getElementById("rango-id").value;
    const fechaInicio = document.getElementById("fecha-inicio").value;
    const fechaFin = document.getElementById("fecha-fin").value;

    // Función para obtener y actualizar datos
    const fetchAndUpdate = () => {
        fetch(`/consumo?ID_esp=${ID_esp}&fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`)
            .then((response) => response.json())
            .then((data) => {
                if (data.consumo) {
                    const timestamps = data.consumo.map((row) => row.Time_stam);
                    const consumos = data.consumo.map((row) => row.Cantidad_agua);

                    // Si el gráfico ya existe, actualízalo
                    if (consumoChart) {
                        consumoChart.data.labels = timestamps;
                        consumoChart.data.datasets[0].data = consumos;
                        consumoChart.update();
                    } else {
                        // Si no existe, crea un nuevo gráfico
                        consumoChart = new Chart(chartContext, {
                            type: "line",
                            data: {
                                labels: timestamps,
                                datasets: [
                                    {
                                        label: "Consumo de Agua",
                                        data: consumos,
                                        borderColor: "rgba(75, 192, 192, 1)",
                                        backgroundColor: "rgba(75, 192, 192, 0.2)",
                                        borderWidth: 2,
                                        tension: 0.4,
                                    },
                                ],
                            },
                            options: {
                                responsive: true,
                                plugins: {
                                    legend: {
                                        position: "top",
                                    },
                                },
                                scales: {
                                    x: {
                                        title: {
                                            display: true,
                                            text: "Fecha y Hora",
                                        },
                                    },
                                    y: {
                                        title: {
                                            display: true,
                                            text: "Cantidad de Agua (L)",
                                        },
                                    },
                                },
                            },
                        });
                    }
                } else {
                    console.error("No se encontraron datos en el rango especificado.");
                }
            })
            .catch((error) => console.error("Error al actualizar datos:", error));
    };

    // Llama a la función para obtener datos y configurar actualizaciones automáticas
    fetchAndUpdate();

    // Configura el intervalo para actualizar automáticamente cada 5 segundos
    clearInterval(autoUpdateInterval);
    autoUpdateInterval = setInterval(fetchAndUpdate, 5000); // Ajusta el tiempo según sea necesario
});


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
