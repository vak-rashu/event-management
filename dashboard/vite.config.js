import path from "node:path";
import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";

// Conditionally import frappe-ui plugin
async function getFrappeUIPlugin(isDev) {
	if (isDev) {
		const module = await import("./frappe-ui/vite");
		return module.default;
	}
	const module = await import("frappe-ui/vite");
	return module.default;
}

// https://vitejs.dev/config/
export default defineConfig(async ({ command, mode }) => {
	const isDev = command === "serve" || mode === "development";
	const frappeui = await getFrappeUIPlugin(isDev);

	const config = {
		plugins: [
			frappeui({
				frappeProxy: true,
				jinjaBootData: true,
				lucideIcons: true,
				buildConfig: {
					indexHtmlPath: "../events/www/dashboard.html",
					emptyOutDir: true,
					sourcemap: true,
				},
			}),
			vue(),
		],
		build: {
			chunkSizeWarningLimit: 1500,
			outDir: "../events/public/dashboard",
			emptyOutDir: true,
			target: "es2015",
			sourcemap: true,
		},
		resolve: {
			alias: {
				"@": path.resolve(__dirname, "src"),
				"tailwind.config.js": path.resolve(__dirname, "tailwind.config.js"),
			},
		},
		optimizeDeps: {
			include: ["feather-icons", "showdown", "highlight.js/lib/core", "interactjs"],
		},
		server: {
			allowedHosts: true,
		},
	};

	// Add local frappe-ui alias only in development
	if (isDev) {
		config.resolve.alias["frappe-ui"] = path.resolve(__dirname, "frappe-ui");
	}

	return config;
});
