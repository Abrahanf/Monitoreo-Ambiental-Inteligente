import { NavLink } from "react-router-dom";

export default function SidebarCliente() {
  return (
    <aside className="w-64 min-h-screen bg-[var(--primary)] text-white flex flex-col gap-6 p-6">
      <h2 className="text-2xl font-bold leading-tight">
        Cliente · Monitor <br /> Ambiental
      </h2>

      <nav className="flex flex-col gap-4 mt-4">
        <NavLink
          to="/cliente/dashboard"
          className={({ isActive }) =>
            `block text-lg ${
              isActive ? "text-emerald-300 font-semibold" : "text-white hover:text-emerald-300"
            }`
          }
        >
          Inicio
        </NavLink>

        <NavLink
          to="/cliente/sensores"
          className={({ isActive }) =>
            `block text-lg ${
              isActive ? "text-emerald-300 font-semibold" : "text-white hover:text-emerald-300"
            }`
          }
        >
          Sensores
        </NavLink>

        <NavLink
          to="/cliente/alertas"
          className={({ isActive }) =>
            `block text-lg ${
              isActive ? "text-emerald-300 font-semibold" : "text-white hover:text-emerald-300"
            }`
          }
        >
          Alertas
        </NavLink>

        <NavLink
          to="/cliente/reportes"
          className={({ isActive }) =>
            `block text-lg ${
              isActive ? "text-emerald-300 font-semibold" : "text-white hover:text-emerald-300"
            }`
          }
        >
          Reportes
        </NavLink>

        <NavLink
          to="/cliente/perfil"
          className={({ isActive }) =>
            `block text-lg ${
              isActive ? "text-emerald-300 font-semibold" : "text-white hover:text-emerald-300"
            }`
          }
        >
          Perfil
        </NavLink>
      </nav>
    </aside>
  );
}
