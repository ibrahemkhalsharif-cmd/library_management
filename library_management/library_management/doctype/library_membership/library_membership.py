import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus
from frappe.utils import add_days


class LibraryMembership(Document):
	def before_submit(self):
		self.ensure_no_overlap()
		self.apply_loan_period()

	def ensure_no_overlap(self):
		exists = frappe.db.exists(
			"Library Membership",
			{
				"library_member": self.library_member,
				"docstatus": DocStatus.submitted(),
				"to_date": (">", self.from_date),
			},
		)
		if exists:
			frappe.throw("There is an active membership for this member")

	def apply_loan_period(self):
		loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
		self.to_date = add_days(self.from_date, loan_period or 30)