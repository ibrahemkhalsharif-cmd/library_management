# Copyright (c) 2026, me and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class LibraryMember(Document):
	def before_save(self):
		self.full_name = f"{self.first_name} {self.last_name or ''} "
	def validate(self):
		if self.mobile:
			if len(self.mobile) != 10:
				frappe.throw("Mobile number must be 10 digits long.")
			if not self.mobile.isdigit():
				frappe.throw("Mobile number must contain only digits.")
			if not self.mobile.startswith("05"):
				frappe.throw("Mobile number must start with 05.")
