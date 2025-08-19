<template>
	<div class="mb-6">
		<RouterLink :to="{ name: 'sponsorships-list' }" class="hover:underline">
			&larr; Back to Sponsorships
		</RouterLink>
	</div>

	<div class="w-4" v-if="enquiryDetails.loading">
		<Spinner />
	</div>

	<div v-else-if="enquiryDetails.data">
		<!-- Success Message (only shown on payment success) -->
		<Transition
			name="success-message"
			enter-active-class="transition-all duration-500 ease-out"
			leave-active-class="transition-all duration-500 ease-in"
			enter-from-class="opacity-0 transform -translate-y-4 scale-95"
			enter-to-class="opacity-100 transform translate-y-0 scale-100"
			leave-from-class="opacity-100 transform translate-y-0 scale-100"
			leave-to-class="opacity-0 transform -translate-y-4 scale-95"
		>
			<div
				v-if="showSuccessMessage"
				class="mb-6 bg-green-50 border border-green-200 rounded-lg p-4"
			>
				<div class="flex items-center">
					<LucideCheckCircle class="w-6 h-6 text-green-600 mr-3" />
					<div>
						<h3 class="text-green-800 font-semibold">Payment Successful! 🎉</h3>
						<p class="text-green-700">
							Your sponsorship payment has been confirmed. You'll receive
							confirmation details via email.
						</p>
					</div>
				</div>
			</div>
		</Transition>

		<h2 class="text-ink-gray-9 font-semibold text-lg mb-6">
			Sponsorship Inquiry Details
			<span class="text-ink-gray-5 font-mono">(#{{ enquiryId }})</span>
		</h2>

		<!-- Sponsorship Confirmation (shown at top if sponsored) -->
		<div v-if="sponsorDetails" class="mb-6 bg-green-50 border border-green-200 rounded-lg p-6">
			<div class="flex items-center mb-4">
				<LucideCheckCircle class="w-6 h-6 text-green-600 mr-3" />
				<h3 class="text-green-800 font-semibold text-lg">Sponsorship Confirmed</h3>
			</div>
			<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
				<div>
					<label class="block text-sm font-medium text-green-700 mb-1"
						>Sponsor Name</label
					>
					<p class="text-green-900">{{ sponsorDetails.company_name }}</p>
				</div>
				<div>
					<label class="block text-sm font-medium text-green-700 mb-1"
						>Confirmed On</label
					>
					<p class="text-green-900">{{ formatDate(sponsorDetails.creation) }}</p>
				</div>
				<div v-if="sponsorDetails.tier_title" class="md:col-span-2">
					<label class="block text-sm font-medium text-green-700 mb-1"
						>Sponsorship Tier</label
					>
					<p class="text-green-900">{{ sponsorDetails.tier_title }}</p>
				</div>
			</div>
		</div>

		<!-- Payment Pending Alert (shown at top for pending inquiries) -->
		<div
			v-else-if="enquiryDetails.data.enquiry.status === 'Pending'"
			class="mb-6 bg-orange-50 border border-orange-200 rounded-lg p-6"
		>
			<div class="flex items-center justify-between">
				<div class="flex items-center">
					<LucideClock class="w-6 h-6 text-orange-600 mr-3" />
					<div>
						<h3 class="text-orange-800 font-semibold">Payment Pending</h3>
						<p class="text-orange-700 text-sm mt-1">
							Your sponsorship inquiry has been submitted. Complete your payment to
							confirm your sponsorship.
						</p>
					</div>
				</div>
				<div>
					<Button variant="solid" theme="green" @click="showPaymentDialog = true">
						Pay Now
					</Button>
				</div>
			</div>
		</div>

		<div class="space-y-6">
			<!-- Company Information -->
			<div class="bg-white border border-gray-200 rounded-lg p-6">
				<h3 class="text-ink-gray-8 font-semibold text-lg mb-4">Company Information</h3>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
					<div>
						<label class="block text-sm font-medium text-ink-gray-6 mb-1"
							>Company Name</label
						>
						<p class="text-ink-gray-9">
							{{ enquiryDetails.data.enquiry.company_name }}
						</p>
					</div>
					<div v-if="enquiryDetails.data.enquiry.company_logo">
						<label class="block text-sm font-medium text-ink-gray-6 mb-1"
							>Company Logo</label
						>
						<img
							:src="enquiryDetails.data.enquiry.company_logo"
							:alt="enquiryDetails.data.enquiry.company_name"
							class="h-16 w-auto object-contain"
						/>
					</div>
				</div>
			</div>

			<!-- Event & Sponsorship Details -->
			<div class="bg-white border border-gray-200 rounded-lg p-6">
				<h3 class="text-ink-gray-8 font-semibold text-lg mb-4">Sponsorship Details</h3>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
					<div>
						<label class="block text-sm font-medium text-ink-gray-6 mb-1">Event</label>
						<p class="text-ink-gray-9">
							{{
								enquiryDetails.data.event_details.title ||
								enquiryDetails.data.enquiry.event
							}}
						</p>
					</div>
					<div v-if="enquiryDetails.data.enquiry.tier_title">
						<label class="block text-sm font-medium text-ink-gray-6 mb-1"
							>Sponsorship Tier</label
						>
						<p class="text-ink-gray-9">{{ enquiryDetails.data.enquiry.tier_title }}</p>
					</div>
					<div>
						<label class="block text-sm font-medium text-ink-gray-6 mb-1"
							>Status</label
						>
						<Badge
							:theme="getStatusTheme(enquiryDetails.data.enquiry.status)"
							variant="subtle"
							size="md"
						>
							{{ enquiryDetails.data.enquiry.status }}
						</Badge>
					</div>
					<div>
						<label class="block text-sm font-medium text-ink-gray-6 mb-1"
							>Submitted On</label
						>
						<p class="text-ink-gray-9">
							{{ formatDate(enquiryDetails.data.enquiry.creation) }}
						</p>
					</div>
				</div>
			</div>

			<!-- Event Information (if available) -->
			<div
				v-if="enquiryDetails.data.event_details"
				class="bg-white border border-gray-200 rounded-lg p-6"
			>
				<h3 class="text-ink-gray-8 font-semibold text-lg mb-4">Event Information</h3>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
					<div v-if="enquiryDetails.data.event_details.start_date">
						<label class="block text-sm font-medium text-ink-gray-6 mb-1"
							>Event Date</label
						>
						<p class="text-ink-gray-9">
							{{ formatDate(enquiryDetails.data.event_details.start_date) }}
						</p>
					</div>
					<div v-if="enquiryDetails.data.event_details.venue">
						<label class="block text-sm font-medium text-ink-gray-6 mb-1">Venue</label>
						<p class="text-ink-gray-9">
							{{ enquiryDetails.data.event_details.venue }}
						</p>
					</div>
				</div>
				<div v-if="enquiryDetails.data.event_details.short_description" class="mt-4">
					<label class="block text-sm font-medium text-ink-gray-6 mb-1"
						>Event Description</label
					>
					<p class="text-ink-gray-9">
						{{ enquiryDetails.data.event_details.short_description }}
					</p>
				</div>
				<div v-if="enquiryDetails.data.event_details.about" class="mt-4">
					<label class="block text-sm font-medium text-ink-gray-6 mb-1"
						>About Event</label
					>
					<div
						class="text-ink-gray-9"
						v-html="enquiryDetails.data.event_details.about"
					></div>
				</div>
			</div>
		</div>
	</div>

	<div v-else-if="enquiryDetails.error" class="text-center py-8">
		<div class="text-red-600 text-lg mb-2">Error loading sponsorship details</div>
		<div class="text-ink-gray-4 text-sm">{{ enquiryDetails.error }}</div>
	</div>

	<!-- Payment Dialog -->
	<SponsorshipPaymentDialog
		v-if="enquiryDetails.data && enquiryDetails.data.enquiry.status === 'Pending'"
		v-model:open="showPaymentDialog"
		:enquiry-id="enquiryId"
		:event-id="enquiryDetails.data?.enquiry.event"
		:event-title="enquiryDetails.data?.event_details.title"
		@payment-started="onPaymentStarted"
	/>
</template>

<script setup>
import { computed, ref } from "vue";
import { createResource, Spinner, Badge, Button } from "frappe-ui";
import { dayjsLocal } from "frappe-ui";
import LucideCheckCircle from "~icons/lucide/check-circle";
import LucideClock from "~icons/lucide/clock";
import SponsorshipPaymentDialog from "../components/SponsorshipPaymentDialog.vue";
import { usePaymentSuccess } from "../composables/usePaymentSuccess.js";

const props = defineProps({
	enquiryId: {
		type: String,
		required: true,
	},
});

const showPaymentDialog = ref(false);

const enquiryDetails = createResource({
	url: "events.api.get_sponsorship_details",
	params: {
		enquiry_id: props.enquiryId,
	},
	auto: true,
});

// Use the payment success composable
const { showSuccessMessage } = usePaymentSuccess({
	onSuccess: () => {
		// Reload the enquiry details to get updated status
		enquiryDetails.reload();
	},
});

// Extract sponsor details from the response
const sponsorDetails = computed(() => {
	return enquiryDetails.data?.sponsor_details || null;
});

const getStatusTheme = (status) => {
	switch (status) {
		case "Paid":
			return "green";
		case "Pending":
			return "orange";
		case "Withdrawn":
			return "red";
		default:
			return "gray";
	}
};

const formatDate = (dateString) => {
	return dayjsLocal(dateString).format("MMM DD, YYYY");
};

const onPaymentStarted = () => {
	// Optional: Show a loading state or toast message
	console.log("Payment process started");
};
</script>
