import { useState, useEffect, useRef } from 'react'
import ChatMessage from './ChatMessage'

export default function ChatWindow({ messages, onSend, loading, onClose }) {
  const [input, setInput] = useState('')
  const endRef = useRef(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const handleSend = () => {
    if (!input.trim()) return
    onSend(input.trim())
    setInput('')
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="w-80 sm:w-96 h-96 bg-[#07221c] border border-emerald-600 rounded-2xl shadow-2xl flex flex-col mb-4">
      
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-2 bg-emerald-700 rounded-t-2xl">
        <div className="flex flex-col">
          <span className="text-sm font-semibold text-white">Asistente Ambiental IA</span>
          <span className="text-xs text-emerald-100/80">Monitoreo y alertas inteligentes</span>
        </div>
        <button onClick={onClose} className="text-white hover:text-gray-200 text-xl">×</button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-3 py-2 space-y-1 bg-[#031712]">
        {messages.map(m => (
          <ChatMessage key={m.id} from={m.from} text={m.text} />
        ))}

        {loading && (
          <div className="text-xs text-gray-300 italic">Analizando datos ambientales...</div>
        )}

        <div ref={endRef} />
      </div>

      {/* Input */}
      <div className="border-t border-emerald-700 px-3 py-2 bg-[#031712]">
        <div className="flex items-center gap-2">
          <textarea
            rows="1"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            className="flex-1 text-sm bg-[#00251e] text-white rounded-lg px-2 py-1 outline-none resize-none border border-emerald-700 focus:border-emerald-400"
            placeholder="Pregunta por sensores, datos, alertas..."
          />

          <button
            onClick={handleSend}
            className="bg-emerald-500 hover:bg-emerald-400 text-white px-3 py-1 rounded-lg text-sm font-semibold"
          >
            Enviar
          </button>
        </div>
      </div>

    </div>
  )
}
