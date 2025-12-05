import { useState } from 'react'
import ChatWindow from './ChatWindow'

export default function ChatContainer({ onClose }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      from: 'bot',
      text: 'Hola, soy el asistente cognitivo. Pregúntame por el estado actual del ambiente o las últimas alertas. 🌿'
    }
  ])
  const [loading, setLoading] = useState(false)

  const sendMessage = async (text) => {
    const userMsg = { id: Date.now(), from: 'user', text }
    setMessages(prev => [...prev, userMsg])
    setLoading(true)

    try {
      const res = await fetch('/api/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      })

      const data = await res.json()

      const botMsg = {
        id: Date.now() + 1,
        from: 'bot',
        text: data.reply || 'No tengo respuesta en este momento.'
      }

      setMessages(prev => [...prev, botMsg])
    } catch (e) {
      setMessages(prev => [...prev, {
        id: Date.now() + 2,
        from: 'bot',
        text: 'Ocurrió un error al contactar al asistente. Intenta de nuevo.'
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <ChatWindow
      messages={messages}
      onSend={sendMessage}
      loading={loading}
      onClose={onClose}
    />
  )
}
