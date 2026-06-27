import { defineConfig } from "astro/config"
import react from "@astrojs/react"
import tailwind from "@astrojs/tailwind"
import mdx from "@astrojs/mdx"
import icon from "astro-icon"
import mermaid from "astro-mermaid"
import { resolve } from 'path'
import { fileURLToPath } from 'url'

const __dirname = fileURLToPath(new URL('.', import.meta.url))

export default defineConfig({
  site: "https://frex-is.github.io",
  base: "/astro-website/",
  markdown: {
    syntaxHighlight: {
      type: 'shiki',
      excludeLangs: ['mermaid'],
    },
  },
  integrations: [
    react(),
    tailwind(),
    mdx(),
    icon(),
    mermaid({
      autoTheme: false,
      theme: 'base',
      mermaidConfig: {
        themeVariables: {
          background: '#0B131F',
          primaryColor: '#1e293b',
          primaryBorderColor: '#334155',
          primaryTextColor: '#e2e8f0',
          secondaryColor: 'rgba(15, 23, 42, 0.4)',
          secondaryBorderColor: '#1e293b',
          tertiaryColor: 'rgba(34, 211, 238, 0.08)',
          tertiaryBorderColor: 'rgba(34, 211, 238, 0.2)',
          lineColor: '#22d3ee',
          textColor: '#94a3b8',
          actorBkg: 'rgba(15, 23, 42, 0.4)',
          actorBorder: '#1e293b',
          actorTextColor: '#e2e8f0',
          noteBkg: 'rgba(34, 211, 238, 0.08)',
          noteBorder: 'rgba(34, 211, 238, 0.2)',
          noteTextColor: '#94a3b8',
          activationBkgColor: '#1e293b',
          activationBorderColor: '#334155',
          sequenceNumberColor: '#64748b',
          signalColor: '#22d3ee',
          signalTextColor: '#94a3b8',
        },
      },
    }),
  ],
  vite: {
    resolve: {
      alias: {
        "@": resolve(__dirname, "src"),
        "@components": resolve(__dirname, "src/components"),
        "@layouts": resolve(__dirname, "src/layouts"),
        "@config": resolve(__dirname, "src/config"),
        "@utils": resolve(__dirname, "src/utils"),
        "@hooks": resolve(__dirname, "src/hooks"),
      }
    },
  }
})
