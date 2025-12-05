import { useState, useEffect } from 'react'
import { setAuthToken } from '../services/api'

export default function useUser() {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(null)

  useEffect(() => {
    const storedUser = localStorage.getItem('user')
    const storedToken = localStorage.getItem('token')
    if (storedUser && storedToken) {
      const u = JSON.parse(storedUser)
      setUser(u)
      setToken(storedToken)
      setAuthToken(storedToken)
    }
  }, [])

  const login = (userData, token) => {
    setUser(userData)
    setToken(token)
    setAuthToken(token)
    localStorage.setItem('user', JSON.stringify(userData))
    localStorage.setItem('token', token)
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    setAuthToken(null)
    localStorage.removeItem('user')
    localStorage.removeItem('token')
  }

  return { user, token, login, logout }
}
