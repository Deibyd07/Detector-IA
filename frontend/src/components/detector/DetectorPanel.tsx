"use client";

import { useState } from "react";
import { AlertCircle, ChevronDown, ChevronUp, Clipboard, ClipboardCheck, Loader2, ScanText, Zap } from "lucide-react";
import { detectAI } from "@/lib/api";
import type { DetectResponse } from "@/lib/types";
import ScoreGauge from "./ScoreGauge";
import MetricBar from "./MetricBar";
import HighlightedText from "./HighlightedText";
import { useLanguage } from "@/contexts/LanguageContext";
import { translateWarning } from "@/lib/i18n";

export default function DetectorPanel({
  onSendToHumanizer,
}: {
  onSendToHumanizer: (text: string) => void;
}) {
  const { t, lang } = useLanguage();
  const [text, setText] = useState("");
  const [result, setResult] = useState<DetectResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showSentences, setShowSentences] = useState(false);
  const [copied, setCopied] = useState(false);

  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
  const charCount = text.length;

  async function handleAnalyze() {
    if (!text.trim() || wordCount < 10) return;
    setLoading(true);
    setError(null);
    setResult(null);
    setShowSentences(false);
    try {
      const data = await detectAI(text);
      setResult(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : t("detector_error_fallback") as string);
    } finally {
      setLoading(false);
    }
  }

  async function handleCopy() {
    if (!result) return;
    const fn = t("detector_copy_result_text") as (score: number, verdict: string, confidence: string) => string;
    await navigator.clipboard.writeText(fn(result.score, result.verdict, result.confidence));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  const metricEntries = result
    ? Object.entries(result.breakdown).sort((a, b) => b[1].score - a[1].score)
    : [];

  const addWordsFn = t("detector_add_words") as (n: number) => string;
  const signaturesFn = t("detector_signatures") as (n: number) => string;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-full">
      {/* ── Input column ───────────────────────────────────────────── */}
      <div className="flex flex-col gap-4">
        <div className="relative flex-1 gradient-border rounded-xl overflow-hidden">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder={t("detector_placeholder") as string}
            className="w-full h-full min-h-[420px] bg-bg-secondary text-txt-primary placeholder:text-txt-muted text-sm leading-relaxed p-5 focus:outline-none focus:ring-1 focus:ring-brand-blue/30 rounded-xl font-sans transition-colors"
          />
          {/* word count badge */}
          <div className="absolute bottom-3 right-4 flex items-center gap-2">
            <span className={`text-xs tabular-nums ${wordCount < 150 ? "text-status-uncertain" : "text-txt-muted"}`}>
              {wordCount} {t("detector_words") as string}
            </span>
            <span className="text-xs text-txt-muted/50">·</span>
            <span className="text-xs text-txt-muted tabular-nums">{charCount} {t("detector_chars") as string}</span>
          </div>
        </div>

        {wordCount > 0 && wordCount < 150 && (
          <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-status-uncertain/8 border border-status-uncertain/20 text-xs text-status-uncertain">
            <AlertCircle className="w-3.5 h-3.5 shrink-0" />
            {addWordsFn(150 - wordCount)}
          </div>
        )}

        <div className="flex gap-3">
          <button
            onClick={handleAnalyze}
            disabled={loading || wordCount < 10}
            className="flex-1 flex items-center justify-center gap-2.5 px-6 py-3 bg-brand-blue hover:bg-brand-blue-dim disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition-all duration-200 shadow-glow-blue hover:shadow-none text-sm cursor-pointer"
          >
            {loading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <ScanText className="w-4 h-4" />
            )}
            {loading ? (t("detector_btn_analyzing") as string) : (t("detector_btn_analyze") as string)}
          </button>
          {result && result.score > 50 && (
            <button
              onClick={() => onSendToHumanizer(text)}
              className="flex items-center gap-2 px-4 py-3 bg-bg-tertiary hover:bg-border-hover border border-border hover:border-border-hover text-txt-secondary hover:text-txt-primary font-medium rounded-xl transition-all duration-200 text-sm cursor-pointer"
            >
              <Zap className="w-4 h-4 text-brand-orange" />
              {t("detector_btn_humanize") as string}
            </button>
          )}
        </div>

        {error && (
          <div className="flex items-start gap-2.5 px-4 py-3 rounded-xl bg-status-ai/8 border border-status-ai/25 text-sm text-status-ai">
            <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />
            <div>
              <p className="font-medium">{t("detector_error_title") as string}</p>
              <p className="text-xs mt-0.5 text-status-ai/70">{error}</p>
            </div>
          </div>
        )}
      </div>

      {/* ── Results column ─────────────────────────────────────────── */}
      <div className="flex flex-col gap-5">
        {!result && !loading && (
          <div className="flex-1 flex flex-col items-center justify-center py-20 text-center space-y-3">
            <div className="w-16 h-16 rounded-2xl bg-bg-tertiary border border-border flex items-center justify-center">
              <ScanText className="w-7 h-7 text-txt-muted" />
            </div>
            <div>
              <p className="text-txt-secondary font-medium">{t("detector_empty_title") as string}</p>
              <p className="text-txt-muted text-sm mt-1">{t("detector_empty_sub") as string}</p>
            </div>
          </div>
        )}

        {loading && (
          <div className="flex-1 flex flex-col items-center justify-center py-20 space-y-4">
            <div className="relative w-16 h-16">
              <div className="absolute inset-0 rounded-full border-2 border-brand-blue/20" />
              <div className="absolute inset-0 rounded-full border-2 border-transparent border-t-brand-blue animate-spin" />
              <div className="absolute inset-2 rounded-full border border-brand-blue/10 animate-pulse-slow" />
            </div>
            <div className="space-y-1.5 text-center">
              <p className="text-txt-secondary font-medium">{t("detector_loading_title") as string}</p>
              <p className="text-txt-muted text-sm">{t("detector_loading_sub") as string}</p>
            </div>
          </div>
        )}

        {result && (
          <div className="space-y-5 animate-slide-up">
            {/* Score header */}
            <div className="bg-bg-card border border-border rounded-2xl p-6">
              <div className="flex items-start justify-between mb-5">
                <h3 className="text-sm font-semibold text-txt-muted uppercase tracking-widest">
                  {t("detector_result_title") as string}
                </h3>
                <button
                  onClick={handleCopy}
                  className="flex items-center gap-1.5 text-xs text-txt-muted hover:text-txt-secondary transition-colors cursor-pointer"
                >
                  {copied ? <ClipboardCheck className="w-3.5 h-3.5 text-status-human" /> : <Clipboard className="w-3.5 h-3.5" />}
                  {copied ? (t("detector_copied") as string) : (t("detector_copy") as string)}
                </button>
              </div>
              <ScoreGauge
                score={result.score}
                verdict={result.verdict}
                confidence={result.confidence}
              />
            </div>

            {/* Warning */}
            {result.warning && (
              <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-status-uncertain/8 border border-status-uncertain/20 text-xs text-status-uncertain">
                <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                {translateWarning(result.warning, lang)}
              </div>
            )}

            {/* Metrics */}
            <div className="bg-bg-card border border-border rounded-2xl p-5 space-y-4">
              <h3 className="text-sm font-semibold text-txt-muted uppercase tracking-widest">
                {t("detector_metrics") as string}
              </h3>
              <div className="space-y-4">
                {metricEntries.map(([key, metric], i) => (
                  <MetricBar
                    key={key}
                    name={key}
                    score={metric.score}
                    label={metric.label}
                    description={metric.description}
                    weight={metric.weight}
                    delay={i * 80}
                  />
                ))}
              </div>
            </div>

            {/* AI phrases */}
            {result.ai_phrases_found.length > 0 && (
              <div className="bg-bg-card border border-border rounded-2xl p-5">
                <h3 className="text-sm font-semibold text-txt-muted uppercase tracking-widest mb-3">
                  {signaturesFn(result.ai_phrases_found.length)}
                </h3>
                <div className="flex flex-wrap gap-2">
                  {result.ai_phrases_found.map((phrase, i) => (
                    <span
                      key={i}
                      className="px-2.5 py-1 rounded-lg bg-status-ai/10 border border-status-ai/20 text-status-ai text-xs font-medium"
                    >
                      {phrase}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Stats */}
            <div className="bg-bg-card border border-border rounded-2xl p-5">
              <h3 className="text-sm font-semibold text-txt-muted uppercase tracking-widest mb-3">
                {t("detector_stats") as string}
              </h3>
              <div className="grid grid-cols-2 gap-x-6 gap-y-2.5 text-sm">
                {[
                  [t("stat_words") as string, result.stats.word_count],
                  [t("stat_sentences") as string, result.stats.sentence_count],
                  [t("stat_avg_len") as string, `${result.stats.avg_sentence_length} ${t("detector_words") as string}`],
                  [t("stat_burstiness") as string, result.stats.burstiness],
                  [t("stat_mattr") as string, result.stats.mattr],
                  [t("stat_flesch") as string, result.stats.flesch_reading_ease],
                ].map(([label, val]) => (
                  <div key={String(label)} className="flex justify-between">
                    <span className="text-txt-muted">{label}</span>
                    <span className="text-txt-secondary font-medium tabular-nums">{val}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Sentence toggle */}
            {result.sentences.length > 0 && (
              <div className="bg-bg-card border border-border rounded-2xl overflow-hidden">
                <button
                  onClick={() => setShowSentences(!showSentences)}
                  className="w-full flex items-center justify-between px-5 py-4 text-sm font-semibold text-txt-muted uppercase tracking-widest hover:text-txt-secondary transition-colors cursor-pointer"
                >
                  {t("detector_sentences") as string}
                  {showSentences ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                </button>
                {showSentences && (
                  <div className="px-5 pb-5 border-t border-border">
                    <div className="pt-4">
                      <HighlightedText sentences={result.sentences} />
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
