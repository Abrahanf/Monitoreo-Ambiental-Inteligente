export default function Button({ children, variant = 'primary', className = '', ...props }) {
  const base = 'px-4 py-2 rounded-full font-semibold text-sm transition'
  const variants = {
    primary: 'bg-emerald-500 hover:bg-emerald-400 text-white',
    outline: 'border border-slate-600 text-slate-100 hover:bg-slate-800',
  }
  return (
    <button className={`${base} ${variants[variant]} ${className}`} {...props}>
      {children}
    </button>
  )
}
