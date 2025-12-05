export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#0f2b24] flex flex-col items-center justify-center text-center px-6">
      <h1 className="text-white text-5xl font-extrabold leading-tight">
        Monitoreo Ambiental <br /> Inteligente 🌿
      </h1>
      <p className="text-gray-200 text-lg mt-6 max-w-2xl">
        Sistema integral de sensores, alertas y análisis con Inteligencia Artificial.
      </p>
      <p className="text-gray-300 text-sm mt-2 max-w-xl">
        Control, predicción y toma de decisiones para ambientes saludables.
      </p>
      <button
        onClick={() => (window.location.href = '/login')}
        className="mt-10 bg-white text-[#0f2b24] px-10 py-3 rounded-full shadow-md text-lg font-medium hover:bg-gray-100 transition"
      >
        Ingresar al Sistema
      </button>
    </div>
  )
}
