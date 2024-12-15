document.addEventListener("DOMContentLoaded", () => {
    const btnActualizarUmbral = document.getElementById("btnActualizarUmbral");
    const graficoConsumo = document.getElementById("graficoConsumo");

    // Función para obtener los datos de consumo y graficarlos
    async function cargarGrafico() {
        const response = await fetch("/api/consumo");
        if (response.ok) {
            const data = await response.json();
            const labels = data.map(item => item[0]); // Fechas
            const values = data.map(item => item[1]); // Cantidades
            new Chart(graficoConsumo, {
                type: "line",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Consumo de Agua",
                        data: values,
                        borderColor: "blue",
                        backgroundColor: "rgba(0, 120, 215, 0.2)"
                    }]
                }
            });
        } else {
            console.error("Error al cargar los datos de consumo.");
        }
    }

    // Función para actualizar el umbral
    btnActualizarUmbral.addEventListener("click", async () => {
        const { value: nuevoUmbral } = await Swal.fire({
            title: "Actualizar Umbral",
            input: "text",
            inputLabel: "Nuevo umbral",
            showCancelButton: true,
            inputValidator: (value) => {
                if (!value) {
                    return "Por favor, escribe un valor.";
                }
            }
        });

        if (nuevoUmbral) {
            const { value: password } = await Swal.fire({
                title: "Ingresa tu contraseña",
                input: "password",
                inputLabel: "Contraseña",
                inputPlaceholder: "Escribe tu contraseña",
                showCancelButton: true,
                inputValidator: (value) => {
                    if (!value) {
                        return "Por favor, escribe una contraseña.";
                    }
                }
            });

            if (password) {
                const response = await fetch("/api/umbral", {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ nuevo_umbral: nuevoUmbral, password: password })
                });

                if (response.ok) {
                    Swal.fire("Éxito", "Umbral actualizado correctamente", "success");
                } else {
                    Swal.fire("Error", "No se pudo actualizar el umbral. Verifica tus datos.", "error");
                }
            }
        }
    });

    // Cargar el gráfico al iniciar
    cargarGrafico();
});
