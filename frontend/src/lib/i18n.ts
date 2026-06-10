export type Lang = "en" | "es";

export const translations = {
  en: {
    // Navbar
    nav_detector: "Detector",
    nav_humanizer: "Humanizer",
    nav_badge: "Multi-layer detection",

    // Hero
    hero_badge: "Multi-layer Statistical Engine",
    hero_title1: "Detect & Humanize",
    hero_title2: "AI-Generated Text",
    hero_desc:
      "Professional-grade AI detection using burstiness analysis, AI phrase fingerprinting, lexical diversity scoring, and 5 more signals — plus a Claude-powered humanizer that passes every detector.",
    hero_btn_analyze: "Analyze Text",
    hero_btn_humanize: "Humanize Text",

    // Feature pills
    feat_burstiness: "Burstiness Analysis",
    feat_phrase: "AI Phrase Fingerprinting",
    feat_mattr: "MATTR Lexical Scoring",
    feat_coherence: "Paragraph Coherence",
    feat_claude: "Claude Humanizer",
    feat_intensity: "3 Intensity Levels",

    // Footer
    footer_powered: "DetectAI — Powered by FastAPI + Claude",
    footer_burstiness: "Burstiness Analysis",
    footer_phrase: "AI Phrase Detection",
    footer_claude: "Claude Humanizer",

    // DetectorPanel
    detector_placeholder: `Paste or type any text here to analyze whether it was written by an AI or a human.\n\nFor best results, use at least 150 words. The detector uses multiple algorithms including sentence burstiness analysis, AI phrase pattern matching, lexical diversity scoring, formality index, and paragraph coherence analysis.`,
    detector_words: "words",
    detector_chars: "chars",
    detector_add_words: (n: number) => `Add ${n} more words for reliable detection accuracy`,
    detector_btn_analyzing: "Analyzing…",
    detector_btn_analyze: "Analyze Text",
    detector_btn_humanize: "Humanize",
    detector_error_title: "Detection Failed",
    detector_error_fallback: "Failed to connect to the detection API.",
    detector_empty_title: "Awaiting Analysis",
    detector_empty_sub: "Paste text and click Analyze",
    detector_loading_title: "Running Analysis",
    detector_loading_sub: "Checking burstiness, phrase patterns, coherence…",
    detector_result_title: "Detection Result",
    detector_copy: "Copy result",
    detector_copied: "Copied!",
    detector_metrics: "Metric Breakdown",
    detector_signatures: (n: number) => `AI Signatures Detected (${n})`,
    detector_stats: "Text Statistics",
    stat_words: "Words",
    stat_sentences: "Sentences",
    stat_avg_len: "Avg. sent. length",
    stat_burstiness: "Burstiness",
    stat_mattr: "MATTR",
    stat_flesch: "Flesch score",
    detector_sentences: "Sentence-level Analysis",
    detector_copy_result_text: (score: number, verdict: string, confidence: string) =>
      `AI Detection Result\nScore: ${score}% AI\nVerdict: ${verdict}\nConfidence: ${confidence}`,
    detector_warning_short: "For best accuracy, provide at least 150 words. Short texts reduce reliability.",

    // Verdict & confidence (from backend)
    verdict_human_written: "Human Written",
    verdict_likely_human: "Likely Human",
    verdict_uncertain: "Uncertain",
    verdict_likely_ai: "Likely AI",
    verdict_ai_generated: "AI Generated",
    confidence_low: "Low",
    confidence_medium: "Medium",
    confidence_high: "High",
    confidence_very_high: "Very High",

    // ScoreGauge
    gauge_probability: "AI PROBABILITY",
    gauge_confidence: "confidence",

    // MetricBar
    metric_weight: "weight",
    metric_burstiness: "Sentence Variation",
    metric_ai_phrases: "AI Phrase Patterns",
    metric_personal_voice: "Personal Voice",
    metric_sentence_structure: "Lexical Diversity",
    metric_transition_density: "Transition Words",
    metric_formality: "Formality Level",
    metric_coherence: "Paragraph Coherence",
    metric_contraction: "Contraction Use",
    metric_opener_diversity: "Sentence Openers",

    // HighlightedText
    highlight_title: "Sentence Analysis",
    highlight_human: "Human",
    highlight_uncertain: "Uncertain",
    highlight_ai: "AI",
    highlight_tooltip: (score: number) => `AI probability: ${score}%`,

    // HumanizerPanel
    humanizer_placeholder: `Paste AI-generated text here to humanize it.\n\nThe rule-based humanizer rewrites your text with natural contractions, varied sentence lengths, personal voice, and removes 200+ AI-signature phrases — no API key needed.`,
    humanizer_mode_label: "Humanization Mode",
    humanizer_mode_rules: "No AI (Rules)",
    humanizer_mode_rules_desc: "Instant · no API key needed",
    humanizer_mode_ai: "Claude AI",
    humanizer_mode_ai_desc: "Best results · requires API key",
    humanizer_intensity_label: "Humanization Intensity",
    intensity_subtle_label: "Subtle",
    intensity_subtle_desc: "Light polish — preserves structure",
    intensity_balanced_label: "Balanced",
    intensity_balanced_desc: "Natural rewrite — best for most cases",
    intensity_aggressive_label: "Aggressive",
    intensity_aggressive_desc: "Full restructure — new expression",
    humanizer_btn_loading: "Humanizing…",
    humanizer_btn_loading_ai: "Humanizing with Claude…",
    humanizer_btn: "Humanize (No AI)",
    humanizer_btn_ai: "Humanize with Claude",
    humanizer_error_title: "Humanization Failed",
    humanizer_error_fallback: "Humanization failed. Try again.",
    humanizer_error_fallback_ai: "Humanization failed. Check your API key.",
    humanizer_empty_title: "Humanized Output",
    humanizer_empty_sub: "Will appear here after processing",
    humanizer_loading_title: "Rewriting…",
    humanizer_loading_title_ai: "Claude is rewriting…",
    humanizer_loading_sub: "Removing AI signatures, adding human voice",
    humanizer_output_label: "Humanized Output",
    humanizer_copy: "Copy",
    humanizer_copied: "Copied!",
    humanizer_score_title: "Detection Score Comparison",
    humanizer_before: "Before",
    humanizer_after: "After",
    humanizer_humanized_label: "Humanized",
    humanizer_score_desc: (score: number) =>
      `Estimated AI score reduced to ${Math.round(score)}% — should pass most AI detectors`,
    humanizer_changes_title: "Changes Applied",
    humanizer_original: "Original",
  },

  es: {
    // Navbar
    nav_detector: "Detector",
    nav_humanizer: "Humanizador",
    nav_badge: "Detección multicapa",

    // Hero
    hero_badge: "Motor Estadístico Multicapa",
    hero_title1: "Detecta y Humaniza",
    hero_title2: "Texto Generado por IA",
    hero_desc:
      "Detección de IA de nivel profesional usando análisis de burstiness, huellas de frases IA, puntuación de diversidad léxica y 5 señales más — más un humanizador basado en Claude que supera cualquier detector.",
    hero_btn_analyze: "Analizar Texto",
    hero_btn_humanize: "Humanizar Texto",

    // Feature pills
    feat_burstiness: "Análisis de Burstiness",
    feat_phrase: "Huellas de Frases IA",
    feat_mattr: "Puntuación Léxica MATTR",
    feat_coherence: "Coherencia de Párrafos",
    feat_claude: "Humanizador Claude",
    feat_intensity: "3 Niveles de Intensidad",

    // Footer
    footer_powered: "DetectAI — Impulsado por FastAPI + Claude",
    footer_burstiness: "Análisis de Burstiness",
    footer_phrase: "Detección de Frases IA",
    footer_claude: "Humanizador Claude",

    // DetectorPanel
    detector_placeholder: `Pega o escribe cualquier texto aquí para analizar si fue escrito por una IA o un humano.\n\nPara mejores resultados, usa al menos 150 palabras. El detector utiliza múltiples algoritmos: análisis de burstiness, coincidencia de patrones de frases IA, puntuación de diversidad léxica, índice de formalidad y análisis de coherencia de párrafos.`,
    detector_words: "palabras",
    detector_chars: "caracteres",
    detector_add_words: (n: number) => `Agrega ${n} palabras más para mayor precisión en la detección`,
    detector_btn_analyzing: "Analizando…",
    detector_btn_analyze: "Analizar Texto",
    detector_btn_humanize: "Humanizar",
    detector_error_title: "Detección Fallida",
    detector_error_fallback: "No se pudo conectar con la API de detección.",
    detector_empty_title: "Esperando Análisis",
    detector_empty_sub: "Pega texto y haz clic en Analizar",
    detector_loading_title: "Ejecutando Análisis",
    detector_loading_sub: "Verificando burstiness, patrones de frases, coherencia…",
    detector_result_title: "Resultado de Detección",
    detector_copy: "Copiar resultado",
    detector_copied: "¡Copiado!",
    detector_metrics: "Desglose de Métricas",
    detector_signatures: (n: number) => `Firmas de IA Detectadas (${n})`,
    detector_stats: "Estadísticas del Texto",
    stat_words: "Palabras",
    stat_sentences: "Oraciones",
    stat_avg_len: "Long. media de oración",
    stat_burstiness: "Burstiness",
    stat_mattr: "MATTR",
    stat_flesch: "Puntuación Flesch",
    detector_sentences: "Análisis por Oración",
    detector_copy_result_text: (score: number, verdict: string, confidence: string) =>
      `Resultado de Detección IA\nPuntuación: ${score}% IA\nVeredicto: ${verdict}\nConfianza: ${confidence}`,
    detector_warning_short: "Para mayor precisión, proporciona al menos 150 palabras. Los textos cortos reducen la fiabilidad.",

    // Verdict & confidence (from backend)
    verdict_human_written: "Escrito por Humano",
    verdict_likely_human: "Probablemente Humano",
    verdict_uncertain: "Incierto",
    verdict_likely_ai: "Probablemente IA",
    verdict_ai_generated: "Generado por IA",
    confidence_low: "Baja",
    confidence_medium: "Media",
    confidence_high: "Alta",
    confidence_very_high: "Muy Alta",

    // ScoreGauge
    gauge_probability: "PROB. IA",
    gauge_confidence: "confianza",

    // MetricBar
    metric_weight: "peso",
    metric_burstiness: "Variación de Oraciones",
    metric_ai_phrases: "Patrones de Frases IA",
    metric_personal_voice: "Voz Personal",
    metric_sentence_structure: "Diversidad Léxica",
    metric_transition_density: "Palabras de Transición",
    metric_formality: "Nivel de Formalidad",
    metric_coherence: "Coherencia de Párrafos",
    metric_contraction: "Uso de Contracciones",
    metric_opener_diversity: "Inicio de Oraciones",

    // HighlightedText
    highlight_title: "Análisis por Oración",
    highlight_human: "Humano",
    highlight_uncertain: "Incierto",
    highlight_ai: "IA",
    highlight_tooltip: (score: number) => `Probabilidad IA: ${score}%`,

    // HumanizerPanel
    humanizer_placeholder: `Pega texto generado por IA aquí para humanizarlo.\n\nEl humanizador elimina más de 200 frases típicas de IA, añade contracciones naturales, varía la longitud de oraciones e inyecta voz personal — sin necesidad de clave API.`,
    humanizer_mode_label: "Modo de Humanización",
    humanizer_mode_rules: "Sin IA (Reglas)",
    humanizer_mode_rules_desc: "Instantáneo · sin clave API",
    humanizer_mode_ai: "Claude IA",
    humanizer_mode_ai_desc: "Mejores resultados · requiere API",
    humanizer_intensity_label: "Intensidad de Humanización",
    intensity_subtle_label: "Sutil",
    intensity_subtle_desc: "Pulido ligero — conserva la estructura",
    intensity_balanced_label: "Equilibrado",
    intensity_balanced_desc: "Reescritura natural — mejor para la mayoría",
    intensity_aggressive_label: "Agresivo",
    intensity_aggressive_desc: "Reestructuración total — nueva expresión",
    humanizer_btn_loading: "Humanizando…",
    humanizer_btn_loading_ai: "Humanizando con Claude…",
    humanizer_btn: "Humanizar (Sin IA)",
    humanizer_btn_ai: "Humanizar con Claude",
    humanizer_error_title: "Humanización Fallida",
    humanizer_error_fallback: "La humanización falló. Inténtalo de nuevo.",
    humanizer_error_fallback_ai: "La humanización falló. Verifica tu clave API.",
    humanizer_empty_title: "Salida Humanizada",
    humanizer_empty_sub: "Aparecerá aquí después de procesar",
    humanizer_loading_title: "Reescribiendo…",
    humanizer_loading_title_ai: "Claude está reescribiendo…",
    humanizer_loading_sub: "Eliminando firmas IA, añadiendo voz humana",
    humanizer_output_label: "Salida Humanizada",
    humanizer_copy: "Copiar",
    humanizer_copied: "¡Copiado!",
    humanizer_score_title: "Comparación de Puntuación de Detección",
    humanizer_before: "Antes",
    humanizer_after: "Después",
    humanizer_humanized_label: "Humanizado",
    humanizer_score_desc: (score: number) =>
      `Puntuación IA estimada reducida a ${Math.round(score)}% — debería pasar la mayoría de detectores`,
    humanizer_changes_title: "Cambios Aplicados",
    humanizer_original: "Original",
  },
} as const;

