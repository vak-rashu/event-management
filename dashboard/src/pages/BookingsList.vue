<template>
	<div>
		<h2 class="text-ink-gray-9 font-semibold text-lg mb-3">Your Bookings</h2>
		<ListView
			v-if="bookings.data"
			:columns="columns"
			:rows="bookings.data"
			row-key="name"
			:options="{
				selectable: false,
				getRowRoute: (row) => ({
					name: 'booking-details',
					params: { bookingId: row.name },
				}),
			}"
		>
			<template #cell="{ item, row, column }">
				<Badge
					v-if="column.key === 'status'"
					:theme="row.status === 'Confirmed' ? 'green' : 'red'"
					variant="subtle"
					size="sm"
				>
					{{ item }}
				</Badge>
				<span v-else>{{ item }}</span>
			</template>
		</ListView>
	</div>
</template>

<script setup>
import { ListView, useList, Badge } from "frappe-ui";
import { session } from "../data/session";
import { formatCurrency } from "../utils/currency";
import { dayjsLocal } from "frappe-ui";
import { pluralize } from "../utils/pluralize";

const columns = [
	{ label: "Event", key: "event_title" },
	{ label: "", key: "ticket_count" },
	{ label: "Start Date", key: "start_date" },
	{ label: "Venue", key: "venue" },
	{ label: "Amount Paid", key: "formatted_amount" },
	{ label: "Status", key: "status" },
];

const bookings = useList({
	doctype: "Event Booking",
	fields: [
		"name",
		"event",
		"event.title as event_title",
		"event.start_date",
		"event.venue",
		"docstatus",
		"total_amount",
		"currency",
		"creation",
		{ attendees: ["ticket_type"] },
	],
	filters: { user: session.user, docstatus: ["!=", "0"] },
	orderBy: "creation desc",
	realtime: true,
	auto: true,
	cacheKey: "bookings-list",
	onError: console.error,
	transform(data) {
		return data.map((booking) => ({
			...booking,
			formatted_amount:
				booking.total_amount !== 0
					? formatCurrency(booking.total_amount, booking.currency)
					: "FREE",
			status: booking.docstatus === 1 ? "Confirmed" : "Cancelled",
			start_date: dayjsLocal(booking.start_date).format("MMM DD, YYYY"),
			ticket_count: pluralize(booking.attendees ? booking.attendees.length : 0, "Ticket"),
		}));
	},
});
</script>
