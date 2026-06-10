import type { Metadata } from "next";
import "./globals.css";
import { LanguageProvider } from "@/contexts/LanguageContext";

export const metadata: Metadata = {
  title: "DetectAI — AI Text Detector & Humanizer",
  description:
    "Professional-grade AI text detection using multi-layer statistical analysis, plus an advanced humanizer powered by Claude.",
  keywords: ["AI detector", "AI text detection", "humanizer", "GPTZero alternative", "AI writing detector"],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-bg-primary text-txt-primary antialiased min-h-screen">
        <div className="noise-overlay fixed inset-0 pointer-events-none z-50" />
        <LanguageProvider>{children}</LanguageProvider>
      </body>
    </html>
  );
}