export type TranslationKey = keyof (typeof translations)["en"];

// ---------------------------------------------------------------------------
// Helpers to translate fixed-value strings that come from the backend
// ---------------------------------------------------------------------------

const VERDICT_MAP: Record<string, "verdict_human_written" | "verdict_likely_human" | "verdict_uncertain" | "verdict_likely_ai" | "verdict_ai_generated"> = {
  "Human Written": "verdict_human_written",
  "Likely Human": "verdict_likely_human",
  "Uncertain": "verdict_uncertain",
  "Likely AI": "verdict_likely_ai",
  "AI Generated": "verdict_ai_generated",
};

const CONFIDENCE_MAP: Record<string, "confidence_low" | "confidence_medium" | "confidence_high" | "confidence_very_high"> = {
  "Low": "confidence_low",
  "Medium": "confidence_medium",
  "High": "confidence_high",
  "Very High": "confidence_very_high",
};

export function translateVerdict(verdict: string, lang: Lang): string {
  const key = VERDICT_MAP[verdict];
  return key ? (translations[lang][key] as string) : verdict;
}

export function translateConfidence(confidence: string, lang: Lang): string {
  const key = CONFIDENCE_MAP[confidence];
  return key ? (translations[lang][key] as string) : confidence;
}

export function translateWarning(warning: string, lang: Lang): string {
  if (lang === "en") return warning;
  return translations.es.detector_warning_short as string;
}

