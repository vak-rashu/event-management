# Copyright (c) 2025, BWH Studios and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EventTicketType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		auto_unpublish_on: DF.Date | None
		currency: DF.Link
		event: DF.Link
		is_published: DF.Check
		max_tickets_available: DF.Int
		name: DF.Int | None
		price: DF.Currency
		title: DF.Data
	# end: auto-generated types

	pass
