import { userResource } from "@/data/user";
import { createRouter, createWebHistory } from "vue-router";
import { session } from "./data/session";

const routes = [
	{
		path: "/",
		name: "dashboard",
		component: () => import("@/pages/Dashboard.vue"),
	},
	{
		path: "/book-tickets/:eventRoute",
		props: true,
		name: "event-booking",
		component: () => import("@/pages/EventBooking.vue"),
	},
	{
		path: "/bookings",
		name: "bookings-list",
		component: () => import("@/pages/BookingsList.vue"),
	},
	{
		path: "/bookings/:bookingId",
		props: true,
		name: "booking-details",
		component: () => import("@/pages/BookingDetails.vue"),
	},
];

const router = createRouter({
	history: createWebHistory("/dashboard"),
	routes,
});

router.beforeEach(async (to, from, next) => {
	let isLoggedIn = session.isLoggedIn;
	try {
		await userResource.promise;
	} catch (error) {
		isLoggedIn = false;
	}

	if (to.name === "Login" && isLoggedIn) {
		next({ name: "Home" });
	} else if (to.name !== "Login" && !isLoggedIn) {
		window.location.href = `/login?redirect-to=${encodeURIComponent(to.fullPath)}`;
	} else {
		next();
	}
});

export default router;
