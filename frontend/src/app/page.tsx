"use client";

import { useState } from "react";
import { Brain, ChevronRight, Lock, ScanText, Shield, Wand2, Zap } from "lucide-react";
import Navbar from "@/components/Navbar";
import DetectorPanel from "@/components/detector/DetectorPanel";
import HumanizerPanel from "@/components/humanizer/HumanizerPanel";
import { useLanguage } from "@/contexts/LanguageContext";

export default function Home() {
  const [activeTab, setActiveTab] = useState<"detector" | "humanizer">("detector");
  const [humanizeText, setHumanizeText] = useState("");
  const { t } = useLanguage();

  function handleSendToHumanizer(text: string) {
    setHumanizeText(text);
    setActiveTab("humanizer");
  }

  const features = [
    { icon: Brain, label: t("feat_burstiness") },
    { icon: ScanText, label: t("feat_phrase") },
    { icon: Shield, label: t("feat_mattr") },
    { icon: Lock, label: t("feat_coherence") },
    { icon: Zap, label: t("feat_claude") },
    { icon: Wand2, label: t("feat_intensity") },
  ];

  return (
    <div className="min-h-screen bg-bg-primary flex flex-col">
      <Navbar activeTab={activeTab} onTabChange={setActiveTab} />

      {/* ── Hero banner ──────────────────────────────────────────────── */}
      <section className="relative overflow-hidden border-b border-border">
        {/* Ambient glows */}
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-brand-blue/5 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute top-0 right-1/4 w-96 h-96 bg-brand-orange/4 rounded-full blur-3xl pointer-events-none" />

        <div className="relative max-w-7xl mx-auto px-6 py-14">
          <div className="max-w-2xl space-y-5">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-brand-blue/10 border border-brand-blue/20 text-brand-blue-light text-xs font-medium">
              <Shield className="w-3.5 h-3.5" />
              {t("hero_badge")}
              <ChevronRight className="w-3 h-3 opacity-60" />
            </div>

            <h1 className="text-4xl sm:text-5xl font-extrabold leading-tight tracking-tight text-txt-primary">
              {t("hero_title1")}
              <br />
              <span className="text-brand-blue glow-blue">{t("hero_title2")}</span>
            </h1>

            <p className="text-txt-secondary text-lg leading-relaxed max-w-xl">
              {t("hero_desc")}
            </p>

            <div className="flex flex-wrap gap-3 pt-1">
              <button
                onClick={() => setActiveTab("detector")}
                className={`flex items-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-sm transition-all duration-200 cursor-pointer ${
                  activeTab === "detector"
                    ? "bg-brand-blue text-white shadow-glow-blue"
                    : "bg-bg-tertiary border border-border text-txt-secondary hover:border-brand-blue/40 hover:text-txt-primary"
                }`}
              >
                <ScanText className="w-4 h-4" />
                {t("hero_btn_analyze")}
              </button>
              <button
                onClick={() => setActiveTab("humanizer")}
                className={`flex items-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-sm transition-all duration-200 cursor-pointer ${
                  activeTab === "humanizer"
                    ? "bg-brand-orange text-white"
                    : "bg-bg-tertiary border border-border text-txt-secondary hover:border-brand-orange/40 hover:text-txt-primary"
                }`}
              >
                <Wand2 className="w-4 h-4" />
                {t("hero_btn_humanize")}
              </button>
            </div>
          </div>

          {/* Feature pills */}
          <div className="flex flex-wrap gap-3 mt-8">
            {features.map((f) => (
              <div
                key={f.label}
                className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-bg-secondary border border-border text-xs text-txt-muted"
              >
                <f.icon className="w-3.5 h-3.5 text-brand-blue-light" />
                {f.label}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Main tool area ───────────────────────────────────────────── */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-6 py-8">
        <div className="animate-fade-in">
          {activeTab === "detector" ? (
            <DetectorPanel onSendToHumanizer={handleSendToHumanizer} />
          ) : (
            <HumanizerPanel initialText={humanizeText} />
          )}
        </div>
      </main>

      {/* ── Footer ──────────────────────────────────────────────────── */}
      <footer className="border-t border-border py-6 px-6">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2 text-txt-muted text-sm">
            <Zap className="w-3.5 h-3.5 text-brand-blue" />
            <span>{t("footer_powered")}</span>
          </div>
          <div className="flex items-center gap-4 text-xs text-txt-muted">
            <span>{t("footer_burstiness")}</span>
            <span className="text-border">·</span>
            <span>{t("footer_phrase")}</span>
            <span className="text-border">·</span>
            <span>{t("footer_claude")}</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
