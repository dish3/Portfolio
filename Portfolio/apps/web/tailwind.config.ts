import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "../../packages/config/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0A0A0F",
        surface: {
          DEFAULT: "#12121A",
          hover: "#181824",
          subtle: "#161622",
        },
        border: {
          DEFAULT: "#1E1E2E",
          subtle: "#161622",
        },
        accent: {
          amber: "#D9A857",
          "amber-muted": "#9E7B3B",
          ice: "#7FE7E0",
          "ice-muted": "#4DA8A2",
        },
        foreground: {
          DEFAULT: "#F3F4F6",
          secondary: "#9CA3AF",
          muted: "#6B7280",
        },
      },
      fontFamily: {
        sans: ["var(--font-sans)", "Inter", "sans-serif"],
        mono: ["var(--font-mono)", "JetBrains Mono", "monospace"],
      },
    },
  },
  plugins: [],
};

export default config;
