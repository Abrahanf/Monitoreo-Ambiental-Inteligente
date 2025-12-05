import axios from 'axios';

// 1. Configuración dinámica (Para que funcione en tu PC y en Docker)
// Si existe la variable de entorno (Docker), la usa. Si no, usa localhost:5000.
//const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
const API_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 2. INTERCEPTOR AUTOMÁTICO (Reemplaza a tu función setAuthToken)
// Antes de que salga CUALQUIER petición, revisa si hay token y lo pega.
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token'); // Busca en el almacenamiento del navegador
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 3. (Opcional pero recomendado) Interceptor de Errores
// Si el token expiró (Error 401), te saca automáticamente al login
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token'); // Borra el token malo
      // Opcional: window.location.href = '/login'; 
    }
    return Promise.reject(error);
  }
);

export default api;