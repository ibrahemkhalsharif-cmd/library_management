# Copyright (c) 2026, me and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibraryMembership(Document):
	def before_submit(self):
		exists = frappe.db.exists(
			"Library Membership",
			{
				'library_member': self.library_member,
				'docstatus' : DocStatus.submitted(),
				'to_date': ('>', self.from_date),
			}
		)
		if exists:
			frappe.throw("A membership for this member already exists for the given date range.")
