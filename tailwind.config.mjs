import type { Config } from 'tailwindcss'

export default {
  content: ['./src/**/*.{astro,tsx,ts,mdx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        surface: {
          DEFAULT: '#0B131F',
          card: 'rgba(15, 23, 42, 0.4)',
          elevated: 'rgba(15, 23, 42, 0.5)',
          hover: 'rgba(34, 211, 238, 0.08)',
          'card-light': 'rgba(15, 23, 42, 0.3)',
        },
        border: {
          DEFAULT: '#1e293b',
          subtle: 'rgba(30, 41, 59, 0.5)',
          hover: 'rgba(34, 211, 238, 0.3)',
        },
        accent: {
          cyan: '#22d3ee',
          green: '#4ade80',
          red: '#f87171',
          yellow: '#fbbf24',
          purple: '#818cf8',
          pink: '#f472b6',
        },
        text: {
          primary: '#ffffff',
          secondary: '#e2e8f0',
          muted: '#94a3b8',
          subtle: '#64748b',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      borderRadius: {
        card: '12px',
        block: '10px',
        pill: '999px',
      },
      fontSize: {
        'code': '13px',
      },
      maxWidth: {
        article: '960px',
        layout: '1200px',
      },
      animation: {
        'fade-in': 'fadeIn 0.6s ease forwards',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
} satisfies Config
