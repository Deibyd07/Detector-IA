"use client";

import { ScanText, Wand2, Zap } from "lucide-react";
import { useLanguage } from "@/contexts/LanguageContext";

interface NavbarProps {
  activeTab: "detector" | "humanizer";
  onTabChange: (tab: "detector" | "humanizer") => void;
}

export default function Navbar({ activeTab, onTabChange }: NavbarProps) {
  const { lang, setLang, t } = useLanguage();

  return (
    <header className="sticky top-0 z-40 w-full">
      <div className="absolute inset-0 bg-bg-primary/80 backdrop-blur-md border-b border-border" />
      <div className="relative max-w-7xl mx-auto px-6 h-16 flex items-center justify-between gap-6">
        {/* Logo */}
        <div className="flex items-center gap-2.5 shrink-0">
          <div className="w-8 h-8 rounded-lg bg-brand-blue flex items-center justify-center shadow-glow-blue">
            <Zap className="w-4 h-4 text-white fill-white" />
          </div>
          <span className="text-base font-bold tracking-tight text-txt-primary">
            Detect<span className="text-brand-blue">AI</span>
          </span>
        </div>

        {/* Tab switcher */}
        <nav className="flex items-center p-1 bg-bg-tertiary border border-border rounded-xl gap-1">
          <TabButton
            icon={<ScanText className="w-4 h-4" />}
            label={t("nav_detector")}
            active={activeTab === "detector"}
            onClick={() => onTabChange("detector")}
          />
          <TabButton
            icon={<Wand2 className="w-4 h-4" />}
            label={t("nav_humanizer")}
            active={activeTab === "humanizer"}
            onClick={() => onTabChange("humanizer")}
          />
        </nav>

        {/* Right side: badge + language toggle */}
        <div className="flex items-center gap-3 shrink-0">
          <div className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-bg-tertiary border border-border text-xs text-txt-muted">
            <span className="w-1.5 h-1.5 rounded-full bg-status-human animate-pulse" />
            {t("nav_badge")}
          </div>

          {/* Language toggle */}
          <div className="flex items-center p-0.5 bg-bg-tertiary border border-border rounded-lg">
            <LangButton active={lang === "en"} onClick={() => setLang("en")}>EN</LangButton>
            <LangButton active={lang === "es"} onClick={() => setLang("es")}>ES</LangButton>
          </div>
        </div>
      </div>
    </header>
  );
}

function TabButton({
  icon,
  label,
  active,
  onClick,
}: {
  icon: React.ReactNode;
  label: string;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 cursor-pointer ${
        active
          ? "bg-bg-secondary text-txt-primary shadow-sm border border-border"
          : "text-txt-muted hover:text-txt-secondary"
      }`}
    >
      {icon}
      {label}
    </button>
  );
}

function LangButton({
  children,
  active,
  onClick,
}: {
  children: string;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={`px-2.5 py-1 rounded-md text-xs font-semibold transition-all duration-200 cursor-pointer ${
        active
          ? "bg-brand-blue text-white"
          : "text-txt-muted hover:text-txt-secondary"
      }`}
    >
      {children}
    </button>
  );
}