// Translate the change-list strings generated by the Python backend
// Translate backend-generated metric description strings by extracting embedded numbers
export function translateMetricDescription(key: string, description: string, lang: Lang): string {
  if (lang === "en") return description;

  // Extract all numbers (including decimals) from the description string
  const nums = description.match(/[-\d.]+/g) ?? [];
  const n0 = nums[0] ?? "?";
  const n1 = nums[1] ?? "?";

  switch (key) {
    case "burstiness": {
      const isAI = description.includes("suspiciously uniform");
      return `CV de longitud de oración: ${n0} — ${isAI ? "uniformidad sospechosa (IA)" : "variación natural"}`;
    }
    case "ai_phrases":
      return `Se encontraron ${n0} frases típicas de IA (${n1} por 100 palabras)`;
    case "contraction": {
      const isAI = description.includes("AI-like");
      return `Ratio de contracciones: ${n0} — ${isAI ? "ausencia típica de IA" : "uso similar al humano"}`;
    }
    case "personal_voice": {
      const isAI = description.includes("impersonal");
      return `Ratio de pronombres personales: ${n0} — ${isAI ? "impersonal (IA)" : "voz personal"}`;
    }
    case "transition_density": {
      const isAI = description.includes("overused");
      return `Densidad de conectores: ${n0} — ${isAI ? "sobreuso (IA)" : "uso natural"}`;
    }
    case "opener_diversity": {
      const isAI = description.includes("repetitive");
      return `Inicios de oración estilo IA: ${n0}% de las oraciones — ${isAI ? "patrón repetitivo de IA" : "inicios variados"}`;
    }
    case "formality": {
      const isAI = description.includes("overly formal");
      return `Ratio de vocabulario formal: ${n0} — ${isAI ? "excesivamente formal (IA)" : "conversacional"}`;
    }
    case "sentence_structure": {
      const isAI = description.includes("typical AI range");
      return `Puntuación MATTR: ${n0} — ${isAI ? "rango típico de IA" : "vocabulario variado"}`;
    }
    case "coherence": {
      const isAI = description.includes("suspiciously");
      return `Similitud entre párrafos: ${n0} — ${isAI ? "consistencia sospechosa (IA)" : "flujo natural"}`;
    }
    default:
      return description;
  }
}

