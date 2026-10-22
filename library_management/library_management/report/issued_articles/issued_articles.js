// Copyright (c) 2026, me and contributors
// For license information, please see license.txt

frappe.query_reports["Issued Articles"] = {
    filters: [
        {
            fieldname: "category",
            label: __("Category"),
            fieldtype: "Data",
        },
    ],
};