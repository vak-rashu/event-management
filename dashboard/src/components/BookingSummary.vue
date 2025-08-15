<!-- BookingSummary.vue -->
<template>
	<div class="bg-gray-50 border border-gray-200 rounded-lg p-6">
		<h2 class="text-xl font-bold text-gray-800 mb-4">Booking Summary</h2>

		<!-- Tickets Section -->
		<div v-if="Object.keys(summary.tickets).length" class="mb-4">
			<h3 class="text-lg font-semibold text-gray-700 mb-2">Tickets</h3>
			<div
				v-for="(ticket, name) in summary.tickets"
				:key="name"
				class="flex justify-between items-center text-gray-600 mb-1"
			>
				<span
					>{{ ticket.title }} ({{ ticket.count }} x
					{{ formatPrice(ticket.price, ticket.currency) }})</span
				>
				<span class="font-medium">{{ formatPrice(ticket.amount, ticket.currency) }}</span>
			</div>
		</div>

		<!-- Add-ons Section -->
		<div v-if="Object.keys(summary.add_ons).length" class="mb-4">
			<h3 class="text-lg font-semibold text-gray-700 mb-2">Add-ons</h3>
			<div
				v-for="(addOn, name) in summary.add_ons"
				:key="name"
				class="flex justify-between items-center text-gray-600 mb-1"
			>
				<span
					>{{ addOn.title }} ({{ addOn.count }} x
					{{ formatPrice(addOn.price, addOn.currency) }})</span
				>
				<span class="font-medium">{{ formatPrice(addOn.amount, addOn.currency) }}</span>
			</div>
		</div>

		<hr class="my-4 border-t border-gray-200" />

		<!-- Total Section -->
		<div class="flex justify-between items-center text-xl font-bold text-gray-900">
			<h3>Total</h3>
			<span>{{ formatPrice(total, totalCurrency) }}</span>
		</div>
	</div>
</template>

<script setup>
import { formatPrice } from "../utils/currency.js";

defineProps({
	summary: {
		type: Object,
		required: true,
	},
	total: {
		type: Number,
		required: true,
	},
	totalCurrency: {
		type: String,
		default: "INR",
	},
});
</script>
