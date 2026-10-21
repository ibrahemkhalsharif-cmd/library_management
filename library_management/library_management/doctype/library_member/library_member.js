frappe.ui.form.on('Library Member', {
 refresh: function(frm) {
    frm.add_custom_button('Create Membership'), ()=>{
        frappe.new_doc("Library Membership" , {
        library_member: frm.doc.name
    })
    }
    frm.add_custom_button("Create Transaction", () =>{
        frappe.new_doc("Library Transaction", {
            library_member: frm.doc.name
        })
    })
    frappe.call({
        method: "library_management.library_management.doctype.library_member.library_member.get_membership_end_date",
        args: {member: frm.doc.name},

    }).then((r) => {
        if(r.message){
            frm.set_intro(
                `Membership valid until $(frappe.datetime.str_to_user(r.message))`,
                "green"
            )
        }
        else{
            frm.set_intro("No active membership", "red")
        }
    })
    


 }
});
