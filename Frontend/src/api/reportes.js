import API_URL from "../services/api";

export async function obtenerReporte() {
    const token = localStorage.getItem("token");

    const response = await fetch(
        `${API_URL}/reportes/resumen`,
        {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    if (!response.ok) {
        throw new Error("Error al obtener reportes");
    }

    return await response.json();
}

export async function obtenerReporteCompleto() {
    const token = localStorage.getItem("token");

    const response = await fetch(`${API_URL}/reportes/completo`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (!response.ok) {
        throw new Error("Error al obtener reporte completo");
    }

    return await response.json();
}