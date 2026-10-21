import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class LibraryTransaction(Document):
	def before_submit(self):
		if self.type == "Issue":
			self.validate_membership()
			self.validate_article_is_available()
			self.validate_issue_limit()
			self.set_article_status("Issued")
		elif self.type == "Return":
			self.validate_article_is_issued()
			self.set_article_status("Available")

	def validate_membership(self):
	
		valid_membership = frappe.db.exists(
			"Library Membership",
			{
				"library_member": self.library_member,
				"docstatus": DocStatus.submitted(),
				"from_date": ("<=", self.date),
				"to_date": (">=", self.date),
			},
		)
		if not valid_membership:
			frappe.throw("The member does not have a valid membership")

	def validate_article_is_available(self):
		status = frappe.db.get_value("Article", self.article, "status")
		if status == "Issued":
			frappe.throw("This article is already issued")

	def validate_article_is_issued(self):
		status = frappe.db.get_value("Article", self.article, "status")
		if status == "Available":
			frappe.throw("This article was not issued, so it cannot be returned")

	def set_article_status(self, status):
		article = frappe.get_doc("Article", self.article)
		article.status = status
		article.save()
	
	def validate_issue_limit(self):
		limit = frappe.db.get_single_value("Library Settings", "max_articles") or 0
		if not limit:
			return 

		filters = {"library_member": self.library_member, "docstatus": DocStatus.submitted()}
		issued = frappe.db.count("Library Transaction", {**filters, "type": "Issue"})
		returned = frappe.db.count("Library Transaction", {**filters, "type": "Return"})

		if issued - returned >= limit:
			frappe.throw("This member has reached the maximum number of issued articles")