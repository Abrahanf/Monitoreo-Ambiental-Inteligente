import { Routes, Route } from "react-router-dom";

// PUBLIC
import LandingPage from "../pages/LandingPage";
import Login from "../pages/Login";
import Signup from "../pages/Signup";
import Recuperar from "../pages/Recuperar";
import RecuperarCodigo from "../pages/RECUPERAR-CODIGO";
import PasswordCambiada from "../pages/PASSWORD-CAMBIADA";

// LAYOUTS
import AdminLayout from "../layouts/AdminLayout";
import ClienteLayout from "../layouts/ClienteLayout";

// ADMIN
import DashboardAdmin from "../pages/admin/DashboardAdmin";
import ConfigNodos from "../pages/admin/ConfigNodos";
import ConfigSenales from "../pages/admin/ConfigSenales";
import UsuariosAdmin from "../pages/admin/UsuariosAdmin";
import ModeloIA from "../pages/admin/ModeloIA";

// CLIENTE
import DashboardCliente from "../pages/cliente/DashboardCliente";
import DetallesCliente from "../pages/cliente/DetallesCliente";
import ReportesCliente from "../pages/cliente/ReportesCliente";
import PerfilCliente from "../pages/cliente/PerfilCliente";

export default function AppRoutes() {
  return (
    <Routes>

      {/* PUBLIC */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/recover" element={<Recuperar />} />
      <Route path="/recuperar-codigo" element={<RecuperarCodigo />} />
      <Route path="/password-cambiada" element={<PasswordCambiada />} />

      {/* ADMIN */}
      <Route path="/admin" element={<AdminLayout />}>
        <Route index element={<DashboardAdmin />} />
        <Route path="dashboard" element={<DashboardAdmin />} />
        <Route path="config-nodos" element={<ConfigNodos />} />
        <Route path="config-senales" element={<ConfigSenales />} />
        <Route path="users" element={<UsuariosAdmin />} />
        <Route path="modelo-ia" element={<ModeloIA />} />
      </Route>

      {/* CLIENTE */}
      <Route path="/cliente" element={<ClienteLayout />}>
        <Route index element={<DashboardCliente />} />
        <Route path="dashboard" element={<DashboardCliente />} />
        <Route path="detalles" element={<DetallesCliente />} />
        <Route path="reportes" element={<ReportesCliente />} />
        <Route path="perfil" element={<PerfilCliente />} />
      </Route>

    </Routes>
  );
}
