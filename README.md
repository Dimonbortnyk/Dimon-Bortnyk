# Leadger - Professional Accounting System

Sistema de contabilidad profesional con landing page, autenticación y dashboard completo.

## 🚀 Stack Tecnológico

- **Backend**: Flask + Python
- **Base de Datos**: Supabase (PostgreSQL)
- **Hosting**: Railway
- **Frontend**: HTML + CSS + JavaScript vanilla

## 📦 Estructura del Proyecto

```
leadger/
├── main.py                 # Aplicación Flask principal
├── requirements.txt        # Dependencias Python
├── Procfile               # Configuración Railway
├── supabase_schema.sql    # Schema de base de datos
├── templates/             # Plantillas HTML
│   ├── landing.html       # Página de inicio
│   ├── login.html         # Página de login
│   ├── signup.html        # Página de registro
│   └── app.html           # Dashboard principal (pendiente)
└── static/                # Archivos estáticos
    ├── css/
    │   ├── landing.css    # Estilos landing
    │   └── auth.css       # Estilos autenticación
    └── js/
        └── app.js         # JavaScript de la app (pendiente)
```

## 🔧 Configuración de Supabase

### 1. Crear proyecto en Supabase
1. Ve a [supabase.com](https://supabase.com)
2. Crea un nuevo proyecto
3. Copia tu `Project URL` y `anon public key`

### 2. Crear las tablas
1. Ve a SQL Editor en Supabase
2. Copia y ejecuta el contenido de `supabase_schema.sql`
3. Verifica que las tablas `users` y `app_data` se crearon correctamente

### 3. Configurar variables de entorno en Railway
1. Ve a tu proyecto en Railway
2. Settings → Variables
3. Agrega:
   - `SUPABASE_URL`: Tu URL de Supabase
   - `SUPABASE_KEY`: Tu anon/public key de Supabase
   - `SECRET_KEY`: Una clave secreta random (puedes generarla con `python -c "import os; print(os.urandom(24).hex())"`)

## 🌐 Deployment en Railway

### Opción 1: Desde GitHub
1. Sube este código a tu repositorio de GitHub
2. En Railway, conecta el repositorio
3. Railway detectará automáticamente el `Procfile` y desplegará

### Opción 2: Railway CLI
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Inicializar proyecto
railway init

# Desplegar
railway up
```

## 🔐 Seguridad

- Las contraseñas se hashean con SHA-256 (considera usar bcrypt en producción)
- Row Level Security (RLS) habilitado en Supabase
- Sessions seguras con Flask
- CORS configurado

## 📝 Usuario Demo

Después de ejecutar el schema SQL, tendrás un usuario demo:
- **Email**: demo@leadger.net
- **Password**: demo123

## 🎨 Personalización

### Cambiar colores del tema
Edita las variables CSS en:
- `static/css/landing.css`
- `static/css/auth.css`

Variables principales:
```css
--bg: #0f0f11;           /* Fondo principal */
--accent: #c8ff00;       /* Color de acento (verde-amarillo) */
--surface: #16161a;      /* Superficies/tarjetas */
--text: #f0f0f4;         /* Texto principal */
```

## 🔄 Próximos Pasos

Aún falta crear:
1. `templates/app.html` - Dashboard principal de la aplicación
2. `static/css/app.css` - Estilos del dashboard
3. `static/js/app.js` - Lógica de la aplicación (basada en el código original)
4. Templates de error (404.html, 500.html)

## 📧 Soporte

Para problemas o preguntas, contacta al equipo de desarrollo.
