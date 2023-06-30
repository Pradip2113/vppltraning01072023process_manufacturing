frappe.query_reports["Process Order Summary"] = {
	"filters": [
        {
			label: __("Name"),
			fieldname: "name",
			fieldtype: "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Process Order', txt);
			}
		}
    ]}