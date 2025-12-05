import { useState } from "react";

const fechaHoy = new Date().toLocaleDateString("es-PE", {
  weekday: "long",
  day: "numeric",
  month: "long",
  year: "numeric",
});

const VARIABLES = ["Temperatura", "Humedad", "CO₂"];

function ResumenCard({ titulo, valor, unidad, extra }) {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-[#d4e3d7] p-4 flex flex-col justify-between">
      <div className="flex justify-between items-start">
        <p className="text-xs text-gray-500">{titulo}</p>
        <span className="w-3 h-3 rounded-full bg-green-500" />
      </div>
      <p className="text-4xl font-semibold text-[#0f2b24] mt-4">
        {valor}
        <span className="text-2xl align-top ml-1">{unidad}</span>
      </p>
      <div className="mt-3 border-t pt-3 text-xs text-gray-600 flex justify-between">
        <span>
          Máx: <strong>{extra.max}</strong>
        </span>
        <span>
          Min: <strong>{extra.min}</strong>
        </span>
      </div>
    </div>
  );
}

function GraficoLinea() {
  return (
    <svg viewBox="0 0 400 160" className="w-full h-40 text-[#0f2b24]">
      {/* Ejes */}
      <line x1="30" y1="10" x2="30" y2="140" stroke="#c4d6c7" strokeWidth="1" />
      <line x1="30" y1="140" x2="380" y2="140" stroke="#c4d6c7" strokeWidth="1" />
      {/* Línea */}
      <polyline
        fill="none"
        stroke="#0f2b24"
        strokeWidth="2"
        points="40,100 90,70 140,80 190,60 240,75 290,90 340,80"
      />
    </svg>
  );
}

export default function DashboardCliente() {
  const [variable, setVariable] = useState("CO₂");

  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-1">
        <span className="text-xs text-gray-500">{fechaHoy}</span>
        <h1 className="text-lg font-semibold text-[#0f2b24]">Inicio</h1>
      </header>

      {/* CARDS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <ResumenCard
          titulo="Temperatura"
          valor="25"
          unidad="°C"
          extra={{ max: "28°C", min: "20°C" }}
        />
        <ResumenCard
          titulo="Humedad"
          valor="68"
          unidad="%"
          extra={{ max: "80 %", min: "52 %" }}
        />
        <ResumenCard
          titulo="CO₂"
          valor="746"
          unidad="ppm"
          extra={{ max: "805 ppm", min: "427 ppm" }}
        />
      </div>

      {/* GRÁFICA */}
      <section className="bg-white rounded-lg shadow-sm border border-[#d4e3d7] p-4 space-y-4">
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">
            Variación durante el día (placeholder)
          </span>
          <select
            className="border rounded px-3 py-1 text-sm bg-white"
            value={variable}
            onChange={(e) => setVariable(e.target.value)}
          >
            {VARIABLES.map((v) => (
              <option key={v} value={v}>
                {v}
              </option>
            ))}
          </select>
        </div>
        <GraficoLinea />
      </section>
    </div>
  );
}
