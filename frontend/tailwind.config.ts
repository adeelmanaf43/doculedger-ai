import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: "#172026",
        muted: "#5b6770",
        line: "#d8dee3",
        paper: "#f7f8f5",
        panel: "#ffffff",
        accent: "#0f766e",
        amber: "#9a5b00",
        rose: "#b42318",
      },
    },
  },
  plugins: [],
};

export default config;
