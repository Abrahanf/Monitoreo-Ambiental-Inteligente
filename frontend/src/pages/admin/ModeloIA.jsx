import { useState } from "react";

const fechaHoy = new Date().toLocaleDateString("es-PE", {
  weekday: "long",
  day: "numeric",
  month: "long",
  year: "numeric",
});

export default function ModeloIA() {
  const [dataset, setDataset] = useState("historico");
  const [showModal, setShowModal] = useState(false);

  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-1">
        <span className="text-xs text-gray-500">{fechaHoy}</span>
        <h1 className="text-lg font-semibold text-[#0f2b24]">
          Configuración de modelo IA
        </h1>
      </header>

      {/* INFO GENERAL */}
      <section className="bg-white rounded-lg shadow-sm border border-[#d4e3d7]">
        <div className="px-4 py-3 border-b border-[#e0eee3]">
          <span className="font-semibold text-sm">Información general</span>
        </div>
        <table className="w-full text-sm">
          <thead className="bg-[#eaf3ec] text-left text-gray-700">
            <tr>
              <th className="px-4 py-2">Tipo de modelo</th>
              <th className="px-4 py-2">Estado actual</th>
              <th className="px-4 py-2">Último entrenamiento</th>
              <th className="px-4 py-2">Precisión</th>
              <th className="px-4 py-2">Dataset usado</th>
            </tr>
          </thead>
          <tbody>
            <tr className="border-t border-[#e0eee3]">
              <td className="px-4 py-2">
                <span className="inline-flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-sm bg-green-500" />
                  Por ver
                </span>
              </td>
              <td className="px-4 py-2 font-semibold text-[#0f2b24]">
                Entrenado
              </td>
              <td className="px-4 py-2">2025-09-20</td>
              <td className="px-4 py-2">92.4 %</td>
              <td className="px-4 py-2">Histórico 2025</td>
            </tr>
          </tbody>
        </table>
      </section>

      {/* CONFIGURACIÓN */}
      <section className="bg-white rounded-lg shadow-sm border border-[#d4e3d7] p-4 space-y-4">
        <h2 className="font-semibold text-sm mb-2">Configuración</h2>

        <div className="grid md:grid-cols-3 gap-4 text-sm">
          {/* VARIABLES USADAS */}
          <div>
            <p className="font-semibold mb-2">Variables usadas</p>
            <div className="space-y-1">
              <label className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-sm bg-green-500" />
                <span>Temperatura</span>
              </label>
              <label className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-sm bg-green-500" />
                <span>Humedad</span>
              </label>
              <label className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-sm bg-green-500" />
                <span>CO2</span>
              </label>
            </div>
          </div>

          {/* VENTANA / DATASET */}
          <div>
            <p className="font-semibold mb-2">Ventana temporal de análisis</p>
            <p className="mb-4">24 h</p>

            <p className="font-semibold mb-2">Dataset</p>
            <div className="space-y-1">
              <label className="flex items-center gap-2">
                <input
                  type="radio"
                  name="dataset"
                  value="historico"
                  checked={dataset === "historico"}
                  onChange={(e) => setDataset(e.target.value)}
                />
                Histórico 2025
              </label>
              <label className="flex items-center gap-2">
                <input
                  type="radio"
                  name="dataset"
                  value="cargar"
                  checked={dataset === "cargar"}
                  onChange={(e) => setDataset(e.target.value)}
                />
                Cargar datos
              </label>
            </div>
          </div>

          {/* SENSIBILIDAD */}
          <div>
            <p className="font-semibold mb-2">Sensibilidad de alerta</p>
            <div className="flex flex-col gap-2 mt-2">
              <input type="range" min="0" max="100" defaultValue="70" />
              <div className="flex justify-between text-xs text-gray-600">
                <span>Low</span>
                <span>High</span>
              </div>
            </div>
          </div>
        </div>

        {/* BOTONES */}
        <div className="flex gap-4 mt-4">
          <button className="px-4 py-2 text-sm rounded bg-[#7ebc89] text-[#0f2b24] font-semibold">
            Entrenar modelo
          </button>
          <button className="px-4 py-2 text-sm rounded bg-gray-100 text-gray-800">
            Resetear modelo
          </button>
          <button
            className="ml-auto px-4 py-2 text-sm rounded bg-[#7ebc89] text-[#0f2b24]"
            onClick={() => setShowModal(true)}
          >
            Cargar archivo…
          </button>
        </div>
      </section>

      {/* MODAL CARGAR ARCHIVO */}
      {showModal && (
        <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50">
          <div className="bg-[#eaf3ec] rounded-xl shadow-lg w-[420px] p-8 text-center space-y-6 border border-[#c4d6c7]">
            <p className="text-xl font-semibold text-[#0f2b24]">
              Cargar archivo
            </p>
            <div className="border border-dashed border-[#c4d6c7] rounded-lg py-10 text-sm text-gray-600">
              Aquí se seleccionará el dataset (placeholder).
            </div>
            <button
              className="px-6 py-2 rounded bg-[#7ebc89] text-[#0f2b24] font-semibold"
              onClick={() => setShowModal(false)}
            >
              Aceptar
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