export function translateChange(change: string, lang: Lang): string {
  if (lang === "en") return change;

  // "Replaced N AI-signature phrases and formal words"  (rules-based)
  const replacedMatch = change.match(/^Replaced (\d+) AI-signature phrases/);
  if (replacedMatch) {
    return `Se reemplazaron ${replacedMatch[1]} frases de firma IA y palabras formales`;
  }
  // "Removed AI tells → replaced with ..."  (Claude AI)
  if (change.startsWith("Removed AI tells →")) {
    const rest = change.replace("Removed AI tells → replaced with ", "");
    return `Se eliminaron frases IA → reemplazadas con ${rest}`;
  }
  // "Added N natural contractions"
  const contrMatch = change.match(/^Added (\d+) natural contractions?/);
  if (contrMatch) {
    return `Se añadieron ${contrMatch[1]} contracciones naturales`;
  }
  // "Injected personal voice in N sentence(s)"  (rules-based)
  const voiceMatch = change.match(/^Injected personal voice in (\d+)/);
  if (voiceMatch) {
    return `Se inyectó voz personal en ${voiceMatch[1]} oración(es)`;
  }
  if (change.includes("Injected personal voice")) {
    return "Se añadió voz personal y perspectiva en primera persona";
  }
  if (change.includes("rhetorical questions")) {
    return "Se añadieron preguntas retóricas para mayor engagement";
  }
  if (change.includes("natural punctuation")) {
    return "Se introdujo puntuación natural (guiones em, puntos suspensivos)";
  }
  // "Restructured sentence count (N → M) for natural burstiness"
  const structMatch = change.match(/Restructured sentence count \((\d+) → (\d+)\)/);
  if (structMatch) {
    return `Se reestructuró el número de oraciones (${structMatch[1]} → ${structMatch[2]}) para mayor naturalidad`;
  }
  if (change.includes("subtle polish")) {
    return "Pulido sutil aplicado — cambios estructurales mínimos";
  }
  if (change.includes("natural human tone")) {
    return "Reescrito para tono humano natural y ritmo variado";
  }
  if (change.includes("Fully restructured")) {
    return "Reestructuración completa — nueva expresión, mismas ideas";
  }

  return change;
}
