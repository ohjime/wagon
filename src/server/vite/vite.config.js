import { defineConfig } from 'vite';
import { resolve } from 'path';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
    base: "/static/",
    build: {
        manifest: "manifest.json",
        outDir: resolve("./static"),
        assetsDir: "vite",
        rollupOptions: {
            input: {
                test: resolve("./assets/js/main.js"),
            },
            onwarn: (warning, warn) => (warning.code !== 'EVAL') ? warn(warning) : undefined // suppress eval warnings (@vue/devtools)

        }
    },
    plugins: [
        tailwindcss(),
    ]
})