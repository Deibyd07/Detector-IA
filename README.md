# DetectAI

Aplicación web completa para detectar texto generado por IA y humanizarlo. El detector ejecuta un motor de análisis estadístico multicapa; el humanizador reescribe el texto marcado usando la API de Claude para que suene naturalmente humano.

---

## Funcionalidades

### Detector
Analiza el texto en nueve métricas independientes y las combina en un puntaje de probabilidad IA del 0 al 100:

| Métrica | Peso | Qué mide |
|---|---|---|
| Densidad de frases IA | 24% | Más de 160 frases características de la IA |
| Burstiness de oraciones | 20% | Coeficiente de variación en la longitud de oraciones |
| Densidad de conectores | 10% | Abuso de conectores formales |
| Ausencia de contracciones | 9% | La IA rara vez usa contracciones en prosa formal |
| Voz personal | 9% | Proporción de pronombres en primera persona |
| Nivel de formalidad | 8% | Vocabulario excesivamente académico |
| Diversidad de openers | 7% | Patrones de inicio de oración repetitivos |
| Diversidad léxica (MATTR) | 7% | Moving Average Type-Token Ratio |
| Coherencia entre párrafos | 6% | Similitud coseno entre párrafos vía TF-IDF |

Un paso de calibración no lineal estira los puntajes alejándolos del centro para mejorar la discriminación. También se calcula un puntaje por oración, resaltando cuáles contribuyeron más a la señal IA.

Veredictos: **Escrito por humano** · **Probablemente humano** · **Incierto** · **Probablemente IA** · **Generado por IA**

### Humanizador
Tres modos de intensidad impulsados por la API de Claude:

- **Sutil** — elimina frases IA con cambios estructurales mínimos
- **Equilibrado** — reescritura completa con variedad de oraciones, contracciones y voz personal
- **Agresivo** — reestructuración total; mismas ideas, expresión completamente nueva

El humanizador apunta a evadir detectores como GPTZero, Originality.ai, Turnitin y Copyleaks.

---

## Stack tecnológico

**Backend**
- Python 3.11+
- FastAPI + Uvicorn
- NLTK (tokenización, stopwords)
- scikit-learn (TF-IDF, similitud coseno)
- NumPy
- Anthropic SDK (API de Claude)

**Frontend**
- Next.js 14 (App Router)
- React 18 + TypeScript
- Tailwind CSS
- Framer Motion
- Lucide React

---

## Cómo empezar

### Requisitos previos

- Python 3.11+
- Node.js 18+
- Una [API key de Anthropic](https://console.anthropic.com/) (solo necesaria para el Humanizador)

### 1. Clonar el repositorio

```bash
git clone https://github.com/Deibyd07/Detector-IA.git
cd Detector-IA
```

### 2. Configurar el backend

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

Crear el archivo de entorno:

```bash
cp .env.example .env
```

Abrir `.env` y agregar la API key de Anthropic:

```env
ANTHROPIC_API_KEY=sk-ant-tu-clave-aqui
FRONTEND_URL=http://localhost:3000
```

Iniciar el servidor de la API:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

La API estará disponible en `http://localhost:8000`. Documentación interactiva en `http://localhost:8000/docs`.

### 3. Configurar el frontend

```bash
cd frontend
npm install
npm run dev
```

La aplicación estará disponible en `http://localhost:3000`.

### 4. Inicio con un solo comando (Windows)

```powershell
.\start.ps1
```

Abre ambos servidores en ventanas de PowerShell separadas.

---

## Referencia de la API

### `POST /api/v1/detect`

Analiza el texto y devuelve un puntaje de probabilidad IA.

**Cuerpo de la petición**
```json
{
  "text": "Tu texto aquí..."
}
```

**Respuesta**
```json
{
  "score": 84.2,
  "verdict": "AI Generated",
  "confidence": "High",
  "breakdown": { ... },
  "ai_phrases_found": ["furthermore", "it's worth noting"],
  "sentences": [ { "text": "...", "score": 91.0 } ],
  "stats": {
    "word_count": 312,
    "sentence_count": 18,
    "avg_sentence_length": 17.3,
    "burstiness": 0.24,
    "mattr": 0.78,
    "flesch_reading_ease": 55.1,
    "ai_phrases_count": 5,
    "personal_pronoun_ratio": 0.002
  },
  "warning": null
}
```

### `POST /api/v1/humanize`

Reescribe texto generado por IA para que suene humano.

**Cuerpo de la petición**
```json
{
  "text": "Tu texto generado por IA aquí...",
  "intensity": "balanced"
}
```

`intensity` acepta `"subtle"`, `"balanced"` o `"aggressive"`.

**Respuesta**
```json
{
  "original": "...",
  "humanized": "...",
  "changes_made": [
    "Removed AI tells → replaced with natural flow transitions",
    "Added 4 natural contractions",
    "Restructured sentence count (12 → 17) for natural burstiness"
  ],
  "estimated_ai_score": 21.4
}
```

### `GET /health`

```json
{ "status": "ok", "version": "1.0.0" }
```

---

## Estructura del proyecto

```
Detector-IA/
├── backend/
│   ├── app/
│   │   ├── api/routes/
│   │   │   ├── detect.py
│   │   │   └── humanize.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── models/
│   │   │   └── schemas.py
│   │   ├── services/
│   │   │   ├── detector.py         # Motor de detección
│   │   │   ├── humanizer.py        # Reescritor con Claude
│   │   │   └── humanizer_rules.py
│   │   └── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   │   ├── detector/
│   │   │   └── humanizer/
│   │   ├── contexts/
│   │   └── lib/
│   ├── package.json
│   └── tailwind.config.ts
├── start.ps1
└── README.md
```

---

## Notas

- El detector funciona sin API key. Solo el Humanizador requiere `ANTHROPIC_API_KEY`.
- La precisión mejora significativamente con textos de 150 palabras o más. Los textos cortos devuelven confianza `Low`.
- El humanizador usa `claude-opus-4-7` para obtener la mejor calidad de reescritura.
