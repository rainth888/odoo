
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    default_metal_type_id = fields.Many2one(
        "metal.type",
        string="默认金种",
        help="产品模板的默认金属类型"
    )
    default_wage_type = fields.Selection([('per_g','克工费'), ('per_piece','件工费')], default='per_piece')
