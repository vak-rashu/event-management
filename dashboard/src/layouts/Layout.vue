<template>
	<nav class="flex items-center justify-end gap-4 p-4 border-b">
		<Button variant="ghost" size="md" @click="toggleTheme">
			<LucideSun v-if="userTheme === 'dark'" class="w-4 h-4" />
			<LucideMoon v-else class="w-4 h-4" />
		</Button>
	</nav>
	<div class="max-w-7xl py-12 mx-auto">
		<slot></slot>
	</div>
</template>

<script setup>
import { onMounted } from "vue";
import { useStorage } from "@vueuse/core";
import LucideMoon from "~icons/lucide/moon";
import LucideSun from "~icons/lucide/sun";

const userTheme = useStorage("user-theme", "dark");

onMounted(() => {
	document.documentElement.setAttribute("data-theme", userTheme.value);
});

function toggleTheme() {
	const currentTheme = userTheme.value;
	const newTheme = currentTheme === "dark" ? "light" : "dark";
	document.documentElement.setAttribute("data-theme", newTheme);
	userTheme.value = newTheme;
}
</script>
