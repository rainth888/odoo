
from odoo import models, fields, api

class MetalPricelist(models.Model):
    _name = "metal.pricelist"
    _description = "Metal daily price for jewelry"

    name = fields.Char("Name", required=True)
    metal_type = fields.Selection([
        ('au_9999', 'Au 999.9'),
        ('au_999',  'Au 999'),
        ('au_au18k','Au 18K'),
        ('au_au14k','Au 14K'),
    ], required=True, help="金种/成色")
    price_per_g = fields.Float("Price (CNY/gram)", digits=(16, 4), required=True)
    fineness_factor = fields.Float("Fineness Factor", default=1.0, help="成色系数，如 18K ~ 0.75")
    effective_date = fields.Date("Effective Date", required=True)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, required=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('uniq_day_metal_company', 'unique(metal_type, effective_date, company_id)',
         '同一天、同一金种、同一公司只能有一条当日金价。')
    ]

    @api.model
    def get_price(self, company_id, metal_type, on_date=None):
        """Return (price_per_g, fineness_factor) for the given day/metal/company."""
        on_date = on_date or fields.Date.context_today(self)
        rec = self.search([
            ('company_id', '=', company_id),
            ('metal_type', '=', metal_type),
            ('effective_date', '<=', on_date),
            ('active', '=', True),
        ], order="effective_date desc", limit=1)
        return rec and (rec.price_per_g, rec.fineness_factor) or (0.0, 1.0)
