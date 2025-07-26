# Copyright (c) 2025, BWH Studios and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EventTicket(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from events.ticketing.doctype.ticket_add_on_value.ticket_add_on_value import TicketAddonValue

		add_ons: DF.Table[TicketAddonValue]
		amended_from: DF.Link | None
		attendee_name: DF.Data
		booking: DF.Link | None
		event: DF.Link
		qr_code: DF.AttachImage | None
		ticket_type: DF.Link
	# end: auto-generated types

	def before_submit(self):
		self.generate_qr_code()

	def generate_qr_code(self):
		import io

		import qrcode

		img = qrcode.make(f"{self.name}")
		output = io.BytesIO()
		img.save(output, format="PNG")
		hex_data = output.getvalue()

		qr_code_file = frappe.get_doc(
			{
				"doctype": "File",
				"content": hex_data,
				"attached_to_doctype": "Event Ticket",
				"attached_to_name": self.name,
				"attached_to_field": "qr_code",
				"file_name": f"ticket-qr-code-{self.name}.png",
			}
		).save()

		self.qr_code = qr_code_file.file_url
