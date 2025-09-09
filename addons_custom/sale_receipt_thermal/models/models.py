# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class sale_receipt_thermal(models.Model):
#     _name = 'sale_receipt_thermal.sale_receipt_thermal'
#     _description = 'sale_receipt_thermal.sale_receipt_thermal'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

