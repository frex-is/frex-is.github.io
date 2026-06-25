import { defineConfig } from "astro/config"
import react from "@astrojs/react"
import tailwind from "@astrojs/tailwind"
import mdx from "@astrojs/mdx"
import icon from "astro-icon"
import { resolve } from 'path'
import { fileURLToPath } from 'url'

const __dirname = fileURLToPath(new URL('.', import.meta.url))

export default defineConfig({
  integrations: [
    react(),
    tailwind(),
    mdx(),
    icon(),
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
