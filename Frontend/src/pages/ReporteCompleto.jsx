import { useEffect, useState } from "react";
import { obtenerReporteCompleto } from "../api/reportes";

function ReporteCompleto({ setPagina }) {
    const [datos, setDatos] = useState([]);

    useEffect(() => {
        async function cargarReporte() {
            try {
                const data = await obtenerReporteCompleto();
                setDatos(data);
            } catch (error) {
                alert(error.message);
            }
        }

        cargarReporte();
    }, []);

    return (
        <div>
            <h2>Reporte completo</h2>

            <table border="1">
                <thead>
                    <tr>
                        <th>Fecha</th>
                        <th>Temp.</th>
                        <th>Humedad</th>
                        <th>Lluvia</th>
                        <th>Clima</th>
                        <th>Sal vendido</th>
                        <th>Dulce vendido</th>
                        <th>Ingreso</th>
                        <th>Sal producido</th>
                        <th>Dulce producido</th>
                        <th>Sal sobrante</th>
                        <th>Dulce sobrante</th>
                    </tr>
                </thead>

                <tbody>
                    {datos.map((item) => (
                        <tr key={item.fecha}>
                            <td>{item.fecha}</td>
                            <td>{item.temperatura ?? "N/A"} °C</td>
                            <td>{item.humedad ?? "N/A"}%</td>
                            <td>{item.lluvia ? "Sí" : "No"}</td>
                            <td>{item.descripcion_clima}</td>
                            <td>{item.pan_sal_vendido}</td>
                            <td>{item.pan_dulce_vendido}</td>
                            <td>${item.ingreso_total}</td>
                            <td>{item.pan_sal_producido}</td>
                            <td>{item.pan_dulce_producido}</td>
                            <td>{item.pan_sal_sobrante}</td>
                            <td>{item.pan_dulce_sobrante}</td>
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

export default ReporteCompleto;