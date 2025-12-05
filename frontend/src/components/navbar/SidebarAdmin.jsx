import { NavLink } from "react-router-dom";

export default function SidebarAdmin() {
  return (
    <aside className="w-64 min-h-screen bg-[var(--primary)] text-white flex flex-col gap-6 p-6">
      <h2 className="text-2xl font-bold leading-tight">
        Admin · Monitor <br /> Ambiental
      </h2>

      <nav className="flex flex-col gap-4 mt-4">
        <NavLink
          to="/admin/dashboard"
          className={({ isActive }) =>
            `block text-lg ${
              isActive ? "text-emerald-300 font-semibold" : "text-white hover:text-emerald-300"
            }`
          }
        >
          Dashboard
        </NavLink>

        <NavLink
          to="/admin/usuarios"
          className={({ isActive }) =>
            `block text-lg ${isActive ? "text-emerald-300 font-semibold" : "text-white"}`
          }
        >
          Usuarios
        </NavLink>

        <NavLink
          to="/admin/sensores"
          className={({ isActive }) =>
            `block text-lg ${isActive ? "text-emerald-300 font-semibold" : "text-white"}`
          }
        >
          Sensores
        </NavLink>

        <NavLink
          to="/admin/alertas"
          className={({ isActive }) =>
            `block text-lg ${isActive ? "text-emerald-300 font-semibold" : "text-white"}`
          }
        >
          Alertas
        </NavLink>

        <NavLink
          to="/admin/reportes"
          className={({ isActive }) =>
            `block text-lg ${isActive ? "text-emerald-300 font-semibold" : "text-white"}`
          }
        >
          Reportes
        </NavLink>
      </nav>
    </aside>
  );
}
