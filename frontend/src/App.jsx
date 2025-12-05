import AppRoutes from "./routes/index";
import ChatBotButton from "./components/chatbot/ChatBotButton";

export default function App() {
  return (
    <div className="font-sans">

      {/* Todas las rutas de tu app */}
      <AppRoutes />

      {/* Chatbot visible en TODA la interfaz */}
      <ChatBotButton />

    </div>
  );
}
