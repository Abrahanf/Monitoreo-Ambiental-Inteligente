import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    nombre: "",
    email: "",
    pass1: "",
    pass2: "",
  });

  const [showPass1, setShowPass1] = useState(false);
  const [showPass2, setShowPass2] = useState(false);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = (e) => {
    e.preventDefault();

    // Aquí luego conectarás con tu backend.
    alert("Registro exitoso. Ahora inicia sesión.");
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-[#0f2b24] flex items-center justify-center px-4">
      <form
        onSubmit={handleSubmit}
        className="bg-[#eaf3ec] p-10 rounded-3xl w-full max-w-md shadow text-center"
      >
        <h1 className="text-3xl font-bold text-[#0f2b24] mb-6">Sign up</h1>

        {/* NOMBRE */}
        <input
          name="nombre"
          placeholder="Ingrese nombre"
          value={form.nombre}
          onChange={handleChange}
          className="w-full p-3 border border-gray-300 rounded-md bg-white text-[#0f2b24] placeholder-gray-500 text-sm mb-3"
        />

        {/* CORREO */}
        <input
          name="email"
          placeholder="Correo electrónico"
          type="email"
          value={form.email}
          onChange={handleChange}
          className="w-full p-3 border border-gray-300 rounded-md bg-white text-[#0f2b24] placeholder-gray-500 text-sm mb-3"
        />

        {/* CONTRASEÑA */}
        <div className="relative mb-3">
          <input
            name="pass1"
            type={showPass1 ? "text" : "password"}
            placeholder="Contraseña"
            value={form.pass1}
            onChange={handleChange}
            className="w-full p-3 border border-gray-300 rounded-md bg-white text-[#0f2b24] placeholder-gray-500 text-sm"
          />
          <button
            type="button"
            onClick={() => setShowPass1(!showPass1)}
            className="absolute right-3 top-2 text-gray-700 text-xl select-none"
          >
            👁
          </button>
        </div>

        {/* REPETIR CONTRASEÑA */}
        <div className="relative mb-3">
          <input
            name="pass2"
            type={showPass2 ? "text" : "password"}
            placeholder="Repita la contraseña"
            value={form.pass2}
            onChange={handleChange}
            className="w-full p-3 border border-gray-300 rounded-md bg_WHITE text-[#0f2b24] placeholder-gray-500 text-sm"
          />
          <button
            type="button"
            onClick={() => setShowPass2(!showPass2)}
            className="absolute right-3 top-2 text-gray-700 text-xl select-none"
          >
            👁
          </button>
        </div>

        <p className="text-[11px] text-gray-700 mb-4">
          contraseña: mínimo 8 caracteres, debe incluir al menos un número y una tecla especial.
        </p>

        <button
          type="submit"
          className="w-full bg-[#7ebc89] text-[#0f2b24] py-2 rounded font-semibold"
        >
          Sign in
        </button>

        <p className="text-center mt-4 text-sm text-[#0f2b24]">
          or, <a href="/login" className="underline">log in</a>
        </p>
      </form>
    </div>
  );
}
