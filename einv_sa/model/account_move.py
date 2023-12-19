#!/usr/bin/python
# -*- coding: utf-8 -*-
import base64

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning
from datetime import datetime
import logging
log = logging.getLogger(__name__)

class AccountMove(models.Model):
    _name = "account.move"
    _inherit = "account.move"
    einv_amount_sale_total = fields.Monetary(string="Amount sale total")
    einv_amount_discount_total = fields.Monetary(string="Amount discount total")
    einv_amount_tax_total = fields.Monetary(string="Amount tax total")
    l10n_sa_qr_code_str = fields.Char(string='Zatka QR Code', compute='_compute_qr_code_str')
    l10n_sa_delivery_date = fields.Date(string='Delivery Date', default=fields.Date.context_today, copy=False)
    l10n_sa_confirmation_datetime = fields.Datetime(string='Confirmation Date', readonly=True, copy=False)
    
    def _compute_qr_code_str(self):
        """ Generate the qr code for Saudi e-invoicing. Specs are available at the following link at page 23
        https://zatca.gov.sa/ar/E-Invoicing/SystemsDevelopers/Documents/20210528_ZATCA_Electronic_Invoice_Security_Features_Implementation_Standards_vShared.pdf
        """
        def get_qr_encoding(tag, field):
            company_name_byte_array = field.encode('UTF-8')
            company_name_tag_encoding = tag.to_bytes(length=1, byteorder='big')
            company_name_length_encoding = len(company_name_byte_array).to_bytes(length=1, byteorder='big')
            return company_name_tag_encoding + company_name_length_encoding + company_name_byte_array

        for record in self:
            qr_code_str = ''
            if record.company_id and record.invoice_date: 
                seller_name_enc = get_qr_encoding(1, record.company_id.display_name)
                company_vat_enc = get_qr_encoding(2, record.company_id.vat)
                time_sa = fields.Datetime.context_timestamp(self.with_context(tz='Asia/Riyadh'), datetime(record.invoice_date.year, record.invoice_date.month, record.invoice_date.day))
                timestamp_enc = get_qr_encoding(3, time_sa.isoformat())
                invoice_total_enc = get_qr_encoding(4, str(record.amount_total))
                total_vat_enc = get_qr_encoding(5, str(record.currency_id.round(record.amount_total - record.amount_untaxed)))

                str_to_encode = seller_name_enc + company_vat_enc + timestamp_enc + invoice_total_enc + total_vat_enc
                qr_code_str = base64.b64encode(str_to_encode).decode('UTF-8')
            record.l10n_sa_qr_code_str = qr_code_str
            
    def write(self, vals):
        res = super().write(vals)
        for r in self:
            if r.journal_id.type == 'sale':
                einv_amount_sale_total = r.amount_untaxed + sum(line.einv_amount_discount for line in r.invoice_line_ids)
                einv_amount_discount_total = sum(line.einv_amount_discount for line in r.invoice_line_ids)
                einv_amount_tax_total = sum(line.einv_amount_tax for line in r.invoice_line_ids)
                super().write({'einv_amount_tax_total':einv_amount_tax_total,'einv_amount_discount_total':einv_amount_discount_total,'einv_amount_sale_total':einv_amount_sale_total})
        return res

    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        for r in res:
            if r.journal_id.type == 'sale':
                r.einv_amount_sale_total = r.amount_untaxed + sum(line.einv_amount_discount for line in r.invoice_line_ids)
                r.einv_amount_discount_total = sum(line.einv_amount_discount for line in r.invoice_line_ids)
                r.einv_amount_tax_total = sum(line.einv_amount_tax for line in r.invoice_line_ids)
        return res
    
    def _compute_amount(self):
        res = super(AccountMove, self)._compute_amount()

        # do the things here
        return res




class AccountMoveLine(models.Model):
    _name = "account.move.line"
    _inherit = "account.move.line"
    einv_amount_discount = fields.Monetary(string="Amount discount")
    einv_amount_tax = fields.Monetary(string="Amount tax")
    
    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for r in res:
            if r.move_id.journal_id.type == 'sale':
                r.einv_amount_discount = r.quantity * r.price_unit * (r.discount / 100)
                r.einv_amount_tax = sum(r.price_subtotal * (tax.amount / 100) for tax in r.tax_ids)
        return res
            
    def write(self, vals):
        res = super().write(vals)
        for r in self:
            if r.move_id.journal_id.type == 'sale':
                einv_amount_discount = r.quantity * r.price_unit * (r.discount / 100)
                einv_amount_tax = sum(r.price_subtotal * (tax.amount / 100) for tax in r.tax_ids)
                super().write({'einv_amount_discount':einv_amount_discount,'einv_amount_tax':einv_amount_tax})
        return res
            
