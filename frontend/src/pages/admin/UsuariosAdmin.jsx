const fechaHoy = new Date().toLocaleDateString("es-PE", {
  weekday: "long",
  day: "numeric",
  month: "long",
  year: "numeric",
});

const USUARIOS = [
  {
    nombre: "Carlos",
    correo: "carlos@gmail.com",
    ubicacion: "Zona A",
    estado: "Activo",
    ultimo: "2025-10-13 10:30",
    inicio: "2022-06-10",
  },
  {
    nombre: "María",
    correo: "maria@gmail.com",
    ubicacion: "Zona B",
    estado: "Activo",
    ultimo: "2025-10-13 10:30",
    inicio: "2022-06-10",
  },
  {
    nombre: "Juan",
    correo: "juan@gmail.com",
    ubicacion: "Zona C",
    estado: "Activo",
    ultimo: "2025-10-13 10:30",
    inicio: "2022-06-10",
  },
];

export default function UsuariosAdmin() {
  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-1">
        <span className="text-xs text-gray-500">{fechaHoy}</span>
        <h1 className="text-lg font-semibold text-[#0f2b24]">Usuarios</h1>
      </header>

      {/* TABLA PRINCIPAL */}
      <section className="bg-white rounded-lg shadow-sm border border-[#d4e3d7] overflow-hidden">
        <div className="flex justify-between items-center px-4 py-3">
          <span className="font-semibold text-sm">Usuarios</span>
          <button className="px-3 py-1 text-xs rounded bg-[#7ebc89] text-[#0f2b24]">
            Agregar usuario
          </button>
        </div>
        <table className="w-full text-sm">
          <thead className="bg-[#eaf3ec] text-left text-gray-700">
            <tr>
              <th className="px-4 py-2">Nombre</th>
              <th className="px-4 py-2">Correo</th>
              <th className="px-4 py-2">Contraseña</th>
              <th className="px-4 py-2">Ubicación asignada</th>
              <th className="px-4 py-2">Estado</th>
              <th className="px-4 py-2">Último acceso</th>
              <th className="px-4 py-2">Fecha de inicio</th>
              <th className="px-4 py-2 text-right">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {USUARIOS.map((u) => (
              <tr key={u.correo} className="border-t border-[#e0eee3]">
                <td className="px-4 py-2">{u.nombre}</td>
                <td className="px-4 py-2">{u.correo}</td>
                <td className="px-4 py-2">********</td>
                <td className="px-4 py-2">{u.ubicacion}</td>
                <td className="px-4 py-2">{u.estado}</td>
                <td className="px-4 py-2">{u.ultimo}</td>
                <td className="px-4 py-2">{u.inicio}</td>
                <td className="px-4 py-2 text-right space-x-2">
                  <button className="px-3 py-1 text-xs rounded bg-[#7ebc89] text-[#0f2b24]">
                    Editar
                  </button>
                  <button className="px-3 py-1 text-xs rounded bg-yellow-100 text-yellow-700">
                    Bloquear
                  </button>
                  <button className="px-3 py-1 text-xs rounded bg-red-100 text-red-700">
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      {/* MENSAJES / SOLICITUDES */}
      <section className="bg-white rounded-lg shadow-sm border border-[#d4e3d7] overflow-hidden">
        <div className="px-4 py-3 border-b border-[#e0eee3]">
          <span className="font-semibold text-sm">Mensajes</span>
        </div>

        <table className="w-full text-sm">
          <thead className="bg-[#eaf3ec] text-left text-gray-700">
            <tr>
              <th className="px-4 py-2">Nombre</th>
              <th className="px-4 py-2">Correo</th>
              <th className="px-4 py-2">Mensaje</th>
              <th className="px-4 py-2">Nueva contraseña</th>
              <th className="px-4 py-2">Verificación</th>
              <th className="px-4 py-2 text-right">Acción</th>
            </tr>
          </thead>
          <tbody>
            <tr className="border-t border-[#e0eee3]">
              <td className="px-4 py-2">Carlos</td>
              <td className="px-4 py-2">carlos@gmail.com</td>
              <td className="px-4 py-2">cambio de contraseña</td>
              <td className="px-4 py-2">********</td>
              <td className="px-4 py-2">
                <input
                  type="text"
                  className="border rounded px-2 py-1 text-xs w-32"
                  placeholder="ingrese número"
                />
              </td>
              <td className="px-4 py-2 text-right">
                <button className="px-3 py-1 text-xs rounded bg-[#7ebc89] text-[#0f2b24]">
                  Atender
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>
  );
}
