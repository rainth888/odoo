from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    pos_pricing_method = fields.Selection([
        ("by_unit", "By Unit"),
        ("by_weight", "By Weight"),
    ], string="Pricing Method", default="by_unit",
        help=(
            "Choose how this product is priced in POS:\n"
            "- By Unit: uses Sales Price per Unit.\n"
            "- By Weight: uses product Weight (g) multiplied by gold price (provided by pos_gold_pricing)."
        ))

    # Helper field to edit weight in grams while Odoo stores kilograms
    weight_g = fields.Float(
        string="Weight (g)",
        compute="_compute_weight_g",
        inverse="_inverse_weight_g",
        store=False,
    )

    @api.depends("weight")
    def _compute_weight_g(self):
        for rec in self:
            rec.weight_g = (rec.weight or 0.0) * 1000.0

    def _inverse_weight_g(self):
        for rec in self:
            rec.weight = (rec.weight_g or 0.0) / 1000.0

    @api.onchange("pos_pricing_method")
    def _onchange_pos_pricing_method_set_uom(self):
        """Force Unit of Measure based on pricing method.

        - by_unit  -> Unit(s)
        - by_weight -> Gram (g)
        Also keeps purchase UoM in sync.
        """
        unit = self.env.ref("uom.product_uom_unit", raise_if_not_found=False)
        gram = self.env.ref("uom.product_uom_gram", raise_if_not_found=False)
        # Fallbacks if some UoMs are missing
        if gram is None:
            gram = self.env.ref("uom.product_uom_kgm", raise_if_not_found=False)

        for rec in self:
            if rec.pos_pricing_method == "by_unit" and unit:
                rec.uom_id = unit
                rec.uom_po_id = unit
            elif rec.pos_pricing_method == "by_weight" and gram:
                rec.uom_id = gram
                rec.uom_po_id = gram
