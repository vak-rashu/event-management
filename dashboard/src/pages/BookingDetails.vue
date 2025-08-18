<template>
	<div class="mb-6">
		<RouterLink :to="{ name: 'bookings-list' }" class="hover:underline">
			&larr; Back to Bookings
		</RouterLink>
	</div>

	<div class="w-4" v-if="bookingDetails.loading">
		<Spinner />
	</div>

	<div v-else-if="bookingDetails.data">
		<!-- Success Message (only shown on payment success) -->
		<Transition
			name="success-message"
			enter-active-class="transition-all duration-500 ease-out"
			leave-active-class="transition-all duration-500 ease-in"
			enter-from-class="opacity-0 transform -translate-y-4 scale-95"
			enter-to-class="opacity-100 transform translate-y-0 scale-100"
			leave-from-class="opacity-100 transform translate-y-0 scale-100"
			leave-to-class="opacity-0 transform -translate-y-4 scale-95"
		>
			<div
				v-if="showSuccessMessage"
				class="mb-6 bg-green-50 border border-green-200 rounded-lg p-4"
			>
				<div class="flex items-center">
					<LucideCheckCircle class="w-6 h-6 text-green-600 mr-3" />
					<div>
						<h3 class="text-green-800 font-semibold">Payment Successful! 🎉</h3>
						<p class="text-green-700">
							Your booking has been confirmed. Check your email for tickets and
							details.
						</p>
					</div>
				</div>
			</div>
		</Transition>

		<h2 class="text-ink-gray-9 font-semibold text-lg mb-3">
			Booking Details <span class="text-ink-gray-5 font-mono">(#{{ bookingId }})</span>
		</h2>
		<div>
			<h3 class="text-ink-gray-8 font-semibold text-lg mb-3">Tickets</h3>

			<!-- Transfer restriction notice -->
			<div
				v-if="!canTransferTickets"
				class="mb-4 bg-yellow-50 border border-yellow-200 rounded-lg p-4"
			>
				<div class="flex items-center">
					<LucideTriangleAlert class="w-5 h-5 text-yellow-600 mr-3" />
					<div>
						<p class="text-yellow-800 text-sm">
							<strong>Ticket transfers are no longer available</strong> - The
							transfer window has closed as the event is approaching.
						</p>
					</div>
				</div>
			</div>

			<ol class="grid grid-cols-3 gap-3">
				<TicketCard
					v-for="ticket in bookingDetails.data.tickets"
					:key="ticket.name"
					:ticket="ticket"
					:can-transfer="canTransferTickets"
					@transfer-success="onTicketTransferSuccess"
				/>
			</ol>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { createResource, Spinner } from "frappe-ui";
import { triggerCelebrationConfetti } from "../utils/confetti.js";
import TicketCard from "../components/TicketCard.vue";
import LucideTriangleAlert from "~icons/lucide/triangle-alert";
import LucideCheckCircle from "~icons/lucide/check-circle";

const route = useRoute();
const router = useRouter();

const props = defineProps({
	bookingId: {
		type: String,
		required: true,
	},
});

const showSuccessMessage = ref(false);

const bookingDetails = createResource({
	url: "events.api.get_booking_details",
	params: { booking_id: props.bookingId },
	auto: true,
});

const canTransferTickets = computed(() => {
	return bookingDetails.data?.can_transfer_ticket?.can_transfer || false;
});

const onTicketTransferSuccess = () => {
	bookingDetails.reload();
};

// Check if this is a successful payment redirect
onMounted(() => {
	if (route.query.success === "true") {
		showSuccessMessage.value = true;

		// Trigger confetti animation
		triggerCelebrationConfetti();

		// Clean up the URL by removing the success parameter
		router.replace({
			name: route.name,
			params: route.params,
		});

		// Hide success message after 10 seconds
		setTimeout(() => {
			showSuccessMessage.value = false;
		}, 10000);
	}
});
</script>
