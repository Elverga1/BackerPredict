function Dashboard({setPagina}) {
    const token = localStorage.getItem("token");
    let nombreUsuario = "Usuario";

    if (token) {
        const payload = JSON.parse(atob(token.split(".")[1]));
        nombreUsuario = payload.sub;
}
    return (
        <div className="dashboard-container">
            <h1>BakerPredict</h1>
            <h2>Bienvenido, {nombreUsuario}</h2>
            <p>Panel principal del sistema</p>

            <div className="dashboard-grid">
                <button onClick={() => setPagina("ventas")} className="dashboard-card">
                    <span>Ventas</span>
                    <small>Registrar y consultar ventas</small>
                </button>

                <button onClick={() => setPagina("produccion")} className="dashboard-card">
                    <span>Producción</span>
                    <small>Registrar producción diaria</small>
                </button>

                <button onClick={() => setPagina("reportes")} className="dashboard-card">
                    <span>Reportes</span>
                    <small>Ver resumen general</small>
                </button>
                <button onClick={() => setPagina("clima")} className="dashboard-card">
                    <span>Clima</span>
                    <small>Historial de clima</small>
                </button>
                <button onClick={() => setPagina("reporteCompleto")} className="dashboard-card">
                    <span>Reporte completo</span>
                    <small>Ventas, producción y clima</small>
                </button>
            </div>

            <button
                className="logout-button"
                onClick={() => {
                    localStorage.removeItem("token");
                    window.location.reload();
                }}
            >
                Cerrar sesión
            </button>
        </div>
    );
}

export default Dashboard;