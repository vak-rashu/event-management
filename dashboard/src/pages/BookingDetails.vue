<template>
	<div class="mb-6 text-ink-gray-6">
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
				class="mb-6 bg-surface-green-1 border border-outline-green-1 rounded-lg p-4"
			>
				<div class="flex items-center">
					<LucideCheckCircle class="w-6 h-6 text-ink-green-2 mr-3" />
					<div>
						<h3 class="text-ink-green-3 font-semibold">Payment Successful! 🎉</h3>
						<p class="text-ink-green-2">
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

		<!-- Event Information and Payment Summary in two columns -->
		<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
			<!-- Event Information -->
			<BookingEventInfo
				v-if="bookingDetails.data.event"
				:event="bookingDetails.data.event"
			/>

			<!-- Booking Financial Summary -->
			<BookingFinancialSummary
				v-if="bookingDetails.data.doc"
				:booking="bookingDetails.data.doc"
			/>

			<!-- Booking Financial Summary -->
			<BookingFinancialSummary
				v-if="bookingDetails.data.booking_summary"
				:summary="bookingDetails.data.booking_summary"
			/>
		</div>

		<!-- Cancellation Request Section -->
		<div v-if="bookingDetails.data.cancellation_request" class="mb-6">
			<div class="bg-surface-blue-1 border border-outline-blue-1 rounded-lg p-4">
				<div class="flex items-center">
					<LucideInfo class="w-5 h-5 text-ink-blue-2 mr-3" />
					<div>
						<h3 class="text-ink-blue-3 font-semibold">Cancellation Requested</h3>
						<p class="text-ink-blue-2">
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

		<!-- Tickets Section -->
		<div class="bg-surface-cards border border-outline-gray-1 rounded-lg p-6">
			<div class="flex justify-between items-center mb-4">
				<h3 class="text-lg font-semibold text-ink-gray-9">Your Tickets</h3>

				<!-- Request Cancellation Button -->
				<Button
					v-if="canRequestCancellation && !bookingDetails.data.cancellation_request"
					variant="subtle"
					@click="showCancellationDialog = true"
				>
					Request Cancellation
				</Button>
			</div>

			<!-- Restriction notices -->
			<div
				v-if="!canRequestCancellation && !bookingDetails.data.cancellation_request"
				class="mb-4"
			>
				<div class="bg-surface-red-1 border border-outline-red-1 rounded-lg p-4">
					<div class="flex items-center">
						<LucideTriangleAlert class="w-5 h-5 text-ink-red-2 mr-3" />
						<div>
							<p class="text-ink-red-3 text-sm">
								<strong
									>Ticket cancellation requests are no longer available</strong
								>
								- The cancellation window has closed as the event is approaching.
							</p>
						</div>
					</div>
				</div>
			</div>

			<div v-if="!canTransferTickets" class="mb-4">
				<div class="bg-surface-amber-1 border border-outline-amber-1 rounded-lg p-4">
					<div class="flex items-center">
						<LucideTriangleAlert class="w-5 h-5 text-ink-amber-2 mr-3" />
						<div>
							<p class="text-ink-amber-3 text-sm">
								<strong>Ticket transfers are no longer available</strong> - The
								transfer window has closed as the event is approaching.
							</p>
						</div>
					</div>
				</div>
			</div>

			<div v-if="!canChangeAddOns" class="mb-4">
				<div class="bg-surface-orange-1 border border-outline-orange-1 rounded-lg p-4">
					<div class="flex items-center">
						<LucideTriangleAlert class="w-5 h-5 text-ink-orange-1 mr-3" />
						<div>
							<p class="text-ink-orange-1 text-sm">
								<strong>Add-on preference changes are no longer available</strong>
								- The change window has closed as the event is approaching.
							</p>
						</div>
					</div>
				</div>
			</div>

			<!-- Tickets Grid -->
			<ol class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
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
import BookingFinancialSummary from "../components/BookingFinancialSummary.vue";
import BookingEventInfo from "../components/BookingEventInfo.vue";
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
