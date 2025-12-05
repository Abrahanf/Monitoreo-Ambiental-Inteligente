export default function PerfilCliente() {
  const user = JSON.parse(localStorage.getItem("user")) || {
    name: "Cliente",
    email: "cliente@icc.com",
  };

  return (
    <div className="space-y-6">
      <h1 className="text-lg font-semibold text-[#0f2b24]">Perfil</h1>

      <section className="bg-white rounded-lg shadow-sm border border-[#d4e3d7] p-6 max-w-xl">
        <h2 className="text-lg font-semibold mb-4 text-[#0f2b24]">Mi Perfil</h2>

        <div className="space-y-2 text-sm text-gray-800">
          <p>
            <span className="font-semibold mr-2">Nombre:</span>
            {user.name}
          </p>
          <p>
            <span className="font-semibold mr-2">Correo:</span>
            {user.email || "cliente@icc.com"}
          </p>
        </div>

        <button
          onClick={() => {
            localStorage.removeItem("user");
            window.location.href = "/login";
          }}
          className="mt-6 px-4 py-2 rounded bg-[#ff7b7b] text-white font-semibold"
        >
          Cerrar sesión
        </button>
      </section>
    </div>
  );
}
