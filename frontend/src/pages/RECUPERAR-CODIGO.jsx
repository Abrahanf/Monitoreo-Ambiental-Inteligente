import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function RecuperarCodigo() {
  const navigate = useNavigate();
  const [codigo, setCodigo] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate("/password-cambiada");
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
          type="text"
          placeholder="Ingrese el número que le hemos enviado por correo"
          value={codigo}
          onChange={(e) => setCodigo(e.target.value)}
          className="w-full p-3 border border-gray-300 rounded-md bg-white placeholder-gray-500 text-[#0f2b24]"
        />

        <button
          type="submit"
          className="w-full bg-[#7ebc89] text-[#0f2b24] font-semibold py-3 rounded mt-6"
        >
          Recuperar
        </button>

        <p className="mt-4 text-sm text-[#0f2b24]">
          or, <a href="/login" className="underline">log in</a>
        </p>
      </form>
    </div>
  );
}
