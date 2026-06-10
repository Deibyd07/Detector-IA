"use client";

import { useEffect, useRef } from "react";
import { useLanguage } from "@/contexts/LanguageContext";
import { translateVerdict, translateConfidence } from "@/lib/i18n";

interface ScoreGaugeProps {
  score: number;
  verdict: string;
  confidence: string;
}

function getColorForScore(score: number) {
  if (score < 25) return { stroke: "#22C55E", glow: "#22C55E", label: "text-status-human" };
  if (score < 42) return { stroke: "#86EFAC", glow: "#22C55E", label: "text-green-400" };
  if (score < 58) return { stroke: "#EAB308", glow: "#EAB308", label: "text-status-uncertain" };
  if (score < 75) return { stroke: "#FB923C", glow: "#F97316", label: "text-orange-400" };
  return { stroke: "#EF4444", glow: "#EF4444", label: "text-status-ai" };
}

const CIRCUMFERENCE = 2 * Math.PI * 54; // r=54

export default function ScoreGauge({ score, verdict, confidence }: ScoreGaugeProps) {
  const { t, lang } = useLanguage();
  const circleRef = useRef<SVGCircleElement>(null);
  const translatedVerdict = translateVerdict(verdict, lang);
  const translatedConfidence = translateConfidence(confidence, lang);
  const colors = getColorForScore(score);

  useEffect(() => {
    const offset = CIRCUMFERENCE - (score / 100) * CIRCUMFERENCE;
    const el = circleRef.current;
    if (!el) return;
    el.style.strokeDashoffset = String(CIRCUMFERENCE);
    const raf = requestAnimationFrame(() => {
      el.style.transition = "stroke-dashoffset 1.4s cubic-bezier(0.34, 1.56, 0.64, 1)";
      el.style.strokeDashoffset = String(offset);
    });
    return () => cancelAnimationFrame(raf);
  }, [score]);

  return (
    <div className="flex flex-col items-center gap-4">
      <div className="relative">
        {/* Outer glow ring */}
        <div
          className="absolute inset-0 rounded-full opacity-20 blur-xl"
          style={{ background: colors.glow }}
        />
        <svg width="140" height="140" viewBox="0 0 140 140" className="relative z-10">
          {/* Track */}
          <circle
            cx="70" cy="70" r="54"
            fill="none"
            stroke="#1E1E2E"
            strokeWidth="10"
            strokeLinecap="round"
          />
          {/* Animated score arc */}
          <circle
            ref={circleRef}
            cx="70" cy="70" r="54"
            fill="none"
            stroke={colors.stroke}
            strokeWidth="10"
            strokeLinecap="round"
            strokeDasharray={CIRCUMFERENCE}
            strokeDashoffset={CIRCUMFERENCE}
            transform="rotate(-90 70 70)"
            style={{ filter: `drop-shadow(0 0 6px ${colors.glow}80)` }}
          />
          {/* Score text */}
          <text
            x="70" y="66"
            textAnchor="middle"
            dominantBaseline="middle"
            fill={colors.stroke}
            fontSize="28"
            fontWeight="700"
            fontFamily="Plus Jakarta Sans, sans-serif"
            style={{ filter: `drop-shadow(0 0 8px ${colors.glow}60)` }}
          >
            {Math.round(score)}
          </text>
          <text
            x="70" y="88"
            textAnchor="middle"
            fill="#475569"
            fontSize="11"
            fontFamily="Plus Jakarta Sans, sans-serif"
          >
            {t("gauge_probability") as string}
          </text>
        </svg>
      </div>

      {/* Verdict badge */}
      <div className="text-center space-y-1">
        <div
          className={`text-xl font-700 font-bold tracking-tight ${colors.label}`}
          style={{ textShadow: `0 0 16px ${colors.glow}50` }}
        >
          {translatedVerdict}
        </div>
        <div className="flex items-center justify-center gap-1.5">
          <div
            className="w-1.5 h-1.5 rounded-full"
            style={{ background: colors.stroke }}
          />
          <span className="text-xs text-txt-muted font-medium tracking-widest uppercase">
            {translatedConfidence} {t("gauge_confidence") as string}
          </span>
        </div>
      </div>
    </div>
  );
}
