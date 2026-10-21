frappe.ui.form.on('Library Transaction', {
    article(frm) {
        if (!frm.doc.article) return;
        frappe.db.get_value("Article", frm.doc.article, "status").then((r) => {
            const status = r.message.status;
            frappe.show_alert({
                message: `${frm.doc.article} is ${status}`,
                indicator: status === "Available" ? "green" : "red"
            });
        });
    }
});