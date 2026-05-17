# Bob Onboarding Accelerator

## Contexto del proyecto

Estoy construyendo una herramienta llamada **Bob Onboarding Accelerator** para una hackathon de IBM Bob. La herramienta permite que cualquier desarrollador entienda un repositorio de código desconocido en menos de 5 minutos, usando IBM Bob como motor de análisis.

Quiero que me ayudes a construir este proyecto de principio a fin. Tú (Bob) eres el protagonista: sin ti, la herramienta no funciona.

---

## El problema que resuelve

Cuando un desarrollador nuevo entra a un proyecto, tarda entre 2 y 5 días solo en entender la arquitectura, los flujos clave y dónde tocar el código. Esto es costoso y frustrante. Esta herramienta elimina ese tiempo muerto.

---

## Cómo funciona

1. El usuario pega una URL de un repositorio GitHub en la interfaz web.
2. El backend clona el repo y extrae el contenido de los archivos relevantes.
3. Se le envía ese contenido a Bob con prompts específicos.
4. Bob devuelve: un diagrama de arquitectura, los flujos clave del sistema, y una guía de onboarding completa.
5. El frontend muestra todo eso de forma visual e interactiva.

---

## Stack tecnológico

- **Backend:** Python 3.11 + FastAPI
- **Frontend:** React 18 + Vite
- **Diagramas:** Mermaid.js
- **Motor de IA:** IBM Bob (tú)
- **Clonado de repos:** GitPython o subprocess con `git clone --depth=1`
- **Estilos:** Tailwind CSS

---

## Estructura de carpetas objetivo

```
bob-onboarding/
├── backend/
│   ├── main.py
│   ├── repo_reader.py
│   ├── bob_client.py
│   └── prompt_templates.py
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── api.js
│       └── components/
│           ├── RepoInput.jsx
│           ├── ArchDiagram.jsx
│           ├── FlowCards.jsx
│           └── GuidePanel.jsx
├── requirements.txt
├── package.json
└── README.md
```

---

## Archivos que necesito que construyas

### `backend/repo_reader.py`

Función `clone_and_read(repo_url: str) -> dict` que:

- Clona el repo con `git clone --depth=1` en `/tmp/{repo_name}`
- Recorre todos los archivos ignorando: `.git/`, `node_modules/`, `__pycache__/`, `.env`, archivos binarios
- Lee el contenido de cada archivo con un límite de 3000 caracteres por archivo
- Devuelve un dict `{ruta_relativa: contenido}`
- Limpia el directorio temporal después de leer

### `backend/prompt_templates.py`

Tres templates de prompt listos para pasarle a Bob:

**PROMPT_ARCHITECTURE:** Le pide a Bob que devuelva SOLO un bloque Mermaid `graph LR` con los módulos principales y sus relaciones. Sin texto adicional, solo el bloque mermaid.

**PROMPT_FLOWS:** Le pide a Bob que identifique los 3 flujos más importantes del sistema y los devuelva en JSON con este formato exacto:
```json
{
  "flows": [
    {
      "name": "nombre del flujo",
      "description": "qué hace en una oración",
      "steps": ["paso 1", "paso 2", "paso 3"],
      "files": ["archivo_relevante.py"]
    }
  ]
}
```
Solo JSON, sin markdown ni texto extra.

**PROMPT_GUIDE:** Le pide a Bob que genere una guía de onboarding con estas secciones exactas:
1. ¿Qué hace este proyecto? (máximo 3 oraciones)
2. Cómo correrlo localmente (pasos exactos con comandos)
3. Los 5 archivos más importantes y por qué cada uno importa
4. Gotchas o cosas no obvias que alguien nuevo debe saber
5. Por dónde empezar si quiero hacer mi primera contribución

### `backend/bob_client.py`

Función async `ask_bob(prompt: str) -> str` que:

- Hace una llamada HTTP POST al endpoint de IBM Bob
- Maneja errores de red con retry (máximo 3 intentos)
- Devuelve el texto de la respuesta como string
- Tiene un timeout de 60 segundos

> **Nota:** Deja el endpoint y el API key como variables de entorno: `BOB_API_ENDPOINT` y `BOB_API_KEY`

### `backend/main.py`

API FastAPI con:

- `POST /analyze` — recibe `{"url": "https://github.com/..."}`, llama a `clone_and_read`, luego llama a Bob 3 veces (architecture, flows, guide) usando `asyncio.gather` para hacerlo en paralelo, y devuelve `{architecture_mermaid, flows, guide}`
- `GET /health` — devuelve `{"status": "ok"}`
- CORS habilitado para `http://localhost:5173`
- Manejo de errores con respuestas HTTP claras (400 si la URL es inválida, 500 si Bob falla)

### `frontend/src/components/RepoInput.jsx`

Componente con:

- Un campo de texto para pegar la URL del repo
- Un botón "Analizar con Bob"
- Estado de loading con mensaje "Bob está leyendo el repositorio..."
- Validación básica: la URL debe empezar con `https://github.com/`
- Props: `onSubmit(url)`, `loading: boolean`

### `frontend/src/components/ArchDiagram.jsx`

Componente que:

- Recibe `mermaid: string` con el diagrama generado por Bob
- Renderiza el diagrama usando la librería `mermaid` (npm)
- Muestra un título "Arquitectura del proyecto"
- Maneja el caso en que el string de mermaid sea inválido mostrando un mensaje de error amigable

### `frontend/src/components/FlowCards.jsx`

Componente que:

- Recibe `flows: array` con los flujos que devolvió Bob
- Muestra cada flujo en una card con: nombre, descripción, lista numerada de pasos, y los archivos involucrados como badges
- Diseño en grid de 3 columnas en desktop, 1 columna en móvil

### `frontend/src/components/GuidePanel.jsx`

Componente que:

- Recibe `guide: string` con el texto de la guía generada por Bob
- Renderiza el markdown usando `react-markdown`
- Muestra un botón "Copiar guía" que copia el texto al clipboard

### `frontend/src/App.jsx`

Componente principal que:

- Maneja el estado global: `result`, `loading`, `error`
- Llama a `POST /analyze` al hacer submit
- Muestra `RepoInput` siempre arriba
- Debajo del input, si hay resultado, muestra `ArchDiagram`, `FlowCards` y `GuidePanel` en ese orden
- Si hay error, muestra un mensaje claro

### `frontend/src/api.js`

Función `analyzeRepo(url)` que hace el fetch al backend y maneja errores.

---

## Requisitos no funcionales

- El backend debe correr con `uvicorn main:app --reload` en el puerto 8000
- El frontend debe correr con `npm run dev` en el puerto 5173
- Todo debe funcionar con un repo público de GitHub sin autenticación
- El tiempo total de análisis no debe superar 90 segundos
- Si Bob devuelve un Mermaid inválido, el diagrama simplemente no se muestra (no rompe la app)

---

## Archivos de configuración que necesito

### `requirements.txt`
```
fastapi
uvicorn
gitpython
httpx
python-dotenv
```

### `package.json` (frontend)
Dependencias: `react`, `react-dom`, `react-markdown`, `mermaid`
Dev: `vite`, `@vitejs/plugin-react`, `tailwindcss`, `autoprefixer`, `postcss`

### `.env.example`
```
BOB_API_ENDPOINT=https://api.ibm.com/bob/v1/chat
BOB_API_KEY=tu_api_key_aqui
```

---

## Orden de construcción sugerido

1. Empieza por `repo_reader.py` y pruébalo con `https://github.com/tiangolo/fastapi`
2. Luego `prompt_templates.py` con los tres prompts
3. Luego `bob_client.py`
4. Luego `main.py` y prueba el endpoint con curl
5. Finalmente el frontend, empezando por `App.jsx` y `RepoInput.jsx`

---

## Lo que necesito de ti ahora

**Construye todos los archivos listados arriba, uno por uno, con código completo y listo para correr.** Empieza por el backend. Cuando termines cada archivo, pregúntame si quiero ajustar algo antes de continuar con el siguiente.

Si encuentras algo ambiguo o que se puede mejorar, dímelo y propón la mejora. Eres mi partner de desarrollo en esta hackathon.
