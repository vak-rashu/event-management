# Copyright (c) 2025, BWH Studios and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EventBooking(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from events.ticketing.doctype.event_booking_attendee.event_booking_attendee import (
			EventBookingAttendee,
		)

		amended_from: DF.Link | None
		attendees: DF.Table[EventBookingAttendee]
		currency: DF.Link
		event: DF.Link
		total_amount: DF.Currency
		user: DF.Link
	# end: auto-generated types

	def validate(self):
		self.set_total()
		self.set_currency()

	def set_currency(self):
		self.currency = self.attendees[0].currency

	def set_total(self):
		self.total_amount = 0
		for attendee in self.attendees:
			attendee.add_on_total = attendee.get_add_on_total()
			attendee.number_of_add_ons = attendee.get_number_of_add_ons()
			self.total_amount += attendee.amount
			self.total_amount += attendee.add_on_total

	def on_submit(self):
		self.generate_tickets()

	def generate_tickets(self):
		for attendee in self.attendees:
			ticket = frappe.new_doc("Event Ticket")
			ticket.event = self.event
			ticket.booking = self.name
			ticket.ticket_type = attendee.ticket_type
			ticket.attendee_name = attendee.full_name

			if attendee.add_ons:
				add_ons_list = frappe.get_cached_doc("Attendee Ticket Add-on", attendee.add_ons).add_ons
				ticket.add_ons = add_ons_list
			ticket.insert().submit()
