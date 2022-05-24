# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError


class NewModule(models.Model):
    _inherit = 'stock.move'

    sales_qty = fields.Float(string="", required=False, compute='_compute_qty_uom')
    sales_uom_id = fields.Many2one(comodel_name="uom.uom", string="", compute='_compute_qty_uom')

    @api.depends('origin')
    def _compute_qty_uom(self):
        for rec in self:
            sale_obj = self.env['sale.order.line'].search(
                [('order_id.name', '=', rec.origin), ('product_id', '=', rec.product_id.id)],
                limit=1)
            if sale_obj:
                rec.sales_qty = sale_obj.product_uom_qty
                rec.sales_uom_id = sale_obj.product_uom.id
            else:
                rec.sales_qty = False
                rec.sales_uom_id = False

class PickingCustomer(models.Model):
    _inherit = 'stock.picking'

    x_customer_po = fields.Text(string="Customer P.O", required=False, )

    @api.constrains('origin')
    def _check_x_customer_po(self):
        for rec in self:
            sale_obj = self.env['sale.order'].search([('name', '=', rec.origin)],limit=1)
            if sale_obj:
                rec.x_customer_po = sale_obj.x_customer_po
            else:
                rec.x_customer_po = False

