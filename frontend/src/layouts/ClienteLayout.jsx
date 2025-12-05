import { Outlet, Link, useLocation } from "react-router-dom";
import ChatBotButton from "../components/chatbot/ChatBotButton";

export default function ClienteLayout() {
  const user = JSON.parse(localStorage.getItem("user")) || { name: "Cliente" };
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
            to="/cliente/dashboard"
            className={`hover:text-green-400 ${location.pathname.includes("dashboard") ? "text-green-300" : ""}`}
          >
            Inicio
          </Link>
          <Link
            to="/cliente/detalles"
            className={`hover:text-green-400 ${location.pathname.includes("detalles") ? "text-green-300" : ""}`}
          >
            Detalles históricos
          </Link>
          <Link
            to="/cliente/reportes"
            className={`hover:text-green-400 ${location.pathname.includes("reportes") ? "text-green-300" : ""}`}
          >
            Reportes
          </Link>
          <Link
            to="/cliente/perfil"
            className={`hover:text-green-400 ${location.pathname.includes("perfil") ? "text-green-300" : ""}`}
          >
            Perfil
          </Link>
        </nav>
      </aside>

      {/* CONTENIDO */}
      <div className="flex-1 flex flex-col">

        {/* BARRA SUPERIOR */}
        <header className="w-full bg-[#0f2b24] h-12 flex items-center justify-between px-6 shadow-md border-b border-[#13352d]">
          <span className="font-semibold text-lg text-white">{user.name}</span>

          <button
            onClick={() => {
              localStorage.removeItem("user");
              window.location.href = "/login";
            }}
            className="underline hover:text-red-500 text-white"
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
