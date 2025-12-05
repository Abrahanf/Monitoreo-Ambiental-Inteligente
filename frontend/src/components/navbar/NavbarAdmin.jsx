// src/components/navbar/NavbarAdmin.jsx
export default function NavbarAdmin() {
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  const nombre = user?.nombre || "Administrador";

  const handleLogout = () => {
    localStorage.removeItem("user");
    window.location.href = "/login";
  };

  return (
    <header className="h-14 bg-[#134235] text-white flex items-center justify-between px-6 text-sm">
      <div className="flex items-center gap-3">
        <span className="font-semibold">
          Monitoreo y análisis ambiental
        </span>
        <span className="text-white/70">|</span>
        <span className="text-white/80">Panel administrador</span>
        <span className="text-white/70">|</span>
        <span className="font-medium">{nombre}</span>
      </div>

      <button
        onClick={handleLogout}
        className="text-xs font-semibold px-3 py-1 rounded bg-[#2e7d5a] hover:bg-[#3fa06f]"
      >
        Cerrar sesión
      </button>
    </header>
  );
}
