"use client";

import { useEffect, useState } from "react";
import {
  AlertCircle,
  CheckCircle2,
  ClipboardCheck,
  Copy,
  Loader2,
  Sparkles,
  Wand2,
  Zap,
} from "lucide-react";
import { humanizeText } from "@/lib/api";
import type { HumanizeResponse, HumanizerMode, IntensityType } from "@/lib/types";
import { useLanguage } from "@/contexts/LanguageContext";
import { translateChange } from "@/lib/i18n";

function ScoreBadge({ score, label }: { score: number; label: string }) {
  const color =
    score < 30 ? "#22C55E" : score < 55 ? "#EAB308" : score < 75 ? "#FB923C" : "#EF4444";
  return (
    <div className="flex flex-col items-center gap-0.5">
      <div
        className="text-2xl font-bold tabular-nums"
        style={{ color, textShadow: `0 0 12px ${color}50` }}
      >
        {Math.round(score)}%
      </div>
      <div className="text-xs text-txt-muted">{label}</div>
    </div>
  );
}

export default function HumanizerPanel({ initialText = "" }: { initialText?: string }) {
  const { t, lang } = useLanguage();
  const [text, setText] = useState(initialText);
  const [intensity, setIntensity] = useState<IntensityType>("balanced");
  const [mode, setMode] = useState<HumanizerMode>("rules");
  const [result, setResult] = useState<HumanizeResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [copiedOriginal, setCopiedOriginal] = useState(false);
  const [copiedHumanized, setCopiedHumanized] = useState(false);

  useEffect(() => {
    if (initialText) setText(initialText);
  }, [initialText]);

  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;

  const modeOptions = [
    {
      value: "rules" as HumanizerMode,
      label: t("humanizer_mode_rules") as string,
      desc: t("humanizer_mode_rules_desc") as string,
      icon: <Zap className="w-3.5 h-3.5" />,
    },
    {
      value: "ai" as HumanizerMode,
      label: t("humanizer_mode_ai") as string,
      desc: t("humanizer_mode_ai_desc") as string,
      icon: <Sparkles className="w-3.5 h-3.5" />,
    },
  ];

  const intensityOptions = [
    {
      value: "subtle" as IntensityType,
      label: t("intensity_subtle_label") as string,
      desc: t("intensity_subtle_desc") as string,
    },
    {
      value: "balanced" as IntensityType,
      label: t("intensity_balanced_label") as string,
      desc: t("intensity_balanced_desc") as string,
    },
    {
      value: "aggressive" as IntensityType,
      label: t("intensity_aggressive_label") as string,
      desc: t("intensity_aggressive_desc") as string,
    },
  ];

  async function handleHumanize() {
    if (!text.trim() || wordCount < 10) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await humanizeText(text, intensity, mode);
      setResult(data);
    } catch (e) {
      const fallback =
        mode === "ai"
          ? (t("humanizer_error_fallback_ai") as string)
          : (t("humanizer_error_fallback") as string);
      setError(e instanceof Error ? e.message : fallback);
    } finally {
      setLoading(false);
    }
  }

  async function copyText(content: string, which: "original" | "humanized") {
    await navigator.clipboard.writeText(content);
    if (which === "original") {
      setCopiedOriginal(true);
      setTimeout(() => setCopiedOriginal(false), 2000);
    } else {
      setCopiedHumanized(true);
      setTimeout(() => setCopiedHumanized(false), 2000);
    }
  }

  const scoreDescFn = t("humanizer_score_desc") as (score: number) => string;
  const isAiMode = mode === "ai";

  return (
    <div className="space-y-6">
      {/* ── Input + controls ───────────────────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input */}
        <div className="space-y-4">
          <div className="relative gradient-border rounded-xl overflow-hidden">
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder={t("humanizer_placeholder") as string}
              className="w-full min-h-[300px] bg-bg-secondary text-txt-primary placeholder:text-txt-muted text-sm leading-relaxed p-5 focus:outline-none focus:ring-1 focus:ring-brand-blue/30 rounded-xl font-sans"
            />
            <div className="absolute bottom-3 right-4 text-xs text-txt-muted tabular-nums">
              {wordCount} {t("detector_words") as string}
            </div>
          </div>

          {/* Mode selector */}
          <div className="space-y-2">
            <p className="text-xs font-medium text-txt-muted uppercase tracking-widest">
              {t("humanizer_mode_label") as string}
            </p>
            <div className="grid grid-cols-2 gap-2">
              {modeOptions.map((opt) => (
                <button
                  key={opt.value}
                  onClick={() => setMode(opt.value)}
                  className={`p-3 rounded-xl border text-left transition-all duration-200 cursor-pointer ${
                    mode === opt.value
                      ? "border-brand-blue bg-brand-blue/10 text-txt-primary"
                      : "border-border bg-bg-tertiary text-txt-muted hover:border-border-hover hover:text-txt-secondary"
                  }`}
                >
                  <p className="text-sm font-semibold flex items-center gap-1.5">
                    {opt.icon}
                    {opt.label}
                  </p>
                  <p className="text-xs mt-0.5 leading-snug opacity-75">{opt.desc}</p>
                </button>
              ))}
            </div>
          </div>

          {/* Intensity selector */}
          <div className="space-y-2">
            <p className="text-xs font-medium text-txt-muted uppercase tracking-widest">
              {t("humanizer_intensity_label") as string}
            </p>
            <div className="grid grid-cols-3 gap-2">
              {intensityOptions.map((opt) => (
                <button
                  key={opt.value}
                  onClick={() => setIntensity(opt.value)}
                  className={`p-3 rounded-xl border text-left transition-all duration-200 cursor-pointer ${
                    intensity === opt.value
                      ? "border-brand-blue bg-brand-blue/10 text-txt-primary"
                      : "border-border bg-bg-tertiary text-txt-muted hover:border-border-hover hover:text-txt-secondary"
                  }`}
                >
                  <p className="text-sm font-semibold">{opt.label}</p>
                  <p className="text-xs mt-0.5 leading-snug opacity-75">{opt.desc}</p>
                </button>
              ))}
            </div>
          </div>

          <button
            onClick={handleHumanize}
            disabled={loading || wordCount < 10}
            className="w-full flex items-center justify-center gap-2.5 px-6 py-3 bg-brand-orange hover:bg-brand-orange-dim disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition-all duration-200 text-sm cursor-pointer"
          >
            {loading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : isAiMode ? (
              <Sparkles className="w-4 h-4" />
            ) : (
              <Zap className="w-4 h-4" />
            )}
            {loading
              ? isAiMode
                ? (t("humanizer_btn_loading_ai") as string)
                : (t("humanizer_btn_loading") as string)
              : isAiMode
                ? (t("humanizer_btn_ai") as string)
                : (t("humanizer_btn") as string)}
          </button>

          {error && (
            <div className="flex items-start gap-2.5 px-4 py-3 rounded-xl bg-status-ai/8 border border-status-ai/25 text-sm text-status-ai">
              <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />
              <div>
                <p className="font-medium">{t("humanizer_error_title") as string}</p>
                <p className="text-xs mt-0.5 text-status-ai/70">{error}</p>
              </div>
            </div>
          )}
        </div>

        {/* Result preview */}
        <div className="space-y-4">
          {!result && !loading && (
            <div className="flex-1 flex flex-col items-center justify-center h-full min-h-[300px] py-16 text-center space-y-3">
              <div className="w-16 h-16 rounded-2xl bg-bg-tertiary border border-border flex items-center justify-center">
                <Wand2 className="w-7 h-7 text-txt-muted" />
              </div>
              <div>
                <p className="text-txt-secondary font-medium">{t("humanizer_empty_title") as string}</p>
                <p className="text-txt-muted text-sm mt-1">{t("humanizer_empty_sub") as string}</p>
              </div>
            </div>
          )}

          {loading && (
            <div className="flex flex-col items-center justify-center h-full min-h-[300px] space-y-5">
              <div className="relative">
                {isAiMode ? (
                  <Sparkles className="w-10 h-10 text-brand-orange animate-pulse-slow" />
                ) : (
                  <Zap className="w-10 h-10 text-brand-orange animate-pulse-slow" />
                )}
                <div
                  className="absolute inset-0 rounded-full blur-xl opacity-30"
                  style={{ background: "#F97316" }}
                />
              </div>
              <div className="text-center space-y-1.5">
                <p className="text-txt-secondary font-medium">
                  {isAiMode
                    ? (t("humanizer_loading_title_ai") as string)
                    : (t("humanizer_loading_title") as string)}
                </p>
                <p className="text-txt-muted text-sm">{t("humanizer_loading_sub") as string}</p>
              </div>
            </div>
          )}

          {result && (
            <div className="animate-slide-up space-y-4">
              <div className="bg-bg-card border border-border rounded-xl p-4">
                <div className="relative">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-semibold text-txt-muted uppercase tracking-widest">
                      {t("humanizer_output_label") as string}
                    </span>
                    <button
                      onClick={() => copyText(result.humanized, "humanized")}
                      className="flex items-center gap-1 text-xs text-txt-muted hover:text-status-human transition-colors cursor-pointer"
                    >
                      {copiedHumanized ? (
                        <ClipboardCheck className="w-3.5 h-3.5 text-status-human" />
                      ) : (
                        <Copy className="w-3.5 h-3.5" />
                      )}
                      {copiedHumanized
                        ? (t("humanizer_copied") as string)
                        : (t("humanizer_copy") as string)}
                    </button>
                  </div>
                  <p className="text-sm text-txt-primary leading-relaxed max-h-[260px] overflow-y-auto pr-1">
                    {result.humanized}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* ── Detailed results ────────────────────────────────────────── */}
      {result && (
        <div className="animate-slide-up space-y-5">
          {/* Score comparison */}
          <div className="bg-bg-card border border-border rounded-2xl p-6">
            <h3 className="text-sm font-semibold text-txt-muted uppercase tracking-widest mb-5">
              {t("humanizer_score_title") as string}
            </h3>
            <div className="flex items-center justify-around">
              <ScoreBadge
                score={result.original_ai_score ?? 50}
                label={t("humanizer_before") as string}
              />
              <div className="flex flex-col items-center gap-1">
                <div className="flex items-center gap-1 text-txt-muted">
                  <div className="w-8 h-px bg-border" />
                  <Sparkles className="w-4 h-4 text-brand-orange" />
                  <div className="w-8 h-px bg-border" />
                </div>
                <span className="text-xs text-txt-muted">{t("humanizer_humanized_label") as string}</span>
              </div>
              <ScoreBadge score={result.estimated_ai_score} label={t("humanizer_after") as string} />
            </div>
            <div className="mt-4 bg-bg-tertiary rounded-xl p-3 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-status-human shrink-0" />
              <p className="text-xs text-txt-secondary">
                {scoreDescFn(result.estimated_ai_score)}
              </p>
            </div>
          </div>

          {/* Changes made */}
          {result.changes_made.length > 0 && (
            <div className="bg-bg-card border border-border rounded-2xl p-6">
              <h3 className="text-sm font-semibold text-txt-muted uppercase tracking-widest mb-4">
                {t("humanizer_changes_title") as string}
              </h3>
              <ul className="space-y-2.5">
                {result.changes_made.map((change, i) => (
                  <li key={i} className="flex items-start gap-2.5 text-sm text-txt-secondary">
                    <CheckCircle2 className="w-4 h-4 text-status-human mt-0.5 shrink-0" />
                    {translateChange(change, lang)}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Side-by-side comparison */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div className="bg-bg-card border border-status-ai/20 rounded-2xl p-5">
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-semibold text-status-ai uppercase tracking-widest">
                  {t("humanizer_original") as string}
                </span>
                <button
                  onClick={() => copyText(result.original, "original")}
                  className="text-xs text-txt-muted hover:text-txt-secondary transition-colors cursor-pointer"
                >
                  {copiedOriginal
                    ? (t("humanizer_copied") as string)
                    : (t("humanizer_copy") as string)}
                </button>
              </div>
              <p className="text-sm text-txt-secondary leading-relaxed max-h-[200px] overflow-y-auto">
                {result.original}
              </p>
            </div>
            <div className="bg-bg-card border border-status-human/20 rounded-2xl p-5">
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-semibold text-status-human uppercase tracking-widest">
                  {t("humanizer_humanized_label") as string}
                </span>
                <button
                  onClick={() => copyText(result.humanized, "humanized")}
                  className="text-xs text-txt-muted hover:text-txt-secondary transition-colors cursor-pointer"
                >
                  {copiedHumanized
                    ? (t("humanizer_copied") as string)
                    : (t("humanizer_copy") as string)}
                </button>
              </div>
              <p className="text-sm text-txt-primary leading-relaxed max-h-[200px] overflow-y-auto">
                {result.humanized}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
