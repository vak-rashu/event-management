<!-- BookingForm.vue -->
<template>
	<form @submit.prevent="submit" class="max-w-7xl mx-auto p-4">
		<div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
			<!-- Left Side: Form Inputs -->
			<div class="lg:col-span-2">
				<div class="bg-white p-6 rounded-lg shadow-md mb-6">
					<label
						for="num_attendees"
						class="block mb-1 text-sm font-medium text-gray-700"
					>
						Number of Attendees
					</label>
					<input
						id="num_attendees"
						min="1"
						v-model.number="numAttendees"
						type="number"
						class="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
					/>
				</div>

				<AttendeeFormControl
					v-for="(attendee, index) in attendees"
					:key="index"
					:attendee="attendee"
					:index="index"
					:available-ticket-types="availableTicketTypes"
					:available-add-ons="availableAddOns"
				/>
			</div>

			<!-- Right Side: Summary and Submit -->
			<div class="lg:col-span-1">
				<div class="sticky top-4">
					<BookingSummary :summary="summary" :total="total" />
					<button
						type="submit"
						:disabled="submitting"
						class="w-full mt-6 py-3 px-4 text-lg font-semibold bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
					>
						{{ submitting ? "Processing..." : "Submit Booking" }}
					</button>
				</div>
			</div>
		</div>
	</form>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import AttendeeFormControl from "./AttendeeFormControl.vue";
import BookingSummary from "./BookingSummary.vue";

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
const numAttendees = ref(1);
const attendees = ref([]);
const submitting = ref(false);

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
	const newAttendee = {
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
watch(
	numAttendees,
	(newCount) => {
		const currentCount = attendees.value.length;
		if (newCount > currentCount) {
			for (let i = currentCount; i < newCount; i++) {
				attendees.value.push(createNewAttendee());
			}
		} else if (newCount < currentCount) {
			attendees.value.splice(newCount);
		}
	},
	{ immediate: true }
);

// --- FORM SUBMISSION ---
async function submit() {
	if (submitting.value) return;
	submitting.value = true;

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
		redirect_to: "/booking-confirmation",
	};

	try {
		const response = await fetch("/api/v2/method/events.api.process_booking", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				Accept: "application/json",
				"X-Frappe-CSRF-Token": window.frappe?.csrf_token || "",
			},
			body: JSON.stringify(final_payload),
		});

		if (!response.ok) {
			const errorData = await response.json();
			const errorMessage =
				JSON.parse(errorData.errors || "[]")[0] || "An unknown error occurred.";
			alert(errorMessage);
		} else {
			const { data } = await response.json();
			window.location.href = data;
		}
	} catch (error) {
		console.error("Submission failed:", error);
		alert("Could not connect to the server. Please try again later.");
	} finally {
		submitting.value = false;
	}
}
</script>
