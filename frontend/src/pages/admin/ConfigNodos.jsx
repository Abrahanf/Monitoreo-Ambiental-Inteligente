const fechaHoy = new Date().toLocaleDateString("es-PE", {
  weekday: "long",
  day: "numeric",
  month: "long",
  year: "numeric",
});

const NODOS = [
  {
    tag: "MA_A01",
    zona: "Zona A",
    mcu: "ESP32",
    vel: "1 min",
    estado: "ON",
    fecha: "13-10-2025",
  },
  {
    tag: "MA_B01",
    zona: "Zona B",
    mcu: "ESP32",
    vel: "1 min",
    estado: "ON",
    fecha: "13-10-2025",
  },
  {
    tag: "MA_C01",
    zona: "Zona C",
    mcu: "ESP32",
    vel: "1 min",
    estado: "ON",
    fecha: "13-10-2025",
  },
];

export default function ConfigNodos() {
  return (
    <div className="space-y-4">
      <header className="flex flex-col gap-1">
        <span className="text-xs text-gray-500">{fechaHoy}</span>
        <h1 className="text-lg font-semibold text-[#0f2b24]">Nodos</h1>
      </header>

      <div className="bg-white rounded-lg shadow-sm border border-[#d4e3d7] overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-[#eaf3ec] text-left text-gray-700">
            <tr>
              <th className="px-4 py-2">Tag del nodo</th>
              <th className="px-4 py-2">Ubicación</th>
              <th className="px-4 py-2">Microcontrolador</th>
              <th className="px-4 py-2">Velocidad de envío de datos</th>
              <th className="px-4 py-2">Estado</th>
              <th className="px-4 py-2">Fecha de registro</th>
              <th className="px-4 py-2 text-right">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {NODOS.map((n) => (
              <tr key={n.tag} className="border-t border-[#e0eee3]">
                <td className="px-4 py-2">{n.tag}</td>
                <td className="px-4 py-2">{n.zona}</td>
                <td className="px-4 py-2">{n.mcu}</td>
                <td className="px-4 py-2">{n.vel}</td>
                <td className="px-4 py-2">{n.estado}</td>
                <td className="px-4 py-2">{n.fecha}</td>
                <td className="px-4 py-2 text-right space-x-2">
                  <button className="px-3 py-1 text-xs rounded bg-[#7ebc89] text-[#0f2b24]">
                    Editar
                  </button>
                  <button className="px-3 py-1 text-xs rounded bg-red-100 text-red-700">
                    Eliminar
                  </button>
                  <button className="px-3 py-1 text-xs rounded bg-gray-100 text-gray-700">
                    Ver
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
