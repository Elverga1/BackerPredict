import React from "react";
import {useState} from "react";
import {login} from "../api/auth";
import {registrarClimaHoy} from "../api/clima";

function Login({setToken}) {
    const [nombre, setNombre] = useState("");
    const [password, setPassword] = useState("");

    return (
        <div className="login-container">
            <h2>Iniciar sesión</h2>
            <form onSubmit={async (e) => {
                e.preventDefault();
                try {
                    const data = await login(nombre, password);
                    console.log(data);
                    setToken(data.access_token);
                } catch (error) {
                    alert(error.message);
                }
            }}>
                <div className="form-group">
                    <label htmlFor="nombre">Nombre de usuario:</label>
                    <input
                        type="text"
                        id="nombre"
                        value={nombre}
                        onChange={(e) => setNombre(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Contraseña:</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Iniciar sesión</button>
            </form>
        </div>
    );
}
export default Login;