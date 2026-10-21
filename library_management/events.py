import frappe


def create_return_todo(doc, method=None):
    if doc.type != "Issue":
        return

    frappe.get_doc({
        "doctype": "ToDo",
        "description": f"Return {doc.article} by {doc.date}",
        "date": doc.date,
        "allocated_to": frappe.session.user,
        "reference_type": doc.doctype,
        "reference_name": doc.name,
    }).insert(ignore_permissions=True)