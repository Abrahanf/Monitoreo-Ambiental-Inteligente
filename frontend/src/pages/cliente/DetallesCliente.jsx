const fechaHoy = new Date().toLocaleDateString("es-PE", {
  weekday: "long",
  day: "numeric",
  month: "long",
  year: "numeric",
});

function GraficoLinea() {
  return (
    <svg viewBox="0 0 400 140" className="w-full h-36 text-[#0f2b24]">
      <line x1="30" y1="10" x2="30" y2="120" stroke="#c4d6c7" strokeWidth="1" />
      <line x1="30" y1="120" x2="380" y2="120" stroke="#c4d6c7" strokeWidth="1" />
      <polyline
        fill="none"
        stroke="#0f2b24"
        strokeWidth="2"
        points="40,90 80,60 120,70 160,50 200,65 240,80 280,90 320,70 360,60"
      />
    </svg>
  );
}

const METRICAS = [
  { nombre: "Temp promedio", valor: "24 °C", estado: "Normal" },
  { nombre: "Hum promedio", valor: "58%", estado: "Baja" },
  { nombre: "CO₂ promedio", valor: "870 ppm", estado: "Alto" },
  { nombre: "T fuera de rango", valor: "1 h 15 min", estado: "Crítico" },
  { nombre: "Alertas emitidas", valor: "5", estado: "-" },
];

const MAXMIN = [
  { nombre: "Temp máx.", valor: "31 °C", hora: "12 pm" },
  { nombre: "Temp mín.", valor: "19 °C", hora: "3 am" },
  { nombre: "Hum máx.", valor: "87 %", hora: "6 am" },
  { nombre: "Hum mín.", valor: "48 %", hora: "5 pm" },
  { nombre: "CO₂ máx.", valor: "1050 ppm", hora: "7 pm" },
  { nombre: "CO₂ mín.", valor: "480 ppm", hora: "10 am" },
];

export default function DetallesCliente() {
  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-1">
        <span className="text-xs text-gray-500">{fechaHoy}</span>
        <h1 className="text-lg font-semibold text-[#0f2b24]">
          Detalles históricos
        </h1>
      </header>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* GRÁFICOS */}
        <div className="lg:col-span-2 space-y-4">
          <section className="bg-white rounded-lg shadow-sm border border-[#d4e3d7] p-4 space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm font-semibold">
                Temperatura - histórico del día
              </span>
              <select className="border rounded px-3 py-1 text-sm bg-white">
                <option>Temperatura</option>
                <option>Humedad</option>
                <option>CO₂</option>
              </select>
            </div>
            <GraficoLinea />
          </section>

          <section className="bg-white rounded-lg shadow-sm border border-[#d4e3d7] p-4 space-y-3">
            <span className="text-sm font-semibold">
              Predicción para mañana (placeholder IA)
            </span>
            <GraficoLinea />
          </section>
        </div>

        {/* PANEL LATERAL */}
        <aside className="space-y-4">
          <section className="bg-white rounded-lg shadow-sm border border-[#d4e3d7] p-4 text-sm space-y-2">
            <h2 className="font-semibold mb-2">Resumen del periodo</h2>
            <ul className="list-disc list-inside text-gray-700 space-y-1">
              <li>5 alertas de CO₂, alto (5 am, 11 am y 4 pm).</li>
              <li>Confort promedio: 83 %.</li>
              <li>
                Temperatura estable, pero humedad por debajo del rango ideal
                durante 4 h seguidas.
              </li>
              <li>Probabilidad de disconfort mañana al mediodía: Alta.</li>
            </ul>
          </section>

          <section className="bg-white rounded-lg shadow-sm border border-[#d4e3d7] p-4 text-xs space-y-3">
            <h2 className="font-semibold">Métricas</h2>
            <div className="border border-[#e0eee3] rounded">
              <table className="w-full">
                <thead className="bg-[#eaf3ec]">
                  <tr>
                    <th className="px-2 py-1 text-left">Métricas</th>
                    <th className="px-2 py-1 text-left">Valor</th>
                    <th className="px-2 py-1 text-left">Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {METRICAS.map((m) => (
                    <tr key={m.nombre} className="border-t border-[#e0eee3]">
                      <td className="px-2 py-1">{m.nombre}</td>
                      <td className="px-2 py-1">{m.valor}</td>
                      <td className="px-2 py-1">{m.estado}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section className="bg-white rounded-lg shadow-sm border border-[#d4e3d7] p-4 text-xs space-y-3">
            <h2 className="font-semibold">Valores máximos y mínimos actuales</h2>
            <div className="border border-[#e0eee3] rounded">
              <table className="w-full">
                <tbody>
                  {MAXMIN.map((m) => (
                    <tr key={m.nombre} className="border-t border-[#e0eee3]">
                      <td className="px-2 py-1">{m.nombre}</td>
                      <td className="px-2 py-1">{m.valor}</td>
                      <td className="px-2 py-1">{m.hora}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </aside>
      </div>
    </div>
  );
}
