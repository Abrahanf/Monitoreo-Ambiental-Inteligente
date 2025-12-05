const fechaHoy = new Date().toLocaleDateString("es-PE", {
  weekday: "long",
  day: "numeric",
  month: "long",
  year: "numeric",
});

const SENALES = [
  {
    tag: "MA_A01",
    zona: "Zona A",
    sensor: "DHT22",
    variable: "Temperatura",
    umbralMin: "18 °C",
    umbralMax: "28 °C",
    vel: "2 s",
    estado: "ON",
  },
  {
    tag: "MA_A01",
    zona: "Zona A",
    sensor: "DHT22",
    variable: "Humedad",
    umbralMin: "30 %",
    umbralMax: "60 %",
    vel: "2 s",
    estado: "ON",
  },
  {
    tag: "MA_A01",
    zona: "Zona A",
    sensor: "MQ-135",
    variable: "CO2",
    umbralMin: "400 ppm",
    umbralMax: "1001 ppm",
    vel: "2 s",
    estado: "ON",
  },
];

export default function ConfigSenales() {
  return (
    <div className="space-y-4">
      <header className="flex flex-col gap-1">
        <span className="text-xs text-gray-500">{fechaHoy}</span>
        <h1 className="text-lg font-semibold text-[#0f2b24]">Señales</h1>
      </header>

      <div className="bg-white rounded-lg shadow-sm border border-[#d4e3d7] overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-[#eaf3ec] text-left text-gray-700">
            <tr>
              <th className="px-4 py-2">Tag del nodo</th>
              <th className="px-4 py-2">Ubicación</th>
              <th className="px-4 py-2">Sensor</th>
              <th className="px-4 py-2">Variable</th>
              <th className="px-4 py-2">Umbral min</th>
              <th className="px-4 py-2">Umbral máx</th>
              <th className="px-4 py-2">Velocidad de muestreo</th>
              <th className="px-4 py-2">Estado del sensor</th>
              <th className="px-4 py-2 text-right">Acción</th>
            </tr>
          </thead>
          <tbody>
            {SENALES.map((s, i) => (
              <tr key={i} className="border-t border-[#e0eee3]">
                <td className="px-4 py-2">{s.tag}</td>
                <td className="px-4 py-2">{s.zona}</td>
                <td className="px-4 py-2">{s.sensor}</td>
                <td className="px-4 py-2">{s.variable}</td>
                <td className="px-4 py-2">{s.umbralMin}</td>
                <td className="px-4 py-2">{s.umbralMax}</td>
                <td className="px-4 py-2">{s.vel}</td>
                <td className="px-4 py-2">{s.estado}</td>
                <td className="px-4 py-2 text-right">
                  <button className="px-3 py-1 text-xs rounded bg-[#7ebc89] text-[#0f2b24]">
                    Editar
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
