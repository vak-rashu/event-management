# Copyright (c) 2025, BWH Studios and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class IntegrationTestEventTicket(IntegrationTestCase):
	"""
	Integration tests for EventTicket.
	Use this class for testing interactions between multiple components.
	"""

	def test_disallow_ticket_creation_after_max_tickets(self):
		test_event = frappe.get_doc("FE Event", {"route": "test-route"})
		test_ticket_type = frappe.get_doc(
			{
				"doctype": "Event Ticket Type",
				"event": test_event.name,
				"title": "VIP",
				"price": 500,
				"is_published": True,
				"max_tickets_available": 2,
			}
		).insert()

		# 1
		frappe.get_doc(
			{"doctype": "Event Ticket", "ticket_type": test_ticket_type.name, "attendee_name": "John Doe"}
		).insert().submit()
		# 2
		frappe.get_doc(
			{"doctype": "Event Ticket", "ticket_type": test_ticket_type.name, "attendee_name": "Jenny Doe"}
		).insert().submit()

		# 3 should throw
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{
					"doctype": "Event Ticket",
					"ticket_type": test_ticket_type.name,
					"attendee_name": "Jacob Doe",
				}
			).insert().submit()
