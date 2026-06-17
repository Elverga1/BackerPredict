import {useState} from "react";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Ventas from "./pages/Ventas";
import Produccion from "./pages/Produccion";
import Reportes from "./pages/Reportes";
import Clima from "./pages/Clima";

function App() {
    const [token, setToken] = useState(
        localStorage.getItem("token")
    );

    const [pagina, setPagina] = useState("dashboard");

    if (!token) {
        return <Login />;
    }
    if (pagina === "ventas") {
        return <Ventas setPagina={setPagina} />;
    }
    if (pagina === "produccion") {
        return <Produccion setPagina={setPagina} />;
    }
    if (pagina === "reportes") {
    return <Reportes setPagina={setPagina} />;
    } 
    if (pagina === "clima") {
        return <Clima setPagina={setPagina} />;
    }
    return <Dashboard setPagina={setPagina} />;
}

export default App;