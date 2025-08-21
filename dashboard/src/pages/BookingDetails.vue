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

		<!-- Cancellation Request Section -->
		<div v-if="bookingDetails.data.cancellation_request" class="mb-6">
			<div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
				<div class="flex items-center">
					<LucideInfo class="w-5 h-5 text-blue-600 mr-3" />
					<div>
						<h3 class="text-blue-800 font-semibold">Cancellation Requested</h3>
						<p class="text-blue-700">
							<span
								v-if="bookingDetails.data.cancellation_request.cancel_full_booking"
							>
								Full booking cancellation has been requested.
							</span>
							<span v-else>
								Partial cancellation has been requested for selected tickets.
							</span>
							Request submitted on
							{{ formatDate(bookingDetails.data.cancellation_request.creation) }}.
						</p>
					</div>
				</div>
			</div>
		</div>

		<div>
			<div class="flex justify-between items-center mb-3">
				<h3 class="text-ink-gray-8 font-semibold text-lg">Tickets</h3>

				<!-- Request Cancellation Button -->
				<Button
					v-if="canRequestCancellation && !bookingDetails.data.cancellation_request"
					variant="outline"
					@click="showCancellationDialog = true"
					class="text-red-600 border-red-300 hover:bg-red-50"
				>
					Request Cancellation
				</Button>
			</div>

			<!-- Cancellation restriction notice -->
			<div
				v-if="!canRequestCancellation && !bookingDetails.data.cancellation_request"
				class="mb-4 bg-red-50 border border-red-200 rounded-lg p-4"
			>
				<div class="flex items-center">
					<LucideTriangleAlert class="w-5 h-5 text-red-600 mr-3" />
					<div>
						<p class="text-red-800 text-sm">
							<strong>Ticket cancellation requests are no longer available</strong> -
							The cancellation window has closed as the event is approaching.
						</p>
					</div>
				</div>
			</div>

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

			<!-- Add-on change restriction notice -->
			<div
				v-if="!canChangeAddOns"
				class="mb-4 bg-orange-50 border border-orange-200 rounded-lg p-4"
			>
				<div class="flex items-center">
					<LucideTriangleAlert class="w-5 h-5 text-orange-600 mr-3" />
					<div>
						<p class="text-orange-800 text-sm">
							<strong>Add-on preference changes are no longer available</strong> -
							The change window has closed as the event is approaching.
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
					:can-change-add-ons="canChangeAddOns"
					:is-cancelled="isCancelledTicket(ticket.name)"
					@transfer-success="onTicketTransferSuccess"
				/>
			</ol>
		</div>

		<CancellationRequestDialog
			v-model="showCancellationDialog"
			:tickets="bookingDetails.data.tickets"
			:booking-id="bookingId"
			@success="onCancellationRequestSuccess"
		/>
	</div>
</template>

<script setup>
import { ref, computed } from "vue";
import { createResource, Spinner, Button } from "frappe-ui";
import { usePaymentSuccess } from "../composables/usePaymentSuccess.js";
import { useBookingFormStorage } from "../composables/useBookingFormStorage.js";
import TicketCard from "../components/TicketCard.vue";
import CancellationRequestDialog from "../components/CancellationRequestDialog.vue";
import LucideTriangleAlert from "~icons/lucide/triangle-alert";
import LucideCheckCircle from "~icons/lucide/check-circle";
import LucideInfo from "~icons/lucide/info";

const props = defineProps({
	bookingId: {
		type: String,
		required: true,
	},
});

// Use booking form storage composable to clear data on successful payment
const { clearStoredData } = useBookingFormStorage();

// Use payment success composable with callback to clear booking form data
const { showSuccessMessage } = usePaymentSuccess({
	onSuccess: () => {
		// Clear any stored booking form data when payment is successful
		clearStoredData();
	},
});

const showCancellationDialog = ref(false);

const bookingDetails = createResource({
	url: "events.api.get_booking_details",
	params: { booking_id: props.bookingId },
	auto: true,
});

const canTransferTickets = computed(() => {
	return bookingDetails.data?.can_transfer_ticket?.can_transfer || false;
});

const canChangeAddOns = computed(() => {
	return bookingDetails.data?.can_change_add_ons?.can_change_add_ons || false;
});

const canRequestCancellation = computed(() => {
	return bookingDetails.data?.can_request_cancellation?.can_request_cancellation || false;
});

const isCancelledTicket = (ticketId) => {
	return bookingDetails.data?.cancelled_tickets?.includes(ticketId) || false;
};

const formatDate = (dateString) => {
	return new Date(dateString).toLocaleDateString();
};

const onTicketTransferSuccess = () => {
	bookingDetails.reload();
};

const onCancellationRequestSuccess = (data) => {
	bookingDetails.reload();
};
</script>
