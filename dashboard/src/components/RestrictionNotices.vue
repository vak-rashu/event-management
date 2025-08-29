<template>
	<div>
		<!-- Restriction notices -->
		<div v-if="!canRequestCancellation && !cancellationRequest" class="mb-4">
			<div class="bg-surface-red-1 border border-outline-red-1 rounded-lg p-4">
				<div class="flex items-center">
					<LucideTriangleAlert class="w-5 h-5 text-ink-red-2 mr-3" />
					<div>
						<p class="text-ink-red-3 text-sm">
							<strong>Ticket cancellation requests are no longer available</strong>
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
	</div>
</template>

<script setup>
import LucideTriangleAlert from "~icons/lucide/triangle-alert";

defineProps({
	canRequestCancellation: {
		type: Boolean,
		default: false,
	},
	canTransferTickets: {
		type: Boolean,
		default: false,
	},
	canChangeAddOns: {
		type: Boolean,
		default: false,
	},
	cancellationRequest: {
		type: Object,
		default: null,
	},
});
</script>
