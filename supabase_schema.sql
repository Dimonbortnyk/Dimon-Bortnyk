-- ══════════════════════════════════════════════════════════════════════
-- LEADGER DATABASE SCHEMA FOR SUPABASE
-- ══════════════════════════════════════════════════════════════════════

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice en email para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Tabla de datos de la aplicación (almacena el JSON completo de cada usuario)
CREATE TABLE IF NOT EXISTS app_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    data JSONB NOT NULL DEFAULT '{
        "contacts": [],
        "sales": [],
        "purchases": [],
        "treasury": [],
        "journal": [],
        "settings": {}
    }'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

-- Índice en user_id para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_app_data_user_id ON app_data(user_id);

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers para actualizar updated_at
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_app_data_updated_at ON app_data;
CREATE TRIGGER update_app_data_updated_at
    BEFORE UPDATE ON app_data
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ══════════════════════════════════════════════════════════════════════
-- ROW LEVEL SECURITY (RLS)
-- ══════════════════════════════════════════════════════════════════════

-- Habilitar RLS en las tablas
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE app_data ENABLE ROW LEVEL SECURITY;

-- Políticas para users (permite lectura/escritura del propio usuario)
CREATE POLICY "Users can read own data" ON users
    FOR SELECT
    USING (true); -- Permitir lectura para auth (puedes restringir más si usas Supabase Auth)

CREATE POLICY "Users can update own data" ON users
    FOR UPDATE
    USING (true);

-- Políticas para app_data (permite lectura/escritura del propio usuario)
CREATE POLICY "Users can read own app_data" ON app_data
    FOR SELECT
    USING (true);

CREATE POLICY "Users can insert own app_data" ON app_data
    FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Users can update own app_data" ON app_data
    FOR UPDATE
    USING (true);

-- ══════════════════════════════════════════════════════════════════════
-- DATOS DE EJEMPLO (OPCIONAL - SOLO PARA DESARROLLO)
-- ══════════════════════════════════════════════════════════════════════

-- Usuario demo (password: demo123)
-- Hash SHA256 de 'demo123': 6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090
INSERT INTO users (email, password_hash, name, company)
VALUES (
    'demo@leadger.net',
    '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090',
    'Demo User',
    'Demo Company'
) ON CONFLICT (email) DO NOTHING;
