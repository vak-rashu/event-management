# Copyright (c) 2025, BWH Studios and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class IntegrationTestEventBooking(IntegrationTestCase):
	"""
	Integration tests for EventBooking.
	Use this class for testing interactions between multiple components.
	"""

	def test_total_calculation(self):
		TEST_ADD_ON_PRICE = 100
		TEST_VIP_TICKET_TYPE_PRICE = 500

		test_category = frappe.get_doc({"doctype": "Event Category", "name": "Test Category"}).insert()
		test_venue = frappe.get_doc(
			{"doctype": "Event Venue", "name": "Test Venue", "address": "test"}
		).insert()
		test_host = frappe.get_doc({"doctype": "Event Host", "name": "Test Host"}).insert()

		test_event = frappe.get_doc(
			{
				"doctype": "FE Event",
				"category": test_category.name,
				"venue": test_venue.name,
				"host": test_host.name,
				"title": "Test Event",
				"start_date": frappe.utils.today(),
			}
		).insert()

		test_ticket_add_on = frappe.get_doc(
			{
				"doctype": "Ticket Add-on",
				"event": test_event.name,
				"title": "T-Shirt",
				"price": TEST_ADD_ON_PRICE,
			}
		).insert()

		test_ticket_type = frappe.get_doc(
			{
				"doctype": "Event Ticket Type",
				"event": test_event.name,
				"title": "VIP",
				"price": TEST_VIP_TICKET_TYPE_PRICE,
			}
		).insert()

		test_booking = frappe.get_doc(
			{
				"doctype": "Event Booking",
				"event": test_event.name,
				"user": "Administrator",
				"attendees": [
					{"ticket_type": test_ticket_type.name, "full_name": "John", "email": "john@email.com"},
					{"ticket_type": test_ticket_type.name, "full_name": "Jenny", "email": "jenny@email.com"},
				],
			}
		).insert()

		# without add ons
		self.assertEqual(test_booking.total_amount, 1000)

		test_attendee_add_on = frappe.get_doc(
			{
				"doctype": "Attendee Ticket Add-on",
				"add_ons": [{"add_on": test_ticket_add_on.name, "value": "XL"}],
			}
		).insert()

		test_booking.attendees[0].add_ons = test_attendee_add_on.name
		test_booking.save()

		# with one add-on
		self.assertEqual(test_booking.attendees[0].number_of_add_ons, 1)
		self.assertEqual(test_booking.attendees[0].add_on_total, TEST_ADD_ON_PRICE)
		self.assertEqual(test_booking.total_amount, 1100)
