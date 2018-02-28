# -*- coding: utf-8 -*-
# Copyright 2017 Lorenzo Battistini - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from openerp import fields, models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    # we need this to be able to call l10n_it_ddt.delivery_data
    note = fields.Text(
        'Additional Information', readonly=True, related="comment")
    carrier_id = fields.Many2one('res.partner', string='Carrier')
    carrier_tracking_ref = fields.Char('Carrier Tracking Ref')
    weight_net = fields.Float(string="Net Weight")
    weight = fields.Float(string="Weight")
    volume = fields.Float('Volume')
    # date_done = fields.Date(string='Date')
    date_transport_ddt = fields.Date(string='Date')
    time_transport_ddt = fields.Float()
    ddt_notes = fields.Text(string='Delivery Note Notes')
    delivery_invoice = fields.Boolean(compute='compute_delviery_invoice')

    @api.depends('picking_ids.state')
    # @api.depends('picking_ids')
    def compute_delviery_invoice(self):
        model_stock_picking = self.env['stock.picking']
        picking_list = model_stock_picking.search(
            [('invoice_id', '=', self.id)])
        for picking in picking_list:
            self.delivery_invoice = True
            if picking.state != 'done' or picking.ddt_number != False:
                self.delivery_invoice = False
                break


    @api.multi
    def print_delivery_invoice(self):
        self.ensure_one()
        model_invoice = self.env['account.invoice']
        datas = {
            'model': model_invoice._name,
            'form': model_invoice.read(),
            'context': self._context
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'easy_fattura_accompagnatoria.fattura_accompagnatoria_template',
            'datas': datas
        }

    @api.multi
    def ddt_time_report(self, time_ddt):
        hh = int(time_ddt)
        mm = time_ddt - hh
        mms = str(int(round(mm * 60)))
        if (len(mms) == 1):
            mms = '0' + mms
        data = str(hh) + ":" + mms
        return data
