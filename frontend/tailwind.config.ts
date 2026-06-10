import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Plus Jakarta Sans", "system-ui", "sans-serif"],
      },
      colors: {
        bg: {
          primary: "#050508",
          secondary: "#0D0D14",
          tertiary: "#13131F",
          card: "#111118",
        },
        border: {
          DEFAULT: "#1E1E2E",
          hover: "#2A2A3E",
          glow: "#3B82F620",
        },
        brand: {
          blue: "#3B82F6",
          "blue-light": "#60A5FA",
          "blue-dim": "#1D4ED8",
          orange: "#F97316",
          "orange-dim": "#C2410C",
        },
        status: {
          human: "#22C55E",
          "human-dim": "#15803D",
          uncertain: "#EAB308",
          "uncertain-dim": "#A16207",
          ai: "#EF4444",
          "ai-dim": "#B91C1C",
        },
        txt: {
          primary: "#F1F5F9",
          secondary: "#94A3B8",
          muted: "#475569",
        },
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic": "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
        "glow-blue": "radial-gradient(ellipse at center, #3B82F615 0%, transparent 70%)",
        "glow-green": "radial-gradient(ellipse at center, #22C55E15 0%, transparent 70%)",
        "glow-red": "radial-gradient(ellipse at center, #EF444415 0%, transparent 70%)",
      },
      animation: {
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "spin-slow": "spin 3s linear infinite",
        "fade-in": "fadeIn 0.4s ease-out",
        "slide-up": "slideUp 0.4s ease-out",
        "score-fill": "scoreFill 1.2s ease-out forwards",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(16px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        scoreFill: {
          "0%": { "stroke-dashoffset": "339" },
          "100%": { "stroke-dashoffset": "var(--target-offset)" },
        },
      },
      boxShadow: {
        "glow-blue": "0 0 20px #3B82F620, 0 0 40px #3B82F610",
        "glow-green": "0 0 20px #22C55E20, 0 0 40px #22C55E10",
        "glow-red": "0 0 20px #EF444420, 0 0 40px #EF444410",
        "card": "0 1px 3px rgba(0,0,0,0.4), 0 0 0 1px #1E1E2E",
        "card-hover": "0 4px 24px rgba(0,0,0,0.4), 0 0 0 1px #2A2A3E",
      },
    },
  },
  plugins: [],
};

export default config;
