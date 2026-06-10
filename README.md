# DetectAI

A full-stack web application for detecting AI-generated text and humanizing it. The detector runs a multi-layer statistical analysis engine; the humanizer rewrites flagged text using the Claude API to make it read as naturally human-written.

---

## Features

### Detector
Analyzes text across nine independent metrics and combines them into a single 0–100 AI probability score:

| Metric | Weight | What it measures |
|---|---|---|
| AI Phrase Density | 24% | 160+ high-confidence AI-signature phrases |
| Sentence Burstiness | 20% | Coefficient of variation in sentence lengths |
| Transition Word Density | 10% | Overuse of formal connectors |
| Contraction Absence | 9% | AI rarely uses contractions in formal prose |
| Personal Voice | 9% | First-person pronoun ratio |
| Formality Level | 8% | Overly academic vocabulary |
| Sentence Openers | 7% | Repetitive AI framing patterns |
| Lexical Diversity (MATTR) | 7% | Moving Average Type-Token Ratio |
| Paragraph Coherence | 6% | Inter-paragraph cosine similarity via TF-IDF |

A nonlinear calibration step stretches scores away from 50 to improve discrimination. Sentence-level scoring is also available, highlighting which sentences contributed most to the AI signal.

Verdicts: **Human Written** · **Likely Human** · **Uncertain** · **Likely AI** · **AI Generated**

### Humanizer
Three intensity modes powered by the Claude API:

- **Subtle** — removes AI phrases, minimal structural changes
- **Balanced** — full rewrite with sentence variety, contractions, and personal voice
- **Aggressive** — complete restructure; same ideas, entirely new expression

The humanizer targets GPTZero, Originality.ai, Turnitin, Copyleaks, and similar detectors.

---

## Tech Stack

**Backend**
- Python 3.11+
- FastAPI + Uvicorn
- NLTK (tokenization, stopwords)
- scikit-learn (TF-IDF, cosine similarity)
- NumPy
- Anthropic SDK (Claude API)

**Frontend**
- Next.js 14 (App Router)
- React 18 + TypeScript
- Tailwind CSS
- Framer Motion
- Lucide React

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- An [Anthropic API key](https://console.anthropic.com/) (required only for the Humanizer)

### 1. Clone the repository

```bash
git clone https://github.com/Deibyd07/Detector-IA.git
cd Detector-IA
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create the environment file:

```bash
cp .env.example .env
```

Open `.env` and add your Anthropic API key:

```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
FRONTEND_URL=http://localhost:3000
```

Start the API server:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:3000`.

### 4. One-command launch (Windows)

```powershell
.\start.ps1
```

This opens both servers in separate PowerShell windows.

---

## API Reference

### `POST /api/v1/detect`

Analyzes text and returns an AI probability score.

**Request body**
```json
{
  "text": "Your text here..."
}
```

**Response**
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

Rewrites AI-generated text to sound human.

**Request body**
```json
{
  "text": "Your AI-generated text here...",
  "intensity": "balanced"
}
```

`intensity` accepts `"subtle"`, `"balanced"`, or `"aggressive"`.

**Response**
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

## Project Structure

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
│   │   │   ├── detector.py       # Detection engine
│   │   │   ├── humanizer.py      # Claude-powered rewriter
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

## Notes

- The detector works without an API key. Only the Humanizer requires `ANTHROPIC_API_KEY`.
- Accuracy improves significantly with texts of 150+ words. Short texts return a `Low` confidence rating.
- The humanizer uses `claude-opus-4-7` for best rewriting quality.
