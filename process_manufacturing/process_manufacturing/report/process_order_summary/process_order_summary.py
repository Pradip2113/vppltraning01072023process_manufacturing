from collections import defaultdict

import frappe
from frappe import _
from frappe.utils import date_diff, flt, getdate, today

from erpnext.stock.report.stock_analytics.stock_analytics import get_period, get_period_date_ranges

def execute(filters=None):
	data = []

	if not filters.get("age"):
		filters["age"] = 0

	data = get_data(filters)
	return data

def get_data(filters):
	query_filters = {"docstatus": ("<", 1)}


	for field in ["name"]:
		if filters.get(field):
			query_filters[field] = ("in", filters.get(field))