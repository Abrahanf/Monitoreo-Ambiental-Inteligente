import { Outlet, Link, useLocation } from "react-router-dom";
import ChatBotButton from "../components/chatbot/ChatBotButton";

export default function AdminLayout() {
  const user = JSON.parse(localStorage.getItem("user")) || { name: "Admin" };
  const location = useLocation();

  return (
    <div className="flex bg-[#0f2b24] min-h-screen text-white">

      {/* SIDEBAR */}
      <aside className="w-64 bg-[#0f2b24] p-6 space-y-6 border-r border-[#13352d]">
        <h2 className="text-2xl font-bold leading-tight">
          Monitoreo y análisis <br /> ambiental
        </h2>

        <nav className="flex flex-col space-y-4 text-lg mt-4">
          <Link
            to="/admin/dashboard"
            className={`hover:text-green-400 ${location.pathname.includes("dashboard") ? "text-green-300" : ""}`}
          >
            Dashboard
          </Link>
          <Link
            to="/admin/config-nodos"
            className={`hover:text-green-400 ${location.pathname.includes("config-nodos") ? "text-green-300" : ""}`}
          >
            Configuración de nodos
          </Link>
          <Link
            to="/admin/config-senales"
            className={`hover:text-green-400 ${location.pathname.includes("config-senales") ? "text-green-300" : ""}`}
          >
            Configuración de señales
          </Link>
          <Link
            to="/admin/users"
            className={`hover:text-green-400 ${location.pathname.includes("users") ? "text-green-300" : ""}`}
          >
            Usuarios
          </Link>
          <Link
            to="/admin/modelo-ia"
            className={`hover:text-green-400 ${location.pathname.includes("modelo-ia") ? "text-green-300" : ""}`}
          >
            Modelo IA
          </Link>
        </nav>
      </aside>

      {/* CONTENIDO */}
      <div className="flex-1 flex flex-col">

        {/* BARRA SUPERIOR */}
        <header className="w-full bg-[#0f2b24] h-12 flex items-center justify-between px-6 text-white font-medium shadow-md border-b border-[#13352d]">
          <span className="font-semibold text-lg">Bienvenido, {user.name}</span>

          <button
            onClick={() => {
              localStorage.removeItem("user");
              window.location.href = "/login";
            }}
            className="underline hover:text-red-500"
          >
            Cerrar sesión
          </button>
        </header>

        {/* CONTENIDO DE PÁGINA */}
        <main className="flex-1 bg-[#eaf3ec] text-black p-10 overflow-auto relative">
          <Outlet />
          <ChatBotButton />
        </main>
      </div>
    </div>
  );
}
