# 🚀 Guía Completa de Deployment en Render

## Problema Resuelto

El error de Rust/Cargo ocurría porque:
1. Render usaba Python 3.14.3 (muy nuevo)
2. `pydantic-core` necesitaba compilarse con Rust
3. El sistema de archivos de Render es read-only para Cargo

## Solución Implementada

✅ **Python 3.11.7** - Versión estable con wheels pre-compilados
✅ **Dependencias compatibles** - Sin necesidad de compilación
✅ **Build script optimizado** - Instalación rápida y confiable

## Archivos de Configuración

### 1. [`runtime.txt`](runtime.txt:1)
Especifica Python 3.11.7

### 2. [`.python-version`](.python-version:1)
Backup para especificar la versión de Python

### 3. [`requirements-prod.txt`](requirements-prod.txt:1)
Solo dependencias de producción (sin testing/dev tools)

### 4. [`render-build.sh`](render-build.sh:1)
Script de build optimizado

### 5. [`render.yaml`](render.yaml:1)
Configuración Blueprint de Render

## Pasos para Deployar

### 1. Subir Cambios a GitHub

```bash
git add .
git commit -m "Fix Render deployment - Python 3.11.7 with pre-built wheels"
git push origin main
```

### 2. Deployar en Render

#### Opción A: Blueprint (Recomendado) ⭐

1. Ve a https://dashboard.render.com/
2. Click **"New +"** → **"Blueprint"**
3. Conecta tu repositorio GitHub
4. Render detectará automáticamente [`render.yaml`](render.yaml:1)
5. Agrega las variables de entorno:
   ```
   BOB_API_ENDPOINT=https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29
   BOB_API_KEY=tu_api_key_aqui
   ```
6. Click **"Apply"**

#### Opción B: Manual

1. Ve a https://dashboard.render.com/
2. Click **"New +"** → **"Web Service"**
3. Conecta tu repositorio
4. Configura:
   - **Name**: `bob-onboarding-backend`
   - **Region**: `Oregon (US West)`
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `chmod +x render-build.sh && ./render-build.sh`
   - **Start Command**: `cd bob-onboarding/backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Agrega variables de entorno (ver arriba)
6. Click **"Create Web Service"**

### 3. Verificar el Deploy

Una vez completado el build:

1. Render te dará una URL como: `https://bob-onboarding-backend.onrender.com`
2. Prueba el health endpoint:
   ```bash
   curl https://tu-url.onrender.com/health
   ```
3. Deberías ver:
   ```json
   {"status":"ok","version":"1.0.0"}
   ```

### 4. Conectar con el Frontend

Actualiza la URL del backend en tu frontend de Vercel:

```javascript
// En frontend/src/api.js
const API_BASE_URL = 'https://tu-url.onrender.com';
```

## Arquitectura del Sistema

```
┌─────────────────┐
│   Frontend      │
│   (Vercel)      │
│   React + Vite  │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│   Backend       │
│   (Render)      │
│   FastAPI       │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│   IBM Bob AI    │
│   watsonx.ai    │
└─────────────────┘
```

## Variables de Entorno Requeridas

### Backend (Render)

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `BOB_API_ENDPOINT` | URL del API de IBM Bob | `https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29` |
| `BOB_API_KEY` | API Key de IBM Bob | `tu_api_key_secreto` |

### Frontend (Vercel)

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `VITE_API_URL` | URL del backend en Render | `https://bob-onboarding-backend.onrender.com` |

## Troubleshooting

### Error: "Python version not found"
- Verifica que [`runtime.txt`](runtime.txt:1) tenga `python-3.11.7`
- Render soporta: 3.8, 3.9, 3.10, 3.11, 3.12

### Error: "Build failed - Rust compilation"
- ✅ Ya resuelto con Python 3.11.7 y dependencias compatibles
- Si persiste, verifica [`requirements-prod.txt`](requirements-prod.txt:1)

### Error: "Module not found"
- Verifica que todas las dependencias estén en [`requirements-prod.txt`](requirements-prod.txt:1)
- El build script instala desde este archivo

### Error: "Environment variables not set"
1. Ve a tu servicio en Render Dashboard
2. Click en **"Environment"**
3. Agrega `BOB_API_ENDPOINT` y `BOB_API_KEY`
4. Click **"Save Changes"**
5. Render redesplegará automáticamente

### Error: "Service won't start"
- Revisa los logs en Render Dashboard
- Verifica que el comando de inicio sea correcto
- Asegúrate que el directorio `bob-onboarding/backend` exista

## Monitoreo

### Logs en Tiempo Real
```bash
# En Render Dashboard
1. Ve a tu servicio
2. Click en "Logs"
3. Verás logs en tiempo real
```

### Health Check
```bash
curl https://tu-url.onrender.com/health
```

### Test del API
```bash
curl -X POST https://tu-url.onrender.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/tiangolo/fastapi"}'
```

## Costos

- **Render Free Tier**: 
  - 750 horas/mes gratis
  - El servicio se duerme después de 15 min de inactividad
  - Primera request toma ~30 segundos (cold start)

- **Render Starter ($7/mes)**:
  - Siempre activo (sin cold starts)
  - Mejor para producción

## Próximos Pasos

1. ✅ Deploy exitoso en Render
2. 🔄 Conectar frontend en Vercel con backend en Render
3. 🧪 Probar el flujo completo
4. 📊 Configurar monitoreo (opcional)
5. 🚀 ¡Listo para usar!

---

**¿Problemas?** Revisa los logs en Render Dashboard o abre un issue en GitHub.