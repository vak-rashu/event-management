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
			<p class="text-sm text-gray-600">
				<img :src="ticket.qr_code" alt="QR Code" />
			</p>
		</div>

		<!-- Ticket Transfer Dialog -->
		<TicketTransferDialog
			v-model="showTransferDialog"
			:ticket="ticket"
			@success="onTicketTransferSuccess"
		/>
	</li>
</template>

<script setup>
import { ref, computed } from "vue";
import { Button, Dropdown } from "frappe-ui";
import TicketTransferDialog from "./TicketTransferDialog.vue";
import LucideUserPen from "~icons/lucide/user-pen";

const props = defineProps({
	ticket: {
		type: Object,
		required: true,
	},
	canTransfer: {
		type: Boolean,
		default: false,
	},
});

const emit = defineEmits(["transfer-success"]);

const showTransferDialog = ref(false);

const ticketActions = computed(() => {
	// Only show transfer action if transfers are allowed
	if (!props.canTransfer) {
		return [];
	}

	return [
		{
			label: "Transfer Ticket",
			icon: LucideUserPen,
			onClick: () => {
				showTransferDialog.value = true;
			},
		},
	];
});

const onTicketTransferSuccess = () => {
	emit("transfer-success");
};
</script>
