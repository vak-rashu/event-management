<template>
	<div class="mb-6 text-ink-gray-6">
		<RouterLink :to="{ name: 'bookings-list' }" class="hover:underline">
			&larr; Back to Bookings
		</RouterLink>
	</div>

	<h2 class="text-ink-gray-9 font-semibold text-lg mb-3">
		Booking Details <span class="text-ink-gray-5 font-mono">(#{{ bookingId }})</span>
	</h2>
</template>

<script setup>
defineProps({
	bookingId: {
		type: String,
		required: true,
	},
});
</script>
