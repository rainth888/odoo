from odoo import fields, models


class PosMetalType(models.Model):
    """Configurable metal types used by POS gold pricing."""

    _name = "pos.metal.type"
    _description = "POS Metal Type"
    _order = "sequence, name"

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company,
        help="Restrict the metal type to a specific company if needed.",
    )
    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            "pos_metal_type_unique_code_company",
            "unique(code, company_id)",
            "The metal type code must be unique per company.",
        )
    ]
