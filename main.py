#!/usr/bin/env python3
"""
Leadger - Professional Accounting System
Web Application (Flask)
"""

import os
from flask import Flask, render_template, send_from_directory, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
from supabase import create_client, Client
import json

# Cargar variables de entorno
load_dotenv()

# Configuración de la aplicación
app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

# Configuración de la clave secreta para sesiones
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Inicializar cliente de Supabase
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# =====================================================
# RUTAS - LANDING PAGE
# =====================================================

@app.route('/')
def index():
    """Landing page principal"""
    return render_template('landing.html')


# =====================================================
# RUTAS - AUTENTICACIÓN
# =====================================================

@app.route('/app')
def auth_page():
    """Página de autenticación (login/signup)"""
    # Si ya está autenticado, redirigir al dashboard
    if session.get('user'):
        return redirect(url_for('dashboard'))
    return render_template('auth.html')


@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """Registro de nuevo usuario"""
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500
    
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name', '')
        company = data.get('company', '')
        
        # Registrar en Supabase Auth
        response = supabase.auth.sign_up({
            'email': email,
            'password': password,
            'options': {
                'data': {
                    'full_name': full_name,
                    'company': company
                }
            }
        })
        
        if response.user:
            session['user'] = {
                'id': response.user.id,
                'email': response.user.email,
                'full_name': full_name,
                'company': company
            }
            return jsonify({'success': True, 'user': session['user']})
        else:
            return jsonify({'error': 'Signup failed'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Inicio de sesión"""
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500
    
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        # Autenticar con Supabase
        response = supabase.auth.sign_in_with_password({
            'email': email,
            'password': password
        })
        
        if response.user:
            # Obtener datos adicionales del perfil
            try:
                profile = supabase.table('profiles').select('*').eq('id', response.user.id).execute()
                profile_data = profile.data[0] if profile.data else {}
            except:
                profile_data = {}
            
            user_data = {
                'id': response.user.id,
                'email': response.user.email,
                'full_name': profile_data.get('full_name', ''),
                'company': profile_data.get('company', '')
            }
            
            session['user'] = user_data
            return jsonify({'success': True, 'user': user_data})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Cerrar sesión"""
    session.pop('user', None)
    if supabase:
        try:
            supabase.auth.sign_out()
        except:
            pass
    return jsonify({'success': True, 'redirect': '/app'})


# =====================================================
# RUTAS - APLICACIÓN (Requiere autenticación)
# =====================================================

@app.route('/dashboard')
def dashboard():
    """Panel principal de la aplicación"""
    # Verificar autenticación
    if not session.get('user'):
        return redirect(url_for('auth_page'))
    
    return render_template('app.html', user=session['user'])


# =====================================================
# API - DATOS DE LA APLICACIÓN
# =====================================================

@app.route('/api/data/save', methods=['POST'])
def save_data():
    """Guardar datos de la aplicación en Supabase"""
    if not session.get('user'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500
    
    try:
        user_id = session['user']['id']
        data = request.json
        
        # Guardar en la tabla app_data
        result = supabase.table('app_data').upsert({
            'user_id': user_id,
            'data': data,
            'updated_at': 'now()'
        }).execute()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/data/load', methods=['GET'])
def load_data():
    """Cargar datos de la aplicación desde Supabase"""
    if not session.get('user'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500
    
    try:
        user_id = session['user']['id']
        
        # Cargar desde la tabla app_data
        result = supabase.table('app_data').select('data').eq('user_id', user_id).execute()
        
        if result.data and len(result.data) > 0:
            return jsonify(result.data[0]['data'])
        else:
            # No hay datos, devolver estructura vacía
            return jsonify({}), 204
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export', methods=['POST'])
def export_data():
    """Exportar datos a CSV"""
    if not session.get('user'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.json
        filename = data.get('filename', 'export.csv')
        content = data.get('content', '')
        
        return jsonify({
            'success': True,
            'filename': filename,
            'content': content
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# =====================================================
# MANEJO DE ERRORES
# =====================================================

@app.errorhandler(404)
def not_found(e):
    return render_template('landing.html'), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500


# =====================================================
# PUNTO DE ENTRADA
# =====================================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
