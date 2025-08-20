<template>
	<li class="shadow-md p-4 rounded-lg bg-white relative">
		<!-- Three-dot dropdown menu -->
		<div class="absolute top-2 right-2">
			<Dropdown :options="ticketActions" placement="left" v-if="ticketActions.length > 0">
				<Button variant="ghost" icon="more-horizontal" size="sm" />
			</Dropdown>
		</div>

		<div>
			<h4 class="text-md font-semibold text-gray-800">
				{{ ticket.attendee_name }}
			</h4>
			<p class="text-sm text-gray-600">Email: {{ ticket.attendee_email }}</p>
			<p class="text-sm text-gray-600">Ticket Type: {{ ticket.ticket_type }}</p>

			<!-- Add-ons Section -->
			<div v-if="ticket.add_ons && ticket.add_ons.length > 0" class="mt-3">
				<h5 class="text-sm font-medium text-gray-700 mb-2">Add-ons:</h5>
				<div class="space-y-1">
					<div
						v-for="addon in ticket.add_ons"
						:key="addon.name"
						class="flex justify-between items-center bg-gray-50 px-2 py-1 rounded text-xs"
					>
						<span class="font-medium text-gray-700">{{ addon.title }}:</span>
						<span class="text-gray-600">{{ addon.value }}</span>
					</div>
				</div>
			</div>

			<div class="mt-3">
				<img :src="ticket.qr_code" alt="QR Code" class="w-20 h-20" />
			</div>
		</div>

		<!-- Ticket Transfer Dialog -->
		<TicketTransferDialog
			v-model="showTransferDialog"
			:ticket="ticket"
			@success="onTicketTransferSuccess"
		/>

		<!-- Add-on Preference Dialog -->
		<AddOnPreferenceDialog
			v-model="showPreferenceDialog"
			:ticket="ticket"
			@success="onPreferenceChangeSuccess"
		/>
	</li>
</template>

<script setup>
import { ref, computed } from "vue";
import { Button, Dropdown } from "frappe-ui";
import TicketTransferDialog from "./TicketTransferDialog.vue";
import AddOnPreferenceDialog from "./AddOnPreferenceDialog.vue";
import LucideUserPen from "~icons/lucide/user-pen";
import LucideEdit from "~icons/lucide/edit";

const props = defineProps({
	ticket: {
		type: Object,
		required: true,
	},
	canTransfer: {
		type: Boolean,
		default: false,
	},
	canChangeAddOns: {
		type: Boolean,
		default: false,
	},
});

const emit = defineEmits(["transfer-success"]);

const showTransferDialog = ref(false);
const showPreferenceDialog = ref(false);

// Check if ticket has customizable add-ons
const hasCustomizableAddOns = computed(() => {
	return (
		props.ticket?.add_ons?.some((addon) => addon.options && addon.options.length > 0) || false
	);
});

const ticketActions = computed(() => {
	const actions = [];

	// Only show transfer action if transfers are allowed
	if (props.canTransfer) {
		actions.push({
			label: "Transfer Ticket",
			icon: LucideUserPen,
			onClick: () => {
				showTransferDialog.value = true;
			},
		});
	}

	// Only show preference action if add-on changes are allowed and ticket has customizable add-ons
	if (props.canChangeAddOns && hasCustomizableAddOns.value) {
		actions.push({
			label: "Change Add-on Preference",
			icon: LucideEdit,
			onClick: () => {
				showPreferenceDialog.value = true;
			},
		});
	}

	return actions;
});

const onTicketTransferSuccess = () => {
	emit("transfer-success");
};

const onPreferenceChangeSuccess = () => {
	emit("transfer-success");
};
</script>
