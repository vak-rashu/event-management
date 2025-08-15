<template>
	<div class="mb-6">
		<RouterLink :to="{ name: 'bookings-list' }" class="hover:underline">
			&larr; Back to Bookings
		</RouterLink>
	</div>

	<div class="w-4" v-if="booking.loading || tickets.loading">
		<Spinner />
	</div>

	<div v-else-if="booking.doc && tickets.list.data">
		<h2 class="text-ink-gray-9 font-semibold text-lg mb-3">
			Booking Details <span class="text-ink-gray-5 font-mono">(#{{ bookingId }})</span>
		</h2>
		<div>
			<!-- <pre>{{ JSON.stringify(booking.doc, null, 2) }}</pre> -->
			<h3 class="text-ink-gray-8 font-semibold text-lg mb-3">Tickets</h3>

			<ol class="grid grid-cols-3 gap-3">
				<li class="shadow-md p-4 rounded-lg bg-white" v-for="ticket in tickets.list.data">
					<div>
						<h4 class="text-md font-semibold text-gray-800">
							{{ ticket.attendee_name }}
						</h4>
						<p class="text-sm text-gray-600">Email: {{ ticket.attendee_email }}</p>
						<p class="text-sm text-gray-600">Ticket Type: {{ ticket.ticket_type }}</p>
						<p class="text-sm text-gray-600">
							<img :src="ticket.qr_code" alt="QR Code" />
						</p>
					</div>
				</li>
			</ol>
		</div>
	</div>
</template>

<script setup>
import { createDocumentResource, createListResource, Spinner } from "frappe-ui";

const props = defineProps({
	bookingId: {
		type: String,
		required: true,
	},
});

const booking = createDocumentResource({
	doctype: "Event Booking",
	name: props.bookingId,
	auto: true,
});

const tickets = createListResource({
	doctype: "Event Ticket",
	filters: { booking: props.bookingId },
	fields: [
		"name",
		"ticket_type.title as ticket_type",
		"attendee_name",
		"attendee_email",
		"qr_code",
	],
	auto: true,
});
</script>
