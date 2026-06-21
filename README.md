# Repo Accelerate

Repo Accelerate convierte cualquier repositorio público de GitHub en un punto
de partida técnico claro. Analiza la base de código con Google Gemini y genera
un mapa de arquitectura, los flujos principales del sistema y una guía práctica
de incorporación para desarrolladores.

La interfaz y los resultados pueden generarse en español o inglés.

## Qué genera

- **Mapa de arquitectura:** diagrama Mermaid con los principales módulos,
  servicios y relaciones del repositorio.
- **Flujos clave:** tres recorridos importantes del sistema con descripción,
  pasos y archivos relacionados.
- **Guía de incorporación:** documento Markdown con propósito, tecnologías,
  instalación, estructura, archivos importantes y recomendaciones iniciales.
- **Resultados bilingües:** el idioma seleccionado en la interfaz se envía a la
  API y se aplica a las respuestas de Gemini.

## Experiencia de usuario

La aplicación incluye:

- Analizador de repositorios públicos de GitHub.
- Workspace de resultados con pestañas accesibles para Arquitectura, Flujos y
  Guía.
- Cambio inmediato entre español e inglés, persistido en `localStorage`.
- Aviso para volver a analizar cuando el resultado existente está en otro
  idioma.
- Renderizado seguro de Mermaid con zoom, ajuste de vista, reintento,
  visualización del código fuente y descarga SVG.
- Vista `/demo` con funciones, estadísticas, casos de uso y repositorios de
  ejemplo.
- Diseño responsive para escritorio y dispositivos móviles.

## Stack tecnológico

### Frontend

- React 18
- Vite 5
- Tailwind CSS
- Mermaid
- react-i18next
- Lucide React
- React Markdown
- Vitest, Testing Library y Playwright

### Backend

- Python 3.11+
- FastAPI
- Google Gemini mediante `google-genai`
- GitPython
- Pydantic
- Pytest

## Cómo funciona

1. El usuario introduce una URL pública con formato
   `https://github.com/{owner}/{repository}`.
2. El frontend envía la URL y el idioma seleccionado a `POST /analyze`.
3. El backend clona temporalmente el repositorio y lee sus archivos relevantes.
4. Se ejecutan en paralelo tres solicitudes a Gemini:
   arquitectura, flujos y guía.
5. La API valida y estructura las respuestas.
6. El frontend presenta los resultados dentro del workspace.

```text
GitHub URL + idioma
        |
        v
 React / Vite frontend
        |
        | POST /analyze
        v
    FastAPI API
        |
        +----> lectura temporal del repositorio
        |
        +----> prompt de arquitectura ----+
        +----> prompt de flujos ----------+--> Google Gemini
        +----> prompt de guía ------------+
        |
        v
 Mermaid + flujos JSON + guía Markdown
```

## Estructura del repositorio

```text
.
├── bob-onboarding/
│   ├── backend/
│   │   ├── main.py                 # API FastAPI y modelos
│   │   ├── gemini_client.py        # Cliente de Google Gemini
│   │   ├── prompt_templates.py     # Prompts bilingües
│   │   ├── repo_reader.py          # Clonado y lectura segura
│   │   └── tests/                  # Pruebas del backend
│   ├── frontend/
│   │   ├── src/
│   │   │   ├── components/         # Entrada, Mermaid, flujos y guía
│   │   │   ├── pages/              # Analizador y demostración
│   │   │   ├── i18n.js             # Recursos español/inglés
│   │   │   ├── api.js              # Cliente de la API
│   │   │   └── App.jsx             # Navegación y selector de idioma
│   │   └── package.json
│   ├── docs/                       # Referencia de API y pruebas
│   ├── e2e/                        # Pruebas de navegador
│   ├── DEVELOPMENT.md
│   ├── DEPLOYMENT.md
│   └── README.md
├── render.yaml                     # Blueprint del backend en Render
├── render-build.sh
├── requirements.txt
└── Procfile
```

## Desarrollo local

### Requisitos

- Python 3.11 o superior
- Node.js 18 o superior
- npm
- Git
- Una API key de Google Gemini

### 1. Configurar el backend

Desde la raíz del repositorio:

```powershell
cd bob-onboarding
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item backend\.env.example backend\.env
```

Edita `bob-onboarding/backend/.env`:

```dotenv
GEMINI_API_KEY=tu_api_key
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development
```

