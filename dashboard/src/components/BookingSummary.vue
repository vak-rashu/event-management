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
				<span>{{ ticket.title }} ({{ ticket.count }} x ₹{{ ticket.price }})</span>
				<span class="font-medium">₹{{ ticket.amount.toFixed(2) }}</span>
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
				<span>{{ addOn.title }} ({{ addOn.count }} x ₹{{ addOn.price }})</span>
				<span class="font-medium">₹{{ addOn.amount.toFixed(2) }}</span>
			</div>
		</div>

		<hr class="my-4 border-t border-gray-200" />

		<!-- Total Section -->
		<div class="flex justify-between items-center text-xl font-bold text-gray-900">
			<h3>Total</h3>
			<span>₹{{ total.toFixed(2) }}</span>
		</div>
	</div>
</template>

<script setup>
defineProps({
	summary: {
		type: Object,
		required: true,
	},
	total: {
		type: Number,
		required: true,
	},
});
</script>
