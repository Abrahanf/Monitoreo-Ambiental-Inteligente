export default function PasswordCambiada() {
  return (
    <div className="min-h-screen bg-[#0f2b24] flex items-center justify-center px-4">
      <div className="bg-[#eaf3ec] p-10 rounded-3xl w-full max-w-md shadow text-center">

        <h1 className="text-3xl font-bold text-[#0f2b24] mb-6">
          cambiaste tu contraseña
        </h1>

        <a
          href="/login"
          className="block w-full bg-[#7ebc89] text-[#0f2b24] font-semibold py-3 rounded"
        >
          log in
        </a>
      </div>
    </div>
  );
}
