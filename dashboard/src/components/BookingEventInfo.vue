<template>
	<div class="bg-surface-white border border-outline-gray-1 rounded-lg p-6 mb-6">
		<div class="flex items-start space-x-4">
			<!-- Event Details -->
			<div class="flex-1 min-w-0">
				<h3 class="text-xl font-semibold text-ink-gray-9 mb-2">{{ event.title }}</h3>

				<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
					<!-- Date & Time -->
					<div class="flex items-center text-ink-gray-7">
						<LucideCalendarDays class="w-4 h-4 mr-2 flex-shrink-0" />
						<div>
							<p class="font-medium">{{ formatDate(event.start_date) }}</p>
							<p v-if="event.start_time" class="text-sm text-ink-gray-6">
								{{ formatTime(event.start_time) }}
							</p>
						</div>
					</div>

					<!-- Venue -->
					<div v-if="event.venue" class="flex items-center text-ink-gray-7">
						<LucideMapPin class="w-4 h-4 mr-2 flex-shrink-0" />
						<div>
							<p class="font-medium">{{ event.venue }}</p>
							<p class="text-sm text-ink-gray-6">Venue</p>
						</div>
					</div>
				</div>

				<!-- Event Description -->
				<div v-if="event.short_description" class="mt-3 text-ink-gray-6 text-sm">
					<p>{{ event.short_description }}</p>
				</div>
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
