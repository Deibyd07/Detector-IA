export interface MetricDetail {
  score: number;
  label: string;
  description: string;
  weight: number;
}

export interface SentenceScore {
  text: string;
  score: number;
}

export interface DetectResponse {
  score: number;
  verdict: string;
  confidence: string;
  breakdown: Record<string, MetricDetail>;
  ai_phrases_found: string[];
  sentences: SentenceScore[];
  stats: {
    word_count: number;
    sentence_count: number;
    avg_sentence_length: number;
    burstiness: number;
    mattr: number;
    flesch_reading_ease: number;
    ai_phrases_count: number;
    personal_pronoun_ratio: number;
  };
  warning?: string;
}

export interface HumanizeResponse {
  original: string;
  humanized: string;
  changes_made: string[];
  estimated_ai_score: number;
  original_ai_score?: number;
}

export type VerdictType = "Human Written" | "Likely Human" | "Uncertain" | "Likely AI" | "AI Generated";
export type IntensityType = "subtle" | "balanced" | "aggressive";
export type HumanizerMode = "ai" | "rules";
