import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api"; // <--- 1. IMPORTAR TU INSTANCIA DE AXIOS

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [showPass, setShowPass] = useState(false);

  // 2. HACER LA FUNCIÓN ASÍNCRONA (ASYNC)
  const handleLogin = async (e) => {
    e.preventDefault();
    setError(null); // Limpiar errores previos

    try {
      // 3. LLAMADA REAL AL BACKEND
      const response = await api.post("/auth/login", {
        correo: email,       // El backend espera 'correo'
        contrasena: password // El backend espera 'contrasena' (sin ñ)
      });

      // 4. SI LLEGA AQUÍ, EL LOGIN FUE EXITOSO (CÓDIGO 200)
      const { access_token, user } = response.data;

      // 5. GUARDAR TOKEN Y USUARIO
      localStorage.setItem("token", access_token);
      localStorage.setItem("user", JSON.stringify(user));

      // 6. REDIRECCIÓN SEGÚN ROL
      // Nota: Tu backend guarda el rol como 'administrador', no 'admin'.
      // Ajustamos la condición para que detecte ambos por si acaso.
      if (user.rol === "administrador" || user.rol === "admin") {
        navigate("/admin/dashboard");
      } else {
        navigate("/cliente/dashboard"); // O la ruta de usuario que tengas
      }

    } catch (err) {
      // 7. MANEJO DE ERRORES REALES
      console.error("Login fallido:", err);
      if (err.response && err.response.data) {
        // Error que viene del backend (ej: "Correo inválido")
        setError(err.response.data.error || "Credenciales incorrectas");
      } else {
        // Error de conexión (Backend apagado)
        setError("No se pudo conectar con el servidor");
      }
    }
  };

  return (
    <div className="min-h-screen bg-[#0f2b24] flex items-center justify-center px-4">
      <form
        onSubmit={handleLogin}
        className="bg-[#eaf3ec] p-10 rounded-3xl w-full max-w-md shadow text-center"
      >
        <h1 className="text-3xl font-bold text-[#0f2b24] mb-6">Log in</h1>

        {/* Muestra el error si existe */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded relative mb-4 text-sm">
            {error}
          </div>
        )}

        {/* USERNAME / EMAIL */}
        <input
          type="email" 
          placeholder="Correo electrónico" // Cambiado a Correo para ser claro
          className="w-full p-3 border border-gray-300 rounded-md bg-white placeholder-gray-500 text-[#0f2b24]"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        {/* PASSWORD */}
        <div className="relative mt-4">
          <input
            type={showPass ? "text" : "password"}
            placeholder="Password"
            className="w-full p-3 border border-gray-300 rounded-md bg-white placeholder-gray-500 text-[#0f2b24]"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button
            type="button"
            onClick={() => setShowPass(!showPass)}
            className="absolute right-3 top-2 text-gray-600 text-xl select-none focus:outline-none"
          >
            {showPass ? "👁️" : "🙈"}
          </button>
        </div>

        <a
          href="/recover"
          className="block mt-2 text-xs text-[#0f2b24] underline text-left"
        >
          olvidé mi contraseña
        </a>

        <button
          type="submit"
          className="w-full bg-[#7ebc89] mt-6 py-2 rounded-md text-[#0f2b24] font-bold hover:bg-[#69a574] transition duration-200"
        >
          Log in
        </button>

        <p className="mt-4 text-sm text-[#0f2b24]">
          or, <a href="/signup" className="underline">sign up</a>
        </p>
      </form>
    </div>
  );
}