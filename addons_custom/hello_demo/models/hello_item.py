# -*- coding: utf-8 -*-
from odoo import api, fields, models

class HelloItem(models.Model):
    _name = "hello.item"
    _description = "Hello Item"

    name = fields.Char("名称", required=True)
    code = fields.Char("编码", index=True)
    active = fields.Boolean("启用", default=True)
    note = fields.Text("备注")
    # 计算字段示例
    name_display = fields.Char("显示名", compute="_compute_name_display", store=False)

    @api.depends("name", "code")
    def _compute_name_display(self):
        for rec in self:
            rec.name_display = f"[{rec.code}] {rec.name}" if rec.code else rec.name