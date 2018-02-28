# -*- coding: utf-8 -*-
# © 2013-15 Agile Business Group sagl (<http://www.agilebg.com>)
# © 2015-2016 AvanzOSC
# © 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class StockPickingInh(models.Model):
    _inherit = "stock.picking"

    invoice_id = fields.Many2one(
        comodel_name='account.invoice', string='Invoice',
        compute="_compute_invoice_id", store=True)
