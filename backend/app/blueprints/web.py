# backend/app/blueprints/web.py - VERSIÓN CORREGIDA
from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from functools import wraps
from app.services import AuthService
from app.repositories import UserRepository

web_bp = Blueprint('web', __name__)

def login_required(f):
    """Decorador para rutas que requieren login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicia sesión', 'warning')
            return redirect(url_for('web.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required_web(f):
    """Decorador para rutas que requieren admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicia sesión', 'warning')
            return redirect(url_for('web.login'))
        if session.get('rol') != 'administrador':
            flash('Acceso denegado. Se requiere rol de administrador', 'danger')
            return redirect(url_for('web.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# --- Rutas de autenticación ---

@web_bp.route('/')
def index():
    """Página principal"""
    if 'user_id' in session:
        return redirect(url_for('web.dashboard'))
    return redirect(url_for('web.login'))

@web_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    # Si ya está logueado, redirigir
    if 'user_id' in session:
        return redirect(url_for('web.dashboard'))
    
    # Si es POST, procesar login
    if request.method == 'POST':
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        
        # Autenticar usando el servicio
        result, status = AuthService.login(correo, contraseña)
        
        if status == 200:
            # Login exitoso - guardar en sesión
            user = result['user']
            session['user_id'] = user['id']
            session['nombre'] = user['nombre']
            session['correo'] = user['correo']
            session['rol'] = user['rol']
            session['nodo_id'] = user['nodo_id']
            session.permanent = True  # Sesión persistente
            
            flash(f'Bienvenido {user["nombre"]}!', 'success')
            
            # Redirigir según rol
            if user['rol'] == 'administrador':
                return redirect(url_for('web.admin_dashboard'))
            else:
                return redirect(url_for('web.dashboard'))
        else:
            # Login fallido
            flash(result.get('error', 'Error al iniciar sesión'), 'danger')
    
    return render_template('auth/login.html')

@web_bp.route('/forgot-password')
def forgot_password():
    """Página de recuperación de contraseña"""
    return render_template('auth/forgot_password.html')

@web_bp.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('web.login'))

# --- Rutas de usuario ---

@web_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal del usuario"""
    if session.get('rol') == 'administrador':
        return redirect(url_for('web.admin_dashboard'))
    
    # Verificar que el usuario tenga un nodo asignado
    if not session.get('nodo_id'):
        flash('No tienes un nodo asignado. Contacta al administrador.', 'warning')
    
    return render_template('user/dashboard.html')

@web_bp.route('/historical')
@login_required
def historical():
    """Página de históricos"""
    return render_template('user/historical.html')

@web_bp.route('/reports')
@login_required
def reports():
    """Página de reportes"""
    return render_template('user/reports.html')

@web_bp.route('/alerts')
@login_required
def alerts():
    """Página de alertas"""
    return render_template('user/alerts.html')

@web_bp.route('/profile')
@login_required
def profile():
    """Página de perfil"""
    return render_template('auth/change_password.html')

# --- Rutas de administrador ---

@web_bp.route('/admin')
@login_required
@admin_required_web
def admin_dashboard():
    """Dashboard del administrador"""
    return render_template('admin/dashboard.html')

@web_bp.route('/admin/users')
@login_required
@admin_required_web
def admin_users():
    """Gestión de usuarios"""
    return render_template('admin/users.html')

@web_bp.route('/admin/nodes')
@login_required
@admin_required_web
def admin_nodes():
    """Gestión de nodos"""
    return render_template('admin/nodes.html')

@web_bp.route('/admin/ia-config')
@login_required
@admin_required_web
def admin_ia_config():
    """Configuración de IA"""
    return render_template('admin/ia_config.html')

@web_bp.route('/admin/global-reports')
@login_required
@admin_required_web
def admin_global_reports():
    """Reportes globales"""
    return render_template('admin/global_reports.html')

