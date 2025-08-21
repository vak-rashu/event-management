import { useStorage } from "@vueuse/core";

/**
 * Composable for managing booking form localStorage data
 * This allows components to access and clear booking form data stored in localStorage
 */
export function useBookingFormStorage() {
	// Use the same storage keys as in BookingForm.vue
	const attendees = useStorage("event-booking-attendees", []);
	const attendeeIdCounter = useStorage("event-booking-counter", 0);

	/**
	 * Clear all stored booking form data
	 * This should be called when payment is successful
	 */
	const clearStoredData = () => {
		attendees.value = [];
		attendeeIdCounter.value = 0;
	};

	/**
	 * Check if there's any stored booking data
	 */
	const hasStoredData = () => {
		return attendees.value.length > 0;
	};

	return {
		attendees,
		attendeeIdCounter,
		clearStoredData,
		hasStoredData,
	};
}
