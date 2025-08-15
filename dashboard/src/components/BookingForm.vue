<!-- BookingForm.vue -->
<template>
	<form @submit.prevent="submit" class="max-w-7xl mx-auto p-4">
		<div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
			<!-- Left Side: Form Inputs -->
			<div class="lg:col-span-2">
				<AttendeeFormControl
					v-for="(attendee, index) in attendees"
					:key="attendee.id"
					:attendee="attendee"
					:index="index"
					:available-ticket-types="availableTicketTypes"
					:available-add-ons="availableAddOns"
					:show-remove="attendees.length > 1"
					@remove="removeAttendee(index)"
				/>

				<!-- Add Attendee Button -->
				<div class="text-center mt-6">
					<Button
						variant="outline"
						size="lg"
						@click="addAttendee"
						class="w-full max-w-md border-dashed border-2 border-gray-300 hover:border-gray-400 text-gray-600 hover:text-gray-700 py-4"
					>
						+ Add Another Attendee
					</Button>
				</div>
			</div>

			<!-- Right Side: Summary and Submit -->
			<div class="lg:col-span-1">
				<div class="sticky top-4">
					<BookingSummary :summary="summary" :total="total" />
					<Button
						variant="solid"
						size="lg"
						class="w-full mt-3"
						type="submit"
						:loading="processBooking.loading"
					>
						{{ processBooking.loading ? "Processing..." : "Submit Booking" }}
					</Button>
				</div>
			</div>
		</div>
	</form>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import AttendeeFormControl from "./AttendeeFormControl.vue";
import BookingSummary from "./BookingSummary.vue";
import { createResource } from "frappe-ui";

// Props are passed from the parent context (e.g., your main app or page)
const props = defineProps({
	availableAddOns: {
		type: Array,
		default: () => [],
	},
	availableTicketTypes: {
		type: Array,
		default: () => [],
	},
});

// --- STATE ---
const attendees = ref([]);
const attendeeIdCounter = ref(0);

// --- HELPERS / DERIVED STATE ---
const addOnsMap = computed(() =>
	Object.fromEntries(props.availableAddOns.map((a) => [a.name, a]))
);
const ticketTypesMap = computed(() =>
	Object.fromEntries(props.availableTicketTypes.map((t) => [t.name, t]))
);
const eventId = computed(() => props.availableTicketTypes[0]?.event || null);

// --- METHODS ---
const createNewAttendee = () => {
	attendeeIdCounter.value++;
	const newAttendee = {
		id: attendeeIdCounter.value,
		full_name: "",
		email: "",
		ticket_type: props.availableTicketTypes[0]?.name || "",
		add_ons: {},
	};
	for (const addOn of props.availableAddOns) {
		newAttendee.add_ons[addOn.name] = {
			selected: false,
			option: addOn.options ? addOn.options[0] || null : null,
		};
	}
	return newAttendee;
};

const addAttendee = () => {
	attendees.value.push(createNewAttendee());
};

const removeAttendee = (index) => {
	attendees.value.splice(index, 1);
};

// --- COMPUTED PROPERTIES FOR SUMMARY ---
const summary = computed(() => {
	const summaryData = { tickets: {}, add_ons: {} };

	for (const attendee of attendees.value) {
		const ticketType = attendee.ticket_type;
		if (ticketType && ticketTypesMap.value[ticketType]) {
			if (!summaryData.tickets[ticketType]) {
				summaryData.tickets[ticketType] = {
					count: 0,
					amount: 0,
					price: ticketTypesMap.value[ticketType].price,
					title: ticketTypesMap.value[ticketType].title,
				};
			}
			summaryData.tickets[ticketType].count++;
			summaryData.tickets[ticketType].amount += ticketTypesMap.value[ticketType].price;
		}

		for (const addOnName in attendee.add_ons) {
			if (attendee.add_ons[addOnName].selected) {
				if (!summaryData.add_ons[addOnName]) {
					summaryData.add_ons[addOnName] = {
						count: 0,
						amount: 0,
						price: addOnsMap.value[addOnName].price,
						title: addOnsMap.value[addOnName].title,
					};
				}
				summaryData.add_ons[addOnName].count++;
				summaryData.add_ons[addOnName].amount += addOnsMap.value[addOnName].price;
			}
		}
	}
	return summaryData;
});

const total = computed(() => {
	let currentTotal = 0;
	for (const key in summary.value.tickets) {
		currentTotal += summary.value.tickets[key].amount;
	}
	for (const key in summary.value.add_ons) {
		currentTotal += summary.value.add_ons[key].amount;
	}
	return currentTotal;
});

// --- WATCHER ---
// Initialize with one attendee when component mounts
watch(
	() => props.availableTicketTypes,
	() => {
		if (attendees.value.length === 0 && props.availableTicketTypes.length > 0) {
			attendees.value.push(createNewAttendee());
		}
	},
	{ immediate: true }
);

const processBooking = createResource({
	url: "events.api.process_booking",
});

// --- FORM SUBMISSION ---
async function submit() {
	if (processBooking.loading) return;

	const attendees_payload = attendees.value.map((attendee) => {
		const cleanAttendee = JSON.parse(JSON.stringify(attendee));
		const selected_add_ons = [];
		for (const addOnName in cleanAttendee.add_ons) {
			const addOnState = cleanAttendee.add_ons[addOnName];
			if (addOnState.selected) {
				selected_add_ons.push({
					add_on: addOnName,
					value: addOnState.option || true,
				});
			}
		}
		cleanAttendee.add_ons = selected_add_ons;
		return cleanAttendee;
	});

	const final_payload = {
		event: eventId.value,
		attendees: attendees_payload,
		redirect_to: "/dashboard/bookings",
	};

	processBooking.submit(final_payload, {
		onSuccess: (data) => {
			window.location.href = data;
		},
	});
}
</script>
