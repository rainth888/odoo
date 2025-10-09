
from odoo import models, fields, api


class MetalPricelist(models.Model):
    _name = "metal.pricelist"
    _description = "Metal daily price for jewelry"

    name = fields.Char("Name", required=True)
    metal_type_id = fields.Many2one(
        "metal.type", 
        string="Metal Type", 
        required=True, 
        help="金种/成色"
    )
    price_per_g = fields.Float("Price (CNY/gram)", digits=(16, 4), required=True)
    fineness_factor = fields.Float(
        "Fineness Factor", 
        compute="_compute_fineness_factor",
        store=True,
        readonly=False,
        help="成色系数，如 18K ~ 0.75。默认从金属类型继承"
    )
    effective_date = fields.Date("Effective Date", required=True)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, required=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('uniq_day_metal_company', 'unique(metal_type_id, effective_date, company_id)',
         '同一天、同一金种、同一公司只能有一条当日金价。')
    ]

    @api.depends('metal_type_id')
    def _compute_fineness_factor(self):
        """继承金属类型的默认成色系数"""
        for record in self:
            if record.metal_type_id and not record.fineness_factor:
                record.fineness_factor = record.metal_type_id.fineness_factor or 1.0

    @api.model
    def get_price(self, company_id, metal_type_code, on_date=None):
        """Return (price_per_g, fineness_factor) for the given day/metal/company.
        
        Args:
            company_id: Company ID
            metal_type_code: Metal type code (string) or metal.type ID (int)
            on_date: Effective date (defaults to today)
        """
        on_date = on_date or fields.Date.context_today(self)
        
        # 支持传入 code 或 ID
        if isinstance(metal_type_code, str):
            metal_type = self.env['metal.type'].search([('code', '=', metal_type_code)], limit=1)
            if not metal_type:
                return (0.0, 1.0)
            metal_type_id = metal_type.id
        else:
            metal_type_id = metal_type_code
            
        rec = self.search([
            ('company_id', '=', company_id),
            ('metal_type_id', '=', metal_type_id),
            ('effective_date', '<=', on_date),
            ('active', '=', True),
        ], order="effective_date desc", limit=1)
        return rec and (rec.price_per_g, rec.fineness_factor) or (0.0, 1.0)
