export default function ChatMessage({ from, text }) {
  const isUser = from === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-1`}>
      <div
        className={`max-w-[80%] px-3 py-2 rounded-xl text-xs sm:text-sm whitespace-pre-wrap ${
          isUser
            ? 'bg-emerald-600 text-white rounded-br-none'
            : 'bg-[#0d3029] text-emerald-100 rounded-bl-none'
        }`}
      >
        {text}
      </div>
    </div>
  )
}
