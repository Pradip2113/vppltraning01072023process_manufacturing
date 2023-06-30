# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt
# Created by : Abhishek Chougule - Dev.MrAbhi

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import math
from erpnext.stock.get_item_details import get_conversion_factor, get_price_list_rate
from frappe.utils import flt

class ProcessDefinition(Document):
   
	@frappe.whitelist()
	def qtyupdate(self):
		mqty=0.0
		fpq=0.0
		scq=0.0
		tocq=0.0
		mam=0.0
		fpam=0.0
		scam=0.0
		tbam=0.0
		
		for m in self.get('materials'):
   
			#UOM Conversion	
			# itmlst=frappe.db.get_list("Item")
			# for b in itmlst:
			# 	itm = frappe.get_doc("Item", b.name)
			# 	for i in itm.get('uoms'):
			# 		if m.item==b.name and i.uom=="TON":
			# 			temp=(float(m.quantity)/i.conversion_factor)
			# 			break
			# mqty=float(mqty)+float(temp)

			m.conversion_factor = flt(get_conversion_factor(m.item, m.uom)["conversion_factor"])
			if m.uom and m.quantity:
				m.stock_qty = flt(m.conversion_factor) * flt(m.quantity)
			if not m.uom and m.stock_uom:
				m.uom = m.stock_uom
				m.quantity = m.stock_qty
			
			mqty=mqty+flt(m.quantity)
			tbam=flt(m.quantity)*flt(m.rate)
			m.amount=tbam
			mam=mam+m.amount
				
		self.materials_qty=mqty
		self.materials_amount=mam
   
   
   
		for fp in self.get('finished_products'):
   
			fp.conversion_factor = flt(get_conversion_factor(fp.item, fp.uom)["conversion_factor"])
			if fp.uom and fp.quantity:
				fp.stock_qty = flt(fp.conversion_factor) * flt(fp.quantity)
			if not fp.uom and fp.stock_uom:
				fp.uom = fp.stock_uom
				fp.quantity = fp.stock_qty
   
			fpq=fpq+flt(fp.quantity)
			tbam=flt(fp.quantity)*flt(fp.rate)
			fp.amount=tbam
			fpam=fpam+fp.amount
   
			
		self.finished_products_qty=fpq	
		self.finished_products_amount=fpam #math.ceil(fpam)
		
		for sc in self.get('scrap'):
   
			sc.conversion_factor = flt(get_conversion_factor(sc.item, sc.uom)["conversion_factor"])
			if sc.uom and sc.quantity:
				sc.stock_qty = flt(sc.conversion_factor) * flt(sc.quantity)
			if not sc.uom and sc.stock_uom:
				sc.uom = sc.stock_uom
				sc.quantity = sc.stock_qty
   
			scq=scq+flt(sc.quantity)
			tbam=flt(sc.quantity)*flt(sc.rate)
			sc.amount=tbam
			scam=scam+sc.amount

			
			
		self.scrap_qty=scq
		self.scrap_amount=scam
  
		self.all_finish_qty=self.finished_products_qty+self.scrap_qty
		self.total_all_amount=(self.finished_products_amount+self.scrap_amount)-flt(self.total_operation_cost)#(self.finished_products_amount+float(self.total_operation_cost))-self.scrap_amount
		
		for toc in self.get('operation_cost'):
			tocq=tocq+flt(toc.amount)
			
		self.total_operation_cost=tocq
		self.diff_qty=self.all_finish_qty-self.materials_qty
		self.diff_amt=(self.materials_amount+self.total_operation_cost)-flt(self.total_all_amount)

@frappe.whitelist()
def Get_Purchase_Rate(item):
	query = """select  valuation_rate from `tabStock Ledger Entry` where item_code = %(items)s order by creation LIMIT 1"""
	data = frappe.db.sql(query, {"items": item},as_dict=1)
	return data

