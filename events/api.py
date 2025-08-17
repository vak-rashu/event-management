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


@frappe.whitelist()
def transfer_ticket(ticket_id: str, new_name: str, new_email: str):
	"""Transfer a ticket to a new attendee."""
	ticket = frappe.get_doc("Event Ticket", ticket_id)
	if not ticket:
		frappe.throw(frappe._("Ticket not found."))

	# Store old attendee info for notification
	old_name = ticket.attendee_name
	old_email = ticket.attendee_email

	ticket.attendee_name = new_name
	ticket.attendee_email = new_email
	ticket.save(ignore_permissions=True)

	# Send email notifications
	send_ticket_transfer_emails(ticket.name, old_name, old_email, new_name, new_email)


def send_ticket_transfer_emails(ticket_id: str, old_name: str, old_email: str, new_name: str, new_email: str):
	"""Send email notifications for ticket transfer."""
	try:
		# Get ticket and event details
		ticket = frappe.get_doc("Event Ticket", ticket_id)
		event = frappe.get_doc("FE Event", ticket.event)
		booking = frappe.get_doc("Event Booking", ticket.booking)

		# Email to old attendee - notification of transfer
		old_attendee_subject = f"Your ticket for {event.title} has been transferred"
		old_attendee_message = f"""
		<p>Dear {old_name},</p>

		<p>This is to inform you that your ticket for <strong>{event.title}</strong> has been transferred to {new_name} ({new_email}).</p>

		<p><strong>Event Details:</strong></p>
		<ul>
			<li><strong>Event:</strong> {event.title}</li>
			<li><strong>Date:</strong> {frappe.format(event.start_date, 'Date')}</li>
			<li><strong>Ticket Type:</strong> {ticket.ticket_type}</li>
			<li><strong>Booking ID:</strong> {booking.name}</li>
		</ul>

		<p>If you have any questions about this transfer, please contact us.</p>

		<p>Best regards,<br>
		{event.title} Team</p>
		"""

		frappe.sendmail(
			recipients=[old_email], subject=old_attendee_subject, message=old_attendee_message, delayed=False
		)

		# Email to new attendee - welcome and ticket details
		new_attendee_subject = f"Welcome! Your ticket for {event.title}"
		new_attendee_message = f"""
		<p>Dear {new_name},</p>

		<p>Great news! A ticket for <strong>{event.title}</strong> has been transferred to you.</p>

		<p><strong>Event Details:</strong></p>
		<ul>
			<li><strong>Event:</strong> {event.title}</li>
			<li><strong>Date:</strong> {frappe.format(event.start_date, 'Date')}</li>
			<li><strong>Time:</strong> {frappe.format(event.start_time, 'Time') if event.start_time else 'TBA'}</li>
			<li><strong>Venue:</strong> {event.venue or 'TBA'}</li>
			<li><strong>Ticket Type:</strong> {ticket.ticket_type}</li>
			<li><strong>Booking ID:</strong> {booking.name}</li>
		</ul>

		<p><strong>Your Ticket Details:</strong></p>
		<ul>
			<li><strong>Ticket ID:</strong> {ticket.name}</li>
			<li><strong>Attendee Name:</strong> {new_name}</li>
			<li><strong>Email:</strong> {new_email}</li>
		</ul>

		<p>Please save this email for your records. You may need to present this ticket information at the event entrance.</p>

		<p>We look forward to seeing you at the event!</p>

		<p>Best regards,<br>
		{event.title} Team</p>
		"""

		frappe.sendmail(
			recipients=[new_email], subject=new_attendee_subject, message=new_attendee_message, delayed=False
		)

	except Exception as e:
		frappe.log_error(f"Failed to send ticket transfer emails for ticket {ticket_id}: {e!s}")
		# Don't raise the exception to avoid failing the main transfer process
