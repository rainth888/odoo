
from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    default_metal_type = fields.Selection([
        ('au_9999','Au 999.9'), ('au_999','Au 999'), ('au_au18k','Au 18K'), ('au_au14k','Au 14K')
    ], string="默认金种")
    default_wage_type = fields.Selection([('per_g','克工费'), ('per_piece','件工费')], default='per_piece')
