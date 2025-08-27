import { createResource } from "frappe-ui";

export const userResource = createResource({
	url: "events.api.get_user_info",
	cache: "User",
	onError(error) {
		if (error && error.exc_type === "AuthenticationError") {
			window.location.href = "/login?redirect-to=dashboard";
		}
	},
});
