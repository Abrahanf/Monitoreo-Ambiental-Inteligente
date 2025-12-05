// src/components/chatbot/ChatBotButton.jsx
import { useState } from "react";
import ChatContainer from "./ChatContainer";

export default function ChatBotButton() {
  const [open, setOpen] = useState(false);

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {open && <ChatContainer onClose={() => setOpen(false)} />}
      {!open && (
        <button
          onClick={() => setOpen(true)}
          className="bg-emerald-500 hover:bg-emerald-400 text-white rounded-full w-14 h-14 shadow-lg flex items-center justify-center text-2xl border-2 border-[#0f2f28]"
        >
          💬
        </button>
      )}
    </div>
  );
}
