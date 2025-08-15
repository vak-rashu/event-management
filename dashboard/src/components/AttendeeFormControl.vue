<!-- AttendeeCard.vue -->
<template>
	<div class="bg-white border border-gray-300 rounded-xl p-4 md:p-6 mb-6 shadow-sm">
		<h4 class="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
			Attendee {{ index + 1 }}
		</h4>

		<!-- Name and Email Fields -->
		<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
			<div>
				<label class="block mb-1 text-sm font-medium text-gray-700"> Full Name </label>
				<input
					v-model="attendee.full_name"
					placeholder="Enter full name"
					required
					type="text"
					class="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
				/>
			</div>
			<div>
				<label class="block mb-1 text-sm font-medium text-gray-700">Email</label>
				<input
					v-model="attendee.email"
					placeholder="Enter email address"
					required
					type="email"
					class="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
				/>
			</div>
		</div>

		<!-- Ticket Type -->
		<div class="mb-4">
			<label class="block mb-1 text-sm font-medium text-gray-700"> Ticket Type </label>
			<select
				v-model="attendee.ticket_type"
				class="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
			>
				<option v-for="tt in availableTicketTypes" :key="tt.name" :value="tt.name">
					{{ tt.title }} (₹{{ tt.price }})
				</option>
			</select>
		</div>

		<!-- Add-ons -->
		<div v-if="availableAddOns.length > 0">
			<h5 class="text-md font-semibold text-gray-700 mt-6 mb-3">Add-ons</h5>
			<div v-for="addOn in availableAddOns" :key="addOn.name" class="mb-3">
				<div class="flex items-center">
					<input
						type="checkbox"
						v-model="attendee.add_ons[addOn.name].selected"
						:id="`add_on_${addOn.name}_${index}`"
						class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
					/>
					<label
						:for="`add_on_${addOn.name}_${index}`"
						class="ml-2 text-sm text-gray-700"
					>
						{{ addOn.title }} (₹{{ addOn.price }})
					</label>
				</div>

				<div
					v-if="addOn.user_selects_option && attendee.add_ons[addOn.name].selected"
					class="mt-2 ml-6"
				>
					<select
						v-model="attendee.add_ons[addOn.name].option"
						class="w-full md:w-1/2 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
					>
						<option v-for="option in addOn.options" :key="option" :value="option">
							{{ option }}
						</option>
					</select>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
defineProps({
	attendee: { type: Object, required: true },
	index: { type: Number, required: true },
	availableTicketTypes: { type: Array, required: true },
	availableAddOns: { type: Array, required: true },
});
</script>
