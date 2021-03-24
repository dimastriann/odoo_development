# -*- coding: utf-8 -*-

import time
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    @api.model
    def get_stock_dashboard_data(self):
        # server_date = time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        # domains = {
        #     # 'count_picking_draft': "sp.state = 'draft'",
        #     'count_picking_waiting': "sp.state in ('confirmed', 'waiting')",
        #     'count_picking_ready': "sp.state = 'assigned'",
        #     # 'count_picking': "sp.state in ('assigned', 'waiting', 'confirmed')",
        #     'count_picking_late': "sp.scheduled_date < '%s' AND sp.state in ('assigned', 'waiting', 'confirmed')" % server_date,
        #     'count_picking_backorders': "sp.backorder_id NOTNULL AND sp.state in ('confirmed', 'assigned', 'waiting')",
        # }
        #
        # results = []
        # for pick_code in ['incoming', 'internal', 'outgoing']:
        #     query = """SELECT count(sp.id) as picking_count FROM stock_picking sp
        #                 LEFT JOIN stock_picking_type spt on spt.id = sp.picking_type_id"""
        #     query_reset = query
        #     receipts, internal, delivery = [], [], []
        #     for key, value in domains.items():
        #         if pick_code == 'incoming':
        #             query_reset += " WHERE " + value + " AND spt.code = 'incoming'"
        #             self._cr.execute(query_reset)
        #             receipts.append({key + "_in":self._cr.dictfetchall()[0].get('picking_count')})
        #             query_reset = query
        #         elif pick_code == 'internal':
        #             query_reset += " WHERE " + value + " AND spt.code = 'internal'"
        #             self._cr.execute(query_reset)
        #             internal.append({key + "_int":self._cr.dictfetchall()[0].get('picking_count')})
        #             query_reset = query
        #         elif pick_code == 'outgoing':
        #             query_reset += " WHERE " + value + " AND spt.code = 'outgoing'"
        #             self._cr.execute(query_reset)
        #             delivery.append({key + "_out":self._cr.dictfetchall()[0].get('picking_count')})
        #             query_reset = query
        #     if pick_code == 'incoming':
        #         results.append(receipts)
        #     if pick_code == 'internal':
        #         results.append(internal)
        #     if pick_code == 'outgoing':
        #         results.append(delivery)

        receipts = {
            'name': 'All Receipts',
            'data': {'ready': 5, 'waiting': 5,
                     'context': '{"search_default_picking_type_code": "incoming", "search_default_available": True}'},
            'context': '{"search_default_picking_type_code": "incoming"}',
        }
        internal = {
            'name': 'All Internal',
            'data': {'ready': 6, 'waiting': 6,
                     'context': '{"search_default_picking_type_code": "internal", "search_default_available": True}'},
            'context': '{"search_default_picking_type_code": "internal"}',
        }
        delivery = {
            'name': 'All Delivery',
            'data': {'ready': 7, 'waiting': 7,
                     'context': '{"search_default_picking_type_code": "incoming", "search_default_available": True}'},
            'context': '{"search_default_picking_type_code": "outgoing"}',
        }
        results = {
            'incoming': receipts,
            'internal': internal,
            'outgoing': delivery,
        }
        # results = [receipts, internal, delivery]
        return results
