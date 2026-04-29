#!/usr/bin/env python3
"""
Leadger - Professional Accounting System
Web version with Flask for Railway deployment + Supabase
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import json
from functools import wraps
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'leadger-production-secret-key-change-this')
CORS(app)

# Configuración
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config['JSON_AS_ASCII'] = False

# Supabase Configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')

# Initialize Supabase client
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")

# ============= HELPERS =============

def hash_password(password):
    """Simple hash para password (en producción usar bcrypt)"""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_by_email(email):
    """Obtiene un usuario de Supabase por email"""
    if not supabase:
        return None
    try:
        response = supabase.table('users').select('*').eq('email', email).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def create_user(email, password, name, company):
    """Crea un nuevo usuario en Supabase"""
    if not supabase:
        return None
    try:
        user_data = {
            'email': email,
            'password_hash': hash_password(password),
            'name': name,
            'company': company or 'My Company',
            'created_at': datetime.now().isoformat()
        }
        response = supabase.table('users').insert(user_data).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def get_user_app_data(user_id):
    """Obtiene los datos de la app del usuario"""
    if not supabase:
        return {
            'contacts': [],
            'sales': [],
            'purchases': [],
            'treasury': [],
            'journal': [],
            'settings': {}
        }
    try:
        response = supabase.table('app_data').select('*').eq('user_id', user_id).execute()
        if response.data and len(response.data) > 0:
            return response.data[0].get('data', {})
        return {
            'contacts': [],
            'sales': [],
            'purchases': [],
            'treasury': [],
            'journal': [],
            'settings': {}
        }
    except Exception as e:
        print(f"Error getting app data: {e}")
        return {
            'contacts': [],
            'sales': [],
            'purchases': [],
            'treasury': [],
            'journal': [],
            'settings': {}
        }

def save_user_app_data(user_id, data):
    """Guarda los datos de la app del usuario"""
    if not supabase:
        return False
    try:
        # Verificar si ya existe un registro
        existing = supabase.table('app_data').select('id').eq('user_id', user_id).execute()
        
        if existing.data and len(existing.data) > 0:
            # Actualizar
            response = supabase.table('app_data').update({
                'data': data,
                'updated_at': datetime.now().isoformat()
            }).eq('user_id', user_id).execute()
        else:
            # Insertar
            response = supabase.table('app_data').insert({
                'user_id': user_id,
                'data': data,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }).execute()
        
        return True
    except Exception as e:
        print(f"Error saving app data: {e}")
        return False

# Decorator para rutas protegidas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            if request.is_json:
                return jsonify({'error': 'Not authenticated'}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ============= RUTAS PÚBLICAS =============

@app.route('/')
def landing():
    """Página de aterrizaje principal"""
    if 'user_email' in session:
        return redirect(url_for('app_dashboard'))
    return render_template('landing.html')

@app.route('/login')
def login():
    """Página de login"""
    if 'user_email' in session:
        return redirect(url_for('app_dashboard'))
    return render_template('login.html')

@app.route('/signup')
def signup():
    """Página de registro"""
    if 'user_email' in session:
        return redirect(url_for('app_dashboard'))
    return render_template('signup.html')

# ============= API AUTH =============

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """API endpoint para login"""
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'success': False, 'error': 'Email and password required'}), 400
    
    # Obtener usuario de Supabase
    user = get_user_by_email(email)
    
    # Verificar credenciales
    if not user or user.get('password_hash') != hash_password(password):
        return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
    
    # Login exitoso
    session['user_id'] = user['id']
    session['user_email'] = email
    session['user_name'] = user.get('name', email.split('@')[0].title())
    session['user_company'] = user.get('company', 'My Company')
    session.permanent = True
    
    return jsonify({
        'success': True,
        'user': {
            'email': email,
            'name': session['user_name'],
            'company': session['user_company']
        }
    })

@app.route('/api/auth/signup', methods=['POST'])
def api_signup():
    """API endpoint para registro"""
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    name = data.get('name', '').strip()
    company = data.get('company', '').strip()
    
    if not email or not password or not name:
        return jsonify({'success': False, 'error': 'All fields are required'}), 400
    
    # Verificar si el usuario ya existe
    existing_user = get_user_by_email(email)
    if existing_user:
        return jsonify({'success': False, 'error': 'Email already registered'}), 400
    
    # Crear nuevo usuario
    user = create_user(email, password, name, company)
    if not user:
        return jsonify({'success': False, 'error': 'Failed to create account'}), 500
    
    # Auto login
    session['user_id'] = user['id']
    session['user_email'] = email
    session['user_name'] = name
    session['user_company'] = company or 'My Company'
    session.permanent = True
    
    return jsonify({
        'success': True,
        'user': {
            'email': email,
            'name': name,
            'company': company or 'My Company'
        }
    })

@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    """API endpoint para logout"""
    session.clear()
    return jsonify({'success': True})

@app.route('/api/auth/check', methods=['GET'])
def api_check_auth():
    """Verifica si el usuario está autenticado"""
    if 'user_email' in session:
        return jsonify({
            'authenticated': True,
            'user': {
                'email': session['user_email'],
                'name': session['user_name'],
                'company': session['user_company']
            }
        })
    return jsonify({'authenticated': False}), 401

# ============= RUTAS DE LA APP (PROTEGIDAS) =============

@app.route('/app')
@login_required
def app_dashboard():
    """Dashboard principal de la aplicación"""
    return render_template('app.html',
                         user_name=session.get('user_name'),
                         user_email=session.get('user_email'),
                         user_company=session.get('user_company'))

# ============= API ENDPOINTS DE LA APP =============

@app.route('/api/load', methods=['GET'])
@login_required
def api_load_data():
    """Carga todos los datos del usuario"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not found'}), 404
    
    # Obtener datos guardados del usuario
    app_data = get_user_app_data(user_id)
    
    # Si app_data está vacío o no tiene la estructura correcta, devolver estructura por defecto
    if not app_data or 'ids' not in app_data:
        # Obtener nombre y apellido del nombre completo
        full_name = session.get('user_name', 'User')
        name_parts = full_name.split(' ', 1)
        fname = name_parts[0] if len(name_parts) > 0 else 'User'
        lname = name_parts[1] if len(name_parts) > 1 else ''
        
        app_data = {
            'user': {
                'fname': fname,
                'lname': lname,
                'role': 'Chief Accountant',
                'email': session.get('user_email', ''),
                'phone': '',
                'avatarColor': '#c8ff00'
            },
            'co': {
                'name': session.get('user_company', 'My Company Ltd.'),
                'taxid': '',
                'industry': '',
                'addr': '',
                'fy': '2025',
                'fystart': 'Jan',
                'cur': '€',
                'defvat': '21'
            },
            'prefs': {
                'datefmt': 'DD/MM/YYYY',
                'numfmt': 'us',
                'lang': 'en',
                'accent': '#c8ff00',
                'invnotes': '',
                'invpfx': 'INV-',
                'purpfx': 'PINV-'
            },
            'series': [
                {'id': 1, 'name': 'Sales Invoices', 'code': 'INV', 'format': 'INV[YY]-%%%%%', 'lastNum': 0, 'type': 'sale', 'active': True},
                {'id': 2, 'name': 'Credit Notes', 'code': 'CN', 'format': 'CN[YY]-%%%%%', 'lastNum': 0, 'type': 'credit', 'active': True},
                {'id': 3, 'name': 'Purchase Invoices', 'code': 'PINV', 'format': 'PINV[YY]-%%%%', 'lastNum': 0, 'type': 'purchase', 'active': True}
            ],
            'sales': [],
            'purch': [],
            'coll': [],
            'pay': [],
            'je': [],
            'contacts': [],
            'recurring': [],
            'assets': [],
            'deprPlans': [],
            'ids': {'s': 1, 'p': 1, 'c': 1, 'py': 1, 'j': 1, 'ct': 1, 'rc': 1, 'ast': 1, 'dp': 1}
        }
    
    return jsonify(app_data)

@app.route('/api/save', methods=['POST'])
@login_required
def api_save_data():
    """Guarda todos los datos del usuario"""
    try:
        data = request.get_json()
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        # Guardar en Supabase
        success = save_user_app_data(user_id, data)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Failed to save data'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export', methods=['POST'])
@login_required
def api_export():
    """Exporta datos a CSV"""
    try:
        data = request.get_json()
        filename = data.get('filename', 'export.csv')
        content = data.get('content', '')
        
        # En producción, podrías guardar temporalmente y enviar el archivo
        from io import BytesIO
        output = BytesIO()
        output.write(content.encode('utf-8-sig'))
        output.seek(0)
        
        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============= HEALTH CHECK =============

@app.route('/health')
def health():
    """Health check para Railway"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

# ============= ERROR HANDLERS =============

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Not found'}), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('500.html'), 500

# ============= MAIN =============

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
