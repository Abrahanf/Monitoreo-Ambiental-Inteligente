const fechaHoy = new Date().toLocaleDateString("es-PE", {
  weekday: "long",
  day: "numeric",
  month: "long",
  year: "numeric",
});

const ALERTAS = [
  {
    fecha: "13/10/2025 11:00",
    tipo: "CO₂",
    valor: "890 ppm",
    umbral: "> 800",
    severidad: "Crítica",
    estado: "Activa",
  },
  {
    fecha: "13/10/2025 15:30",
    tipo: "Temperatura",
    valor: "31 °C",
    umbral: "18 <> 30",
    severidad: "Media",
    estado: "Activa",
  },
  {
    fecha: "14/10/2025 09:15",
    tipo: "Humedad",
    valor: "40 %",
    umbral: "45 % <> 70 %",
    severidad: "Leve",
    estado: "Pendiente",
  },
];

export default function ReportesCliente() {
  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-1">
        <span className="text-xs text-gray-500">{fechaHoy}</span>
        <h1 className="text-lg font-semibold text-[#0f2b24]">Reportes</h1>
      </header>

      <section className="bg-white rounded-lg shadow-sm border border-[#d4e3d7] p-4 space-y-4">
        {/* FILTROS */}
        <div className="flex flex-wrap gap-3 items-center text-sm">
          <span className="text-gray-700 mr-2">Rango de fecha</span>
          <input
            type="date"
            className="border rounded px-2 py-1 text-sm bg-white"
          />
          <span>-</span>
          <input
            type="date"
            className="border rounded px-2 py-1 text-sm bg-white"
          />

          <select className="border rounded px-3 py-1 text-sm bg-white ml-4">
            <option>Tipo de alerta</option>
            <option>Temperatura</option>
            <option>Humedad</option>
            <option>CO₂</option>
          </select>

          <select className="border rounded px-3 py-1 text-sm bg-white">
            <option>Nivel de severidad</option>
            <option>Crítica</option>
            <option>Media</option>
            <option>Leve</option>
          </select>
        </div>

        {/* TABLA */}
        <div className="border border-[#d4e3d7] rounded overflow-hidden text-sm">
          <table className="w-full">
            <thead className="bg-[#eaf3ec] text-left text-gray-700">
              <tr>
                <th className="px-4 py-2">Fecha y hora</th>
                <th className="px-4 py-2">Tipo</th>
                <th className="px-4 py-2">Valor</th>
                <th className="px-4 py-2">Umbral</th>
                <th className="px-4 py-2">Severidad</th>
                <th className="px-4 py-2">Estado</th>
              </tr>
            </thead>
            <tbody>
              {ALERTAS.map((a, i) => (
                <tr key={i} className="border-t border-[#e0eee3]">
                  <td className="px-4 py-2">{a.fecha}</td>
                  <td className="px-4 py-2">{a.tipo}</td>
                  <td className="px-4 py-2">{a.valor}</td>
                  <td className="px-4 py-2">{a.umbral}</td>
                  <td className="px-4 py-2">{a.severidad}</td>
                  <td className="px-4 py-2">{a.estado}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* BOTONES DESCARGA */}
        <div className="flex justify-end gap-3 mt-3">
          <button className="px-4 py-2 text-sm rounded bg-gray-100 text-gray-700">
            PDF
          </button>
          <button className="px-4 py-2 text-sm rounded bg-gray-100 text-gray-700">
            CSV
          </button>
        </div>
      </section>
    </div>
  );
}
