# Leadger - Professional Accounting System

Sistema de contabilidad profesional con Flask y Supabase.

## Deploy en Railway

Este proyecto está configurado para deploy automático en Railway.

### Variables de entorno requeridas:

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SECRET_KEY=your_secret_key
```

## Estructura

- `/` - Landing page
- `/app` - Login/Signup
- `/dashboard` - Aplicación (requiere autenticación)

## Stack

- Flask + Gunicorn
- Supabase (PostgreSQL + Auth)
- Railway (Deploy)
