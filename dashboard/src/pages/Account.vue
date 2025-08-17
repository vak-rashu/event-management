<template>
	<Tabs as="div" v-model="tabIndex" :tabs="tabs" @change="handleTabChange">
		<template #tab-panel>
			<div class="p-5">
				<router-view></router-view>
			</div>
		</template>
	</Tabs>
</template>

<script setup>
import { Tabs } from "frappe-ui";
import { ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const tabs = [
	{ label: "Profile", name: "profile" },
	{ label: "Bookings", name: "bookings-list" },
];

// Find the tab index based on current route path
const getTabIndexFromRoute = () => {
	const currentPath = route.path;

	// Check path patterns for each tab
	if (currentPath.startsWith("/account/bookings")) {
		return tabs.findIndex((tab) => tab.name === "bookings-list");
	}
	if (currentPath.startsWith("/account/profile")) {
		return tabs.findIndex((tab) => tab.name === "profile");
	}

	// Default to first tab
	return 0;
};

const tabIndex = ref(getTabIndexFromRoute());

// Watch for route changes and update tab index
watch(
	() => route.path,
	() => {
		tabIndex.value = getTabIndexFromRoute();
	}
);

// Handle tab change and navigate to corresponding route
const handleTabChange = (newTabIndex) => {
	const selectedTab = tabs[newTabIndex];
	if (selectedTab && selectedTab.name !== route.name) {
		router.push({ name: selectedTab.name });
	}
};
</script>
