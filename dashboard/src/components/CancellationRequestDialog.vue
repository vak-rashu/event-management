<template>
	<Dialog
		v-model="show"
		:options="{
			title: 'Request Ticket Cancellation',
			size: '3xl',
		}"
	>
		<template #body-content>
			<div class="space-y-6">
				<p class="text-ink-gray-7">
					Select the tickets you would like to cancel. Please note that cancellation
					requests are subject to approval and refund policies.
				</p>

				<!-- Select All Option -->
				<div
					class="border border-gray-200 rounded-lg p-4 cursor-pointer transition-all hover:border-gray-400 hover:bg-gray-50"
					:class="{
						'border-gray-600 bg-gray-100': isAllSelected,
					}"
					@click="toggleSelectAll"
				>
					<div class="flex items-center space-x-3">
						<input
							type="checkbox"
							:checked="isAllSelected"
							@change="toggleSelectAll"
							class="h-4 w-4 text-gray-600 border-gray-300 rounded focus:ring-gray-500"
						/>
						<div>
							<h3 class="font-semibold text-ink-gray-9">Select All Tickets</h3>
							<p class="text-sm text-ink-gray-6">Cancel the entire booking</p>
						</div>
					</div>
				</div>

				<!-- Individual Ticket Selection -->
				<div class="space-y-4">
					<h4 class="font-medium text-ink-gray-8">Or select individual tickets:</h4>
					<div class="space-y-3 max-h-64 overflow-y-auto">
						<div
							v-for="ticket in tickets"
							:key="ticket.name"
							class="border border-gray-200 rounded-lg p-4 cursor-pointer transition-all hover:border-gray-400 hover:bg-gray-50"
							:class="{
								'border-gray-600 bg-gray-100': selectedTickets.includes(
									ticket.name
								),
							}"
							@click="toggleTicketSelection(ticket.name)"
						>
							<div class="flex items-start space-x-3">
								<input
									type="checkbox"
									:checked="selectedTickets.includes(ticket.name)"
									@change="toggleTicketSelection(ticket.name)"
									class="h-4 w-4 text-gray-600 border-gray-300 rounded focus:ring-gray-500 mt-1"
								/>
								<div class="flex-1">
									<div class="flex items-center justify-between">
										<div>
											<h3 class="font-semibold text-ink-gray-9">
												{{ ticket.attendee_name }}
											</h3>
											<p class="text-sm text-ink-gray-6">
												{{ ticket.attendee_email }}
											</p>
											<p class="text-sm text-ink-gray-5">
												{{ ticket.ticket_type }}
											</p>
										</div>
									</div>

									<!-- Add-ons if any -->
									<div
										v-if="ticket.add_ons && ticket.add_ons.length > 0"
										class="mt-2 pt-2 border-t border-gray-100"
									>
										<p class="text-xs text-ink-gray-5 mb-1">Add-ons:</p>
										<div class="flex flex-wrap gap-1">
											<span
												v-for="addon in ticket.add_ons"
												:key="addon.name"
												class="inline-flex items-center px-2 py-1 rounded-full text-xs bg-gray-100 text-gray-700"
											>
												{{ addon.title }}: {{ addon.value }}
											</span>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- Warning if no tickets selected -->
				<div v-if="selectedTickets.length === 0" class="text-center py-4">
					<p class="text-red-600 text-sm">
						Please select at least one ticket to cancel.
					</p>
				</div>

				<!-- Summary -->
				<div
					v-if="selectedTickets.length > 0"
					class="p-4 bg-blue-50 border border-blue-200 rounded-lg"
				>
					<div class="flex items-center justify-between">
						<div>
							<h4 class="font-semibold text-blue-800">Cancellation Summary</h4>
							<p class="text-blue-700">
								{{ pluralize(selectedTickets.length, "ticket") }} selected for
								cancellation
								<span v-if="isAllSelected" class="font-medium"
									>(Full booking)</span
								>
							</p>
						</div>
						<div class="text-right">
							<p class="text-sm text-blue-600">Request Type</p>
							<p class="font-medium text-blue-800">
								{{ isAllSelected ? "Full Cancellation" : "Partial Cancellation" }}
							</p>
						</div>
					</div>
				</div>
			</div>
		</template>

		<template #actions>
			<div class="flex justify-end space-x-3">
				<Button variant="ghost" @click="closeDialog" :loading="submitting">
					Cancel
				</Button>
				<Button
					variant="solid"
					@click="submitCancellationRequest"
					:disabled="selectedTickets.length === 0"
					:loading="submitting"
				>
					Submit Cancellation Request
				</Button>
			</div>
		</template>
	</Dialog>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { Dialog, Button, createResource, toast } from "frappe-ui";
import { pluralize } from "../utils/pluralize.js";

const props = defineProps({
	modelValue: {
		type: Boolean,
		default: false,
	},
	tickets: {
		type: Array,
		required: true,
	},
	bookingId: {
		type: String,
		required: true,
	},
});

const emit = defineEmits(["update:modelValue", "success"]);

const show = computed({
	get: () => props.modelValue,
	set: (val) => emit("update:modelValue", val),
});

const selectedTickets = ref([]);
const submitting = ref(false);

const isAllSelected = computed({
	get: () => selectedTickets.value.length === props.tickets.length && props.tickets.length > 0,
	set: (val) => {
		if (val) {
			selectedTickets.value = props.tickets.map((ticket) => ticket.name);
		} else {
			selectedTickets.value = [];
		}
	},
});

const toggleSelectAll = () => {
	isAllSelected.value = !isAllSelected.value;
};

const toggleTicketSelection = (ticketId) => {
	const index = selectedTickets.value.indexOf(ticketId);
	if (index > -1) {
		selectedTickets.value.splice(index, 1);
	} else {
		selectedTickets.value.push(ticketId);
	}
};

const closeDialog = () => {
	show.value = false;
	selectedTickets.value = [];
};

const createCancellationRequest = createResource({
	url: "events.api.create_cancellation_request",
	onSuccess: (data) => {
		submitting.value = false;

		const ticketCount = selectedTickets.value.length;
		const isFullCancellation = isAllSelected.value;

		toast.success(
			isFullCancellation
				? "Full booking cancellation request submitted successfully!"
				: `Cancellation request submitted for ${pluralize(ticketCount, "ticket")}!`
		);
		emit("success", data);
		closeDialog();
	},

	onError: (error) => {
		submitting.value = false;
		toast.error(data.message || "Failed to submit cancellation request. Please try again.");
	},
});

const submitCancellationRequest = () => {
	if (selectedTickets.value.length === 0) return;

	submitting.value = true;
	createCancellationRequest.submit({
		booking_id: props.bookingId,
		ticket_ids: selectedTickets.value,
	});
};

// Reset selected tickets when dialog closes
watch(show, (newVal) => {
	if (!newVal) {
		selectedTickets.value = [];
	}
});
</script>
