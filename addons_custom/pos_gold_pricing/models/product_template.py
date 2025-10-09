
from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    default_metal_type_id = fields.Many2one(
        "pos.metal.type",
        string="默认金种",
        help="选择默认的金种，以便在 POS 中自动选取当日金价。",
    )
    default_wage_type = fields.Selection([('per_g','克工费'), ('per_piece','件工费')], default='per_piece')
