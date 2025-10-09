
from odoo import models, fields, api


class MetalType(models.Model):
    _name = "metal.type"
    _description = "Metal Type Configuration"
    _order = "sequence, name"

    name = fields.Char("Name", required=True, translate=True, help="显示名称，如：Au 999.9")
    code = fields.Char("Code", required=True, help="唯一代码，如：au_9999")
    fineness_factor = fields.Float(
        "Default Fineness Factor", 
        default=1.0, 
        help="默认成色系数，如 18K ~ 0.75。可在每日金价中覆盖"
    )
    sequence = fields.Integer("Sequence", default=10)
    active = fields.Boolean("Active", default=True)
    description = fields.Text("Description")

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Metal type code must be unique!')
    ]

    def name_get(self):
        """Display name with code"""
        result = []
        for record in self:
            name = f"{record.name} ({record.code})" if record.code else record.name
            result.append((record.id, name))
        return result

