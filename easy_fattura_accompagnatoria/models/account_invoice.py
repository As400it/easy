# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2017 Dinamiche Aziendali srl
#    @author Gianmarco Conte <gconte@dinamicheaziendali.it>
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import fields, models, api


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
    accompagnatoria = fields.Boolean(string='Fattura Accompagnatoria',
                                     readonly=True, copy=False)

    @api.depends('picking_ids.state')
    def compute_delviery_invoice(self):
        model_stock_picking = self.env['stock.picking']
        for x in self:
            picking_list = model_stock_picking.search(
                [('invoice_id', '=', x.id)])
            for picking in picking_list:
                x.delivery_invoice = True
                if picking.state != 'done' or picking.ddt_number != False:
                    x.delivery_invoice = False
                    break
            return True

    @api.multi
    def compute_journal_accomp(self):
        if not self.env['account.journal'].search(
                [('name', 'like', 'Accomp')],
                limit=1):
            return self.env['account.journal'].search(
                [('name', 'like', 'Clienti')],
                limit=1)
        else:
            return self.env['account.journal'].search(
                [('name', 'like', 'Accomp')],
                limit=1)

    @api.multi
    def print_delivery_invoice(self):
        self.ensure_one()
        model_invoice = self.env['account.invoice']
        self.accompagnatoria = True
        self.journal_id = self.compute_journal_accomp()
        self.action_invoice_open()
        return self.invoice_print()

    # @api.multi
    # def print_delivery_invoice(self):
    #     self.ensure_one()
    #     model_invoice = self.env['account.invoice']
    #     self.accompagnatoria = True
    #     self.journal_id = self.compute_journal_accomp()
    #     self.action_invoice_open()
    #     datas = {
    #         'model': model_invoice._name,
    #         'form': model_invoice.read(),
    #         'context': self._context
    #     }
    #     return {
    #         'type': 'ir.actions.report.xml',
    #         # 'report_name': 'easy_fattura_accompagnatoria.fattura_accompagnatoria_template',
    #         'report_name': 'account.report_invoice',
    #         'datas': datas
    #     }




    @api.multi
    def ddt_time_report(self, time_ddt):
        hh = int(time_ddt)
        mm = time_ddt - hh
        mms = str(int(round(mm * 60)))
        if (len(mms) == 1):
            mms = '0' + mms
        data = str(hh) + ":" + mms
        return data
