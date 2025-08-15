<template>
	<div>
		<h2 class="text-ink-gray-9 font-semibold text-lg mb-3">Your Bookings</h2>
		<ListView
			v-if="bookings.list.data"
			:columns="[{ label: 'Event', key: 'event_title' }]"
			:rows="bookings.list.data"
			row-key="name"
			:options="{
				selectable: false,
				getRowRoute: (row) => ({
					name: 'booking-details',
					params: { bookingId: row.name },
				}),
			}"
		/>
	</div>
</template>

<script setup>
import { ListView, createListResource } from "frappe-ui";
import { session } from "../data/session";

const bookings = createListResource({
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
	],
	filters: { user: session.user, docstatus: ["!=", "0"] },
	orderBy: "creation desc",
	realtime: true,
	auto: true,
	onSuccess: console.log,
	onError: console.error,
});
</script>
