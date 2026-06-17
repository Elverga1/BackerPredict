import { useEffect, useState } from "react";
import { obtenerClimas } from "../api/clima";

function Clima({ setPagina }) {
    const [climas, setClimas] = useState([]);

    useEffect(() => {
        async function cargarClimas() {
            try {
                const data = await obtenerClimas();
                setClimas(data);
            } catch (error) {
                alert(error.message);
            }
        }

        cargarClimas();
    }, []);

    return (
        <div>
            <h2>Historial de clima</h2>

            <table border="1">
                <thead>
                    <tr>
                        <th>Fecha</th>
                        <th>Temperatura</th>
                        <th>Humedad</th>
                        <th>Lluvia</th>
                        <th>Descripción</th>
                    </tr>
                </thead>

                <tbody>
                    {climas.map((clima) => (
                        <tr key={clima.id}>
                            <td>{clima.fecha}</td>
                            <td>{clima.temperatura} °C</td>
                            <td>{clima.humedad}%</td>
                            <td>{clima.lluvia ? "Sí" : "No"}</td>
                            <td>{clima.descripcion}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            <br />

            <button onClick={() => setPagina("dashboard")}>
                Volver al menú
            </button>
        </div>
    );
}

export default Clima;