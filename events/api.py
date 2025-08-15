import frappe

from events.payments import get_payment_link_for_booking


@frappe.whitelist()
def get_event_booking_data(event_route: str) -> dict:
	data = frappe._dict()
	event_doc = frappe.get_cached_doc("FE Event", {"route": event_route})

	# Ticket Types
	available_ticket_types = []
	published_ticket_types = frappe.db.get_all(
		"Event Ticket Type", filters={"is_published": True, "event": event_doc.name}, pluck="name"
	)
	for ticket_type in published_ticket_types:
		tt = frappe.get_cached_doc("Event Ticket Type", ticket_type)
		if tt.are_tickets_available(1):
			available_ticket_types.append(tt)
	data.available_ticket_types = available_ticket_types

	# Ticket Add-ons
	add_ons = frappe.db.get_all(
		"Ticket Add-on",
		filters={"event": event_doc.name},
		fields=["name", "title", "price", "currency", "user_selects_option", "options"],
	)

	for add_on in add_ons:
		if add_on.user_selects_option:
			add_on.options = add_on.options.split("\n")

	data.available_add_ons = add_ons
	return data


@frappe.whitelist()
def process_booking(attendees: list[dict], event: str) -> str:
	booking = frappe.new_doc("Event Booking")
	booking.event = event
	booking.user = frappe.session.user
	for attendee in attendees:
		add_ons = attendee.get("add_ons", None)
		if add_ons:
			add_ons = create_add_on_doc(
				attendee_name=attendee["full_name"],
				add_ons=add_ons,
			)

		booking.append(
			"attendees",
			{
				"full_name": attendee.get("full_name"),
				"email": attendee.get("email"),
				"ticket_type": attendee.get("ticket_type"),
				"add_ons": add_ons.name if add_ons else None,
			},
		)

	booking.insert(ignore_permissions=True)
	frappe.db.commit()

	return get_payment_link_for_booking(
		booking.name, redirect_to=f"/dashboard/bookings/{booking.name}?success=true"
	)


def create_add_on_doc(attendee_name: str, add_ons: list[dict]):
	"""Create a new Attendee Ticket Add-on document."""
	return frappe.get_doc(
		{"doctype": "Attendee Ticket Add-on", "add_ons": add_ons, "attendee_name": attendee_name}
	).insert(ignore_permissions=True)
