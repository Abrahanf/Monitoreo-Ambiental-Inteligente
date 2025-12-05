import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Recuperar() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    nombre: "",
    email: "",
    nueva: "",
  });

  const [showPass, setShowPass] = useState(false);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate("/recuperar-codigo");
  };

  return (
    <div className="min-h-screen bg-[#0f2b24] flex items-center justify-center px-4">
      <form
        onSubmit={handleSubmit}
        className="bg-[#eaf3ec] p-10 rounded-3xl w-full max-w-md shadow text-center"
      >
        <h1 className="text-3xl font-bold text-[#0f2b24] mb-6">
          Recuperar contraseña
        </h1>

        <input
          name="nombre"
          placeholder="Ingrese nombre"
          className="w-full p-3 border border-gray-300 rounded-md bg-white placeholder-gray-500 text-[#0f2b24] mb-3"
          onChange={handleChange}
        />

        <input
          name="email"
          type="email"
          placeholder="Correo electrónico"
          className="w-full p-3 border border-gray-300 rounded-md bg-white placeholder-gray-500 text-[#0f2b24] mb-3"
          onChange={handleChange}
        />

        {/* PASSWORD */}
        <div className="relative mb-3">
          <input
            name="nueva"
            type={showPass ? "text" : "password"}
            placeholder="Nueva contraseña"
            className="w-full p-3 border border-gray-300 rounded-md bg-white placeholder-gray-500 text-[#0f2b24]"
            onChange={handleChange}
          />

          <button
            type="button"
            onClick={() => setShowPass(!showPass)}
            className="absolute right-3 top-2 text-gray-600 text-xl select-none"
          >
            👁
          </button>
        </div>

        <button
          type="submit"
          className="w-full bg-[#7ebc89] text-[#0f2b24] font-semibold py-3 rounded mt-4 hover:bg-[#6caf7d]"
        >
          Siguiente
        </button>

        <p className="mt-4 text-sm text-[#0f2b24]">
          or, <a href="/login" className="underline">log in</a>
        </p>
      </form>
    </div>
  );
}