Puedes crear una API key desde
[Google AI Studio](https://aistudio.google.com/app/apikey).

Inicia la API:

```powershell
python -m uvicorn backend.main:app --reload --port 8000
```

Servicios disponibles:

- API: `http://127.0.0.1:8000`
- OpenAPI: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

### 2. Configurar el frontend

En otra terminal:

```powershell
cd bob-onboarding\frontend
npm install
```

Para usar el backend local, crea `frontend/.env.local`:

```dotenv
VITE_API_URL=http://127.0.0.1:8000
```

Inicia Vite:

```powershell
npm run dev
```

Abre:

- Analizador: `http://localhost:5173`
- Demostración: `http://localhost:5173/demo`

## API

### Estado del servicio

```http
GET /health
```

Respuesta:

```json
{
  "status": "ok",
  "version": "3.0.0"
}
```

### Analizar un repositorio

```http
POST /analyze
Content-Type: application/json
```

Solicitud:

```json
{
  "url": "https://github.com/owner/repository",
  "language": "es"
}
```

| Campo | Requerido | Descripción |
| --- | --- | --- |
| `url` | Sí | URL pública de un repositorio de GitHub |
| `language` | No | `en` o `es`; utiliza `en` por defecto |

Respuesta simplificada:

```json
{
  "architecture_mermaid": "flowchart LR\nA[Frontend] --> B[API]",
  "flows": [
    {
      "name": "Flujo de solicitud",
      "description": "Cómo se procesa una solicitud",
      "steps": ["Recibir solicitud", "Ejecutar servicio", "Responder"],
      "files": ["backend/main.py"]
    }
  ],
  "guide": "## 1. ¿Qué hace este proyecto?",
  "repository_url": "https://github.com/owner/repository",
  "files_analyzed": 42,
  "language": "es"
}
```

Consulta la referencia completa en
[`bob-onboarding/docs/API_DOCUMENTATION.md`](bob-onboarding/docs/API_DOCUMENTATION.md).

## Mermaid y seguridad

El frontend acepta exclusivamente diagramas que comienzan con `flowchart` o
`graph`. Antes de renderizar:

- valida la sintaxis con `mermaid.parse()`;
- utiliza `securityLevel: "strict"`;
- desactiva etiquetas HTML;
- evita aplicar resultados de renders obsoletos;
- mantiene el contenedor montado durante carga, éxito y error.

El prompt de arquitectura limita el diagrama a diez módulos, utiliza etiquetas
cortas y solicita `flowchart LR` sin HTML ni estilos ejecutables.

## Internacionalización

Las traducciones se encuentran en
`bob-onboarding/frontend/src/i18n.js`.

- Idiomas disponibles: `en` y `es`.
- Detección inicial: idioma guardado y luego idioma del navegador.
- Persistencia: clave `repoAccelerateLanguage` de `localStorage`.
- Metadatos: se actualizan `<html lang>`, el título y la descripción.
- API: el frontend envía `language` en cada análisis.
- Gemini: los tres prompts solicitan la respuesta en el idioma seleccionado,
  conservando rutas, comandos e identificadores técnicos.

## Pruebas y validación

### Frontend

```powershell
cd bob-onboarding\frontend
npm test -- --run
npm run build
```

Pruebas cubiertas:

- cliente HTTP y envío del idioma;
- cambio y persistencia de idioma;
- conservación de resultados al cambiar de idioma;
- navegación del workspace;
- render válido e inválido de Mermaid;
- controles de reintento y visualización.

### Backend

Desde `bob-onboarding/`:

```powershell
python -m pytest backend/tests
```

### End-to-end

```powershell
cd bob-onboarding
npx playwright test
```

Consulta instrucciones adicionales en
[`bob-onboarding/docs/TESTING_GUIDE.md`](bob-onboarding/docs/TESTING_GUIDE.md).

## Despliegue

El repositorio conserva los nombres técnicos y las URLs del despliegue actual,
aunque el nombre visible del producto sea Repo Accelerate.

### Backend en Render

El archivo raíz `render.yaml` configura:

- build: `chmod +x render-build.sh && ./render-build.sh`;
- inicio:
  `cd bob-onboarding/backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT`;
- variable secreta obligatoria: `GEMINI_API_KEY`;
- Python 3.11.7.

Proceso:

1. Conecta el repositorio en Render.
2. Crea un Blueprint usando `render.yaml`.
3. Configura `GEMINI_API_KEY`.
4. Despliega y comprueba `/health`.

### Frontend

Configura durante el despliegue:

```dotenv
VITE_API_URL=https://tu-backend.example.com
```

Después ejecuta:

```powershell
cd bob-onboarding\frontend
npm install
npm run build
```

El artefacto de producción se genera en `frontend/dist/`.

Consulta [`DEPLOYMENT.md`](DEPLOYMENT.md) y
[`bob-onboarding/DEPLOYMENT.md`](bob-onboarding/DEPLOYMENT.md) para más
detalles operativos.

## Solución de problemas

### El frontend no conecta con la API

- Comprueba que FastAPI esté activo en el puerto `8000`.
- Revisa `VITE_API_URL`.
- Reinicia Vite después de modificar variables de entorno.
- Comprueba la respuesta de `GET /health`.

### Gemini devuelve un error

- Confirma que `GEMINI_API_KEY` esté definida en `backend/.env` o en Render.
- Revisa que la clave siga activa en Google AI Studio.
- Consulta los logs del backend para identificar errores de cuota o red.

### Mermaid no puede mostrar un resultado

- Usa **Reintentar** dentro de la pestaña Arquitectura.
- Abre **Ver código** para inspeccionar la respuesta generada.
- Repite el análisis si Gemini produjo una sintaxis no válida.
- El frontend rechazará deliberadamente tipos distintos de `graph` y
  `flowchart`.

### El análisis tarda demasiado

El tiempo depende del tamaño del repositorio, la cantidad de archivos
relevantes y la latencia de Gemini. Los repositorios grandes pueden superar el
intervalo habitual de 30–90 segundos.

## Documentación adicional

- [Guía principal de la aplicación](bob-onboarding/README.md)
- [Desarrollo](bob-onboarding/DEVELOPMENT.md)
- [Despliegue](bob-onboarding/DEPLOYMENT.md)
- [Referencia de la API](bob-onboarding/docs/API_DOCUMENTATION.md)
- [Pruebas](bob-onboarding/docs/TESTING_GUIDE.md)
- [Prueba rápida](bob-onboarding/QUICK_TEST_GUIDE.md)

## Soporte

Para reportar un problema, abre un issue en
[GitHub](https://github.com/Chriss227/IBM-BOB/issues) e incluye los pasos para
reproducirlo, el entorno utilizado y los logs relevantes sin secretos.
