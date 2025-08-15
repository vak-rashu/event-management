<template></template>

<script setup>
import { createResource } from "frappe-ui";
import { ref } from "vue";
import { session } from "../data/session";

const ping = createResource({
	url: "ping",
	auto: true,
});

const showDialog = ref(false);
</script>
