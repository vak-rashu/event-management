import frappe

from events.payments import get_payment_link_for_booking


@frappe.whitelist()
def process_booking(attendees: list[dict], event: str, redirect_to: str = "/events") -> str:
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

	return get_payment_link_for_booking(booking.name, redirect_to=redirect_to)


def create_add_on_doc(attendee_name: str, add_ons: list[dict]):
	"""Create a new Attendee Ticket Add-on document."""
	return frappe.get_doc(
		{"doctype": "Attendee Ticket Add-on", "add_ons": add_ons, "attendee_name": attendee_name}
	).insert(ignore_permissions=True)
