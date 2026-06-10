"use client";

import type { SentenceScore } from "@/lib/types";
import { useLanguage } from "@/contexts/LanguageContext";

interface HighlightedTextProps {
  sentences: SentenceScore[];
}

function getSentenceClass(score: number) {
  if (score < 35) return "sentence-human";
  if (score < 60) return "sentence-uncertain";
  return "sentence-ai";
}

function getScoreColor(score: number) {
  if (score < 35) return "#22C55E";
  if (score < 60) return "#EAB308";
  return "#EF4444";
}

export default function HighlightedText({ sentences }: HighlightedTextProps) {
  const { t } = useLanguage();

  if (!sentences.length) return null;

  const tooltipFn = t("highlight_tooltip") as (score: number) => string;

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-txt-secondary">{t("highlight_title") as string}</h3>
        <div className="flex items-center gap-3 text-xs text-txt-muted">
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-sm bg-status-human inline-block opacity-70" />
            {t("highlight_human") as string}
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-sm bg-status-uncertain inline-block opacity-70" />
            {t("highlight_uncertain") as string}
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-sm bg-status-ai inline-block opacity-70" />
            {t("highlight_ai") as string}
          </span>
        </div>
      </div>
      <div className="space-y-1.5 text-sm leading-relaxed text-txt-secondary">
        {sentences.map((s, i) => (
          <span
            key={i}
            className={`inline ${getSentenceClass(s.score)} cursor-default`}
            title={tooltipFn(Math.round(s.score))}
          >
            <span style={{ color: getScoreColor(s.score), opacity: 0.9 }}>
              {s.text}
            </span>{" "}
          </span>
        ))}
      </div>
    </div>
  );
}
