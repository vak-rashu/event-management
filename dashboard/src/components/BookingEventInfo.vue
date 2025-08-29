<template>
	<div class="bg-surface-cards border border-outline-gray-1 rounded-lg p-6">
		<h3 class="text-lg font-semibold text-ink-gray-9 mb-4">{{ event.title }}</h3>

		<div class="space-y-3">
			<!-- Date & Time -->
			<div class="flex justify-between items-center text-ink-gray-7">
				<span class="flex items-center">
					<LucideCalendarDays class="w-4 h-4 mr-2 flex-shrink-0" />
					Date & Time
				</span>
				<div class="text-right">
					<p class="font-medium text-ink-gray-9">{{ formatDate(event.start_date) }}</p>
					<p v-if="event.start_time" class="text-sm text-ink-gray-6">
						{{ formatTime(event.start_time) }}
					</p>
				</div>
			</div>

			<!-- Venue -->
			<div v-if="event.venue" class="flex justify-between items-center text-ink-gray-7">
				<span class="flex items-center">
					<LucideMapPin class="w-4 h-4 mr-2 flex-shrink-0" />
					Venue
				</span>
				<div class="text-right">
					<p class="font-medium text-ink-gray-9">{{ event.venue }}</p>
				</div>
			</div>

			<!-- Event Description -->
			<div v-if="event.short_description" class="pt-2 border-t border-outline-gray-1">
				<p class="text-sm text-ink-gray-6">{{ event.short_description }}</p>
			</div>
		</div>
	</div>
</template>

<script setup>
import LucideCalendar from "~icons/lucide/calendar";
import LucideCalendarDays from "~icons/lucide/calendar-days";
import LucideMapPin from "~icons/lucide/map-pin";

defineProps({
	event: {
		type: Object,
		required: true,
		validator: (value) => {
			return (
				typeof value.title === "string" &&
				value.start_date &&
				typeof value.route === "string"
			);
		},
	},
});

const formatDate = (dateString) => {
	return new Date(dateString).toLocaleDateString("en-US", {
		weekday: "long",
		year: "numeric",
		month: "long",
		day: "numeric",
	});
};

const formatTime = (timeString) => {
	if (!timeString) return "";
	const time = new Date(`2000-01-01T${timeString}`);
	return time.toLocaleTimeString("en-US", {
		hour: "numeric",
		minute: "2-digit",
		hour12: true,
	});
};
</script>
