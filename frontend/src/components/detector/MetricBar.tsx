"use client";

import { useEffect, useRef } from "react";
import { useLanguage } from "@/contexts/LanguageContext";
import { translateMetricDescription } from "@/lib/i18n";

interface MetricBarProps {
  name: string;
  score: number;
  label: string;
  description: string;
  weight: number;
  delay?: number;
}

function getBarColor(score: number) {
  if (score < 35) return { bar: "#22C55E", bg: "#22C55E15", text: "#22C55E" };
  if (score < 55) return { bar: "#EAB308", bg: "#EAB30815", text: "#EAB308" };
  if (score < 72) return { bar: "#FB923C", bg: "#FB923C15", text: "#FB923C" };
  return { bar: "#EF4444", bg: "#EF444415", text: "#EF4444" };
}

const METRIC_KEY_MAP: Record<string, "metric_burstiness" | "metric_ai_phrases" | "metric_personal_voice" | "metric_sentence_structure" | "metric_transition_density" | "metric_formality" | "metric_coherence" | "metric_contraction" | "metric_opener_diversity"> = {
  burstiness: "metric_burstiness",
  ai_phrases: "metric_ai_phrases",
  personal_voice: "metric_personal_voice",
  sentence_structure: "metric_sentence_structure",
  transition_density: "metric_transition_density",
  formality: "metric_formality",
  coherence: "metric_coherence",
  contraction: "metric_contraction",
  opener_diversity: "metric_opener_diversity",
};

export default function MetricBar({ name, score, label, description, weight, delay = 0 }: MetricBarProps) {
  const { t, lang } = useLanguage();
  const barRef = useRef<HTMLDivElement>(null);
  const colors = getBarColor(score);

  const translationKey = METRIC_KEY_MAP[name];
  const displayLabel = translationKey ? (t(translationKey) as string) : label;
  const displayDescription = translateMetricDescription(name, description, lang);

  useEffect(() => {
    const el = barRef.current;
    if (!el) return;
    el.style.width = "0%";
    const timer = setTimeout(() => {
      el.style.transition = "width 0.9s cubic-bezier(0.34, 1.56, 0.64, 1)";
      el.style.width = `${score}%`;
    }, delay);
    return () => clearTimeout(timer);
  }, [score, delay]);

  return (
    <div className="group space-y-2">
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-2 min-w-0">
          <span className="text-sm font-medium text-txt-secondary truncate">
            {displayLabel}
          </span>
          <span
            className="hidden group-hover:block text-xs px-1.5 py-0.5 rounded text-txt-muted border border-border max-w-[200px] truncate"
            title={displayDescription}
          >
            {displayDescription}
          </span>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <span className="text-xs text-txt-muted">
            {Math.round(weight * 100)}% {t("metric_weight") as string}
          </span>
          <span
            className="text-sm font-bold tabular-nums min-w-[2.5rem] text-right"
            style={{ color: colors.text }}
          >
            {Math.round(score)}
          </span>
        </div>
      </div>
      <div
        className="h-1.5 rounded-full overflow-hidden"
        style={{ background: "#1E1E2E" }}
      >
        <div
          ref={barRef}
          className="h-full rounded-full"
          style={{
            width: "0%",
            background: `linear-gradient(90deg, ${colors.bar}99, ${colors.bar})`,
            boxShadow: `0 0 8px ${colors.bar}60`,
          }}
        />
      </div>
      <p className="text-xs text-txt-muted opacity-0 group-hover:opacity-100 transition-opacity duration-200 leading-relaxed">
        {displayDescription}
      </p>
    </div>
  );
}
