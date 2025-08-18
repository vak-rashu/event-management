<template>
	<div class="mb-6">
		<RouterLink :to="{ name: 'bookings-list' }" class="hover:underline">
			&larr; Back to Bookings
		</RouterLink>
	</div>

	<div class="w-4" v-if="booking.loading || tickets.loading">
		<Spinner />
	</div>

	<div v-else-if="booking.doc && tickets.data">
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
					<svg
						class="w-6 h-6 text-green-600 mr-3"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
						/>
					</svg>
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
				v-if="!transferEligibility.loading && !canTransferTickets"
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
					v-for="ticket in tickets.data"
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
import { ref, onMounted, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { createDocumentResource, createResource, Spinner, useList } from "frappe-ui";
import confetti from "canvas-confetti";
import TicketCard from "../components/TicketCard.vue";
import LucideTriangleAlert from "~icons/lucide/triangle-alert";

const route = useRoute();
const router = useRouter();

const props = defineProps({
	bookingId: {
		type: String,
		required: true,
	},
});

const showSuccessMessage = ref(false);

// Resource to check if ticket transfer is allowed
const transferEligibility = createResource({
	url: "events.api.can_transfer_ticket",
	auto: false,
});

const canTransferTickets = computed(() => {
	return transferEligibility.data?.can_transfer || false;
});

const onTicketTransferSuccess = () => {
	tickets.reload();
};

const booking = createDocumentResource({
	doctype: "Event Booking",
	name: props.bookingId,
	auto: true,
});

watch(
	() => booking.doc,
	() => {
		// If booking data changes, check if ticket transfer is allowed
		if (booking.doc?.event) {
			transferEligibility.submit({ event_id: booking.doc.event });
		}
	}
);

// Check if this is a successful payment redirect
onMounted(() => {
	if (route.query.success === "true") {
		showSuccessMessage.value = true;

		// Trigger confetti animation
		triggerConfetti();

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

const triggerConfetti = () => {
	// Multiple confetti bursts for celebration
	const duration = 3000;
	const animationEnd = Date.now() + duration;

	const randomInRange = (min, max) => Math.random() * (max - min) + min;

	const interval = setInterval(() => {
		const timeLeft = animationEnd - Date.now();

		if (timeLeft <= 0) {
			clearInterval(interval);
			return;
		}

		const particleCount = 50 * (timeLeft / duration);

		// Left side confetti
		confetti({
			particleCount,
			startVelocity: 30,
			spread: 360,
			origin: {
				x: randomInRange(0.1, 0.3),
				y: Math.random() - 0.2,
			},
		});

		// Right side confetti
		confetti({
			particleCount,
			startVelocity: 30,
			spread: 360,
			origin: {
				x: randomInRange(0.7, 0.9),
				y: Math.random() - 0.2,
			},
		});
	}, 250);
};

const tickets = useList({
	doctype: "Event Ticket",
	filters: { booking: props.bookingId },
	cacheKey: ["booking-tickets", props.bookingId],
	fields: [
		"name",
		"ticket_type.title as ticket_type",
		"attendee_name",
		"attendee_email",
		"qr_code",
		"event",
	],
	auto: true,
});
</script>
