<template>
	<div class="bg-white border border-gray-200 rounded-lg p-6 mb-6">
		<div class="flex items-center justify-between mb-4">
			<h3 class="text-lg font-semibold text-ink-gray-9">Payment Summary</h3>
			<Badge variant="solid" theme="green" size="sm">
				<template #prefix>
					<LucideCheckCircle class="w-3 h-3" />
				</template>
				Paid
			</Badge>
		</div>

		<div class="space-y-3">
			<!-- Net Amount -->
			<div class="flex justify-between items-center text-ink-gray-7">
				<span>Subtotal</span>
				<span class="font-medium">{{
					formatPrice(booking.net_amount || 0, booking.currency || "INR")
				}}</span>
			</div>

			<!-- Tax Information -->
			<div v-if="hasTax" class="flex justify-between items-center text-ink-gray-7">
				<span>GST ({{ booking.tax_percentage || 0 }}%)</span>
				<span class="font-medium">{{
					formatPrice(booking.tax_amount || 0, booking.currency || "INR")
				}}</span>
			</div>

			<!-- Divider -->
			<hr class="border-gray-200" />

			<!-- Total Amount -->
			<div class="flex justify-between items-center text-lg font-semibold text-ink-gray-9">
				<span>Total Paid</span>
				<span class="text-green-600">{{
					formatPrice(booking.total_amount || 0, booking.currency || "INR")
				}}</span>
			</div>
		</div>

		<!-- Zero amount case -->
		<div v-if="(booking.total_amount || 0) === 0" class="mt-4 p-3 bg-green-50 rounded-lg">
			<div class="flex items-start">
				<LucideGift class="w-4 h-4 text-green-600 mt-0.5 mr-2 flex-shrink-0" />
				<div class="text-sm text-green-800">
					<p class="font-medium">Free Event</p>
					<p>This was a free event with no payment required.</p>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed } from "vue";
import { Badge } from "frappe-ui";
import { formatPrice } from "../utils/currency.js";
import LucideCheckCircle from "~icons/lucide/check-circle";
import LucideGift from "~icons/lucide/gift";

const props = defineProps({
	booking: {
		type: Object,
		required: true,
		validator: (value) => {
			return typeof value === "object" && value !== null;
		},
	},
});

const hasTax = computed(() => {
	return Boolean(props.booking.tax_amount && props.booking.tax_amount > 0);
});
</script>
