from odoo import models, fields, api, _


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = "account.move"
    
    x_delivery_note_no = fields.Char(string="Delivery Note", required=False, )

    

class AccountMoveLine(models.Model):
    _name = "account.move.line"
    _inherit = "account.move.line"
    
    price_per_unit = fields.Float(string="Price Per Unit", required=False, )
    total_wieght = fields.Float(string="Total Weight", compute='_compute_weight' )

    def _compute_weight(self):
        for line in self:
            line.total_wieght = line.product_uom_id.x_kgexch * line.quantity

    @api.onchange('price_per_unit', 'product_uom_id')
    def onchange_price_per_unit(self):
        for rec in self:
            if rec.product_uom_id:
                rec.price_unit = rec.price_per_unit * rec.product_uom_id.x_kgexch
            else:
                rec.price_unit = rec.price_per_unit
    
class SaleOrderPo(models.Model):
    _inherit = 'sale.order'

    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        delivery_obj = self.env['stock.picking'].search([('origin', '=', self.name)], limit=1)
        res["x_delivery_note_no"] = delivery_obj.name
        return res
    
    

class SaleOrderPerUnit(models.Model):
    _inherit = 'sale.order.line'

    price_per_unit = fields.Float(string="Price Per Unit", required=False, )
    total_wieght = fields.Float(string="Total Weight", compute='_compute_amount')

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'price_per_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            if line.price_per_unit:
                line.price_unit = line.price_per_unit * line.product_uom.x_kgexch
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
                'total_wieght': line.product_uom.x_kgexch * line.product_uom_qty,
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups(
                    'account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])

    def _prepare_invoice_line(self, **optional_values):
        
        res = super()._prepare_invoice_line(**optional_values)
        res['price_per_unit'] = self.price_per_unit
        res['total_wieght'] = self.total_wieght

        return res