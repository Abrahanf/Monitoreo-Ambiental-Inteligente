import { useEffect, useState } from "react";
import api from "../../services/api"; // Importamos tu cliente Axios configurado

const fechaHoy = new Date().toLocaleDateString("es-PE", {
  weekday: "long",
  day: "numeric",
  month: "long",
  year: "numeric",
});

function NodoCard({ tag, zona, temp, estado }) {
  // Color del indicador según estado
  const statusColor = estado === 'ON' ? 'bg-green-500' : 'bg-red-500';

  return (
    <div className="bg-white rounded-lg shadow-sm border border-[#d4e3d7] p-4 flex flex-col justify-between">
      <div className="flex justify-between items-start">
        <div>
          <p className="text-xs text-gray-500">Nodo: {tag}</p>
          <p className="font-semibold text-[#0f2b24] mt-1">Ubicación: {zona}</p>
        </div>
        <span className={`w-3 h-3 rounded-full ${statusColor}`} title={estado} />
      </div>
      <div className="mt-6">
        {/* Mostramos temperatura o un guion si no hay datos */}
        <p className="text-4xl font-semibold text-[#0f2b24]">
          {temp !== null ? `${temp}°C` : "--"}
        </p>
      </div>
      <div className="mt-4 flex justify-between text-xs text-gray-600 border-t pt-3">
        <span>
          Humedad: <strong>{temp !== null ? "XX%" : "--"}</strong> {/* Pendiente: traer humedad */}
        </span>
        <span>
          Estado: <strong>{estado}</strong>
        </span>
      </div>
    </div>
  );
}

export default function DashboardAdmin() {
  const [nodos, setNodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Función para cargar datos
  const fetchDashboardData = async () => {
    try {
      // 1. Obtener la lista de nodos
      const response = await api.get("/nodes");
      
      // OJO AQUÍ: Extraemos la lista que está dentro de la propiedad 'nodes'
      // Si por alguna razón viene vacía, usamos un array vacío []
      const listaNodos = response.data.nodes || []; 

      // 2. Obtener la temperatura de cada nodo (uno por uno)
      const nodosConDatos = await Promise.all(
        listaNodos.map(async (nodo) => {
          try {
            // Pedimos el historial reciente para sacar la temperatura actual
            // Nota: Asegúrate de usar 'nodo.id' (tu JSON dice 'id': 2)
            const { data: history } = await api.get(`/measurements/historical/${nodo.id}?limit=1`);
            
            // El historial SÍ viene como lista [ ... ] según tu backend
            // Tomamos el primer dato (el más reciente)
            const lastMeasurement = history && history.length > 0 ? history[0] : null;
            
            return {
              ...nodo,
              // Si hay medición, tomamos la temperatura, si no, null
              temp: lastMeasurement ? lastMeasurement.temperatura : null
            };
          } catch (e) {
            console.warn(`No hay datos para nodo ${nodo.id}`, e);
            return { ...nodo, temp: null };
          }
        })
      );

      // 3. Guardar en el estado para que React pinte las tarjetas
      setNodos(nodosConDatos);
      
    } catch (err) {
      console.error("Error cargando dashboard:", err);
      setError("No se pudieron cargar los nodos.");
    } finally {
      setLoading(false);
    }
  };

  // Cargar al montar el componente
  useEffect(() => {
    fetchDashboardData();
    
    // Opcional: Recargar cada 30 segundos (Polling)
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <div className="p-6">Cargando datos del sistema...</div>;
  if (error) return <div className="p-6 text-red-600">{error}</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-xl font-semibold text-[#0f2b24]">
          Panel de Control <span className="font-bold">Admin</span>
        </h1>
        <span className="text-xs text-gray-600">{fechaHoy}</span>
      </div>

      {/* TARJETAS DE NODOS DINÁMICAS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {nodos.length > 0 ? (
          nodos.map((nodo) => (
            <NodoCard 
              key={nodo.id}
              tag={`NODE_${nodo.id}`} 
              zona={nodo.ubicacion} 
              temp={nodo.temp} 
              estado={nodo.estado}
            />
          ))
        ) : (
          <p className="text-gray-500 col-span-3">No hay nodos registrados en el sistema.</p>
        )}
      </div>

      {/* PLANO GENERAL */}
      <section className="bg-white rounded-lg shadow-sm border border-dashed border-[#c4d6c7] p-6 h-[320px] flex flex-col">
        <h2 className="text-sm font-semibold text-[#0f2b24] mb-4">
          Plano general de ubicación
        </h2>
        <div className="flex-1 border border-dashed border-[#c4d6c7] flex items-center justify-center text-sm text-gray-500">
          Plano de Planta (Próximamente)
        </div>
      </section>
    </div>
  );
}