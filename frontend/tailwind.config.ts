import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Colores POSITIVA
        positiva: {
          DEFAULT: "#F58220",
          50: "#FEF3E8",
          100: "#FDDCBF",
          200: "#FBC596",
          300: "#F9AE6D",
          400: "#F79844",
          500: "#F58220",
          600: "#E5721A",
          700: "#C45F15",
          800: "#A34D10",
          900: "#823B0B",
        },
        // Sidebar
        sidebar: {
          DEFAULT: "#1E293B",
          foreground: "#F8FAFC",
          muted: "#64748B",
          accent: "#F58220",
          border: "#334155",
        },
      },
      keyframes: {
        "fade-in": {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "slide-in": {
          "0%": { transform: "translateX(-100%)" },
          "100%": { transform: "translateX(0)" },
        },
        pulse: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.5" },
        },
      },
      animation: {
        "fade-in": "fade-in 0.3s ease-out",
        "slide-in": "slide-in 0.3s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
