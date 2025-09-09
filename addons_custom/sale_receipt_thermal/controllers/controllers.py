# -*- coding: utf-8 -*-
# from odoo import http


# class SaleReceiptThermal(http.Controller):
#     @http.route('/sale_receipt_thermal/sale_receipt_thermal', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_receipt_thermal/sale_receipt_thermal/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_receipt_thermal.listing', {
#             'root': '/sale_receipt_thermal/sale_receipt_thermal',
#             'objects': http.request.env['sale_receipt_thermal.sale_receipt_thermal'].search([]),
#         })

#     @http.route('/sale_receipt_thermal/sale_receipt_thermal/objects/<model("sale_receipt_thermal.sale_receipt_thermal"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_receipt_thermal.object', {
#             'object': obj
#         })

