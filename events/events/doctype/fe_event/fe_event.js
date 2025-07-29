// Copyright (c) 2025, BWH Studios and contributors
// For license information, please see license.txt

frappe.ui.form.on("FE Event", {
	refresh(frm) {
		frappe.call("frappe.geo.country_info.get_country_timezone_info").then(({ message }) => {
			frm.fields_dict.time_zone.set_data(message.all_timezones);
		});

		const button_label = frm.doc.is_published ? __("Unpublish") : __("Publish");
		frm.add_custom_button(button_label, () => {
			frm.set_value("is_published", !frm.doc.is_published);
			frm.save();
		});
	},
});
