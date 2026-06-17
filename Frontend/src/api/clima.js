import API_URL from "../services/api";

export async function obtenerClimas() {
    const token = localStorage.getItem("token");

    const response = await fetch(`${API_URL}/clima/`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (!response.ok) {
        throw new Error("Error al obtener historial de clima");
    }

    return await response.json();
}