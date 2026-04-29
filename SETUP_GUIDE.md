# Guía de Configuración - Leadger en Railway + Supabase

## 📋 Prerequisitos

- Cuenta en [Railway.app](https://railway.app)
- Cuenta en [Supabase.com](https://supabase.com)
- Repositorio de GitHub con el código

## 🗄️ Paso 1: Configurar Supabase

### 1.1 Crear proyecto
1. Accede a [Supabase.com](https://supabase.com)
2. Click en "New Project"
3. Completa:
   - **Name**: leadger-db
   - **Database Password**: (guarda esta contraseña)
   - **Region**: Elige la más cercana a tus usuarios
4. Click "Create new project" y espera 2-3 minutos

### 1.2 Ejecutar el schema SQL
1. En tu proyecto de Supabase, ve a **SQL Editor** (icono de base de datos en el menú izquierdo)
2. Click en "New query"
3. Copia TODO el contenido de `supabase_schema.sql`
4. Pega en el editor
5. Click en "Run" (botón verde abajo a la derecha)
6. Verifica que aparezca "Success. No rows returned"

### 1.3 Obtener credenciales
1. Ve a **Settings** → **API**
2. Copia y guarda:
   - **Project URL** (ejemplo: `https://abcdefgh.supabase.co`)
   - **anon/public key** (la key larga que empieza con `eyJ...`)

## 🚂 Paso 2: Configurar Railway

### 2.1 Crear proyecto en Railway
1. Accede a [Railway.app](https://railway.app)
2. Click en "New Project"
3. Selecciona "Deploy from GitHub repo"
4. Autoriza Railway a acceder a tu GitHub
5. Selecciona el repositorio donde subiste el código de Leadger

### 2.2 Configurar variables de entorno
1. Una vez creado el proyecto, click en tu servicio
2. Ve a la pestaña **Variables**
3. Click en "New Variable" y agrega cada una de estas:

```
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-anon-key-aqui
SECRET_KEY=genera-una-clave-secreta-random-aqui
DEBUG=False
```

**Para generar SECRET_KEY**, ejecuta en tu terminal:
```bash
python3 -c "import os; print(os.urandom(24).hex())"
```

### 2.3 Configurar dominio personalizado
1. En Railway, ve a la pestaña **Settings**
2. Busca la sección "Networking"
3. Click en "Generate Domain" (te dará un dominio tipo `xxx.up.railway.app`)
4. Para usar tu dominio `leadger.net`:
   - Click en "Custom Domain"
   - Ingresa `leadger.net`
   - Railway te dará registros DNS para configurar
   - Ve a tu proveedor de DNS (donde compraste leadger.net)
   - Agrega los registros CNAME/A que Railway te indica
   - Espera 5-30 minutos para propagación DNS

## 🔍 Paso 3: Verificar deployment

### 3.1 Ver logs
1. En Railway, ve a la pestaña **Deployments**
2. Click en el deployment activo
3. Verás los logs en tiempo real
4. Busca líneas como:
   ```
   * Running on all addresses (0.0.0.0)
   * Running on http://127.0.0.1:XXXX
   ```

### 3.2 Probar la aplicación
1. Abre tu dominio de Railway o `leadger.net`
2. Deberías ver la landing page
3. Click en "Start free →" o "Sign In"
4. Prueba crear una cuenta
5. Inicia sesión con el usuario demo:
   - Email: `demo@leadger.net`
   - Password: `demo123`

## ❗ Troubleshooting

### Error: "Internal Server Error"
- Verifica los logs en Railway
- Asegúrate que las variables de entorno estén configuradas
- Verifica que el schema SQL se ejecutó correctamente

### Error: "Failed to connect to Supabase"
- Verifica que `SUPABASE_URL` y `SUPABASE_KEY` sean correctos
- Asegúrate que el proyecto de Supabase esté activo
- Verifica que las tablas existan (ve a Table Editor en Supabase)

### Error: "User not found" al hacer login
- Verifica que el usuario demo se creó ejecutando en Supabase SQL Editor:
  ```sql
  SELECT * FROM users WHERE email = 'demo@leadger.net';
  ```
- Si no existe, ejecuta de nuevo la parte final de `supabase_schema.sql`

### Dominio no funciona
- Espera 30-60 minutos para propagación DNS
- Verifica los registros DNS en tu proveedor
- Usa [whatsmydns.net](https://whatsmydns.net) para verificar propagación
- Asegúrate de usar el dominio exacto que configuraste en Railway

## 🔐 Seguridad en Producción

### Recomendaciones adicionales:
1. **Cambiar hashing de contraseñas**: El código actual usa SHA-256. Para producción, actualiza a bcrypt:
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash
   ```

2. **HTTPS**: Railway provee HTTPS automáticamente

3. **Rate Limiting**: Considera agregar Flask-Limiter para prevenir ataques de fuerza bruta

4. **Validación de email**: Agrega verificación de email antes de activar cuentas

## 📦 Actualizar la Aplicación

Cuando hagas cambios en el código:
1. Haz commit y push a tu repositorio de GitHub
2. Railway detectará automáticamente los cambios
3. Iniciará un nuevo deployment
4. Podrás ver el progreso en la pestaña Deployments

## 🎯 Próximos Pasos

Una vez que todo esté funcionando, necesitas:
1. Crear `templates/app.html` con el dashboard completo
2. Extraer el JavaScript del archivo original a `static/js/app.js`
3. Agregar las funcionalidades de contactos, ventas, compras, etc.
4. Implementar las páginas de error (404.html, 500.html)

¿Necesitas ayuda con alguno de estos pasos?
