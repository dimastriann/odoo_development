# -*- coding: utf-8 -*-

import time
import json

from odoo import models, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    # @api.model
    def get_stock_dashboard_data(self):
        domains = {
            # 'draft': [('state', '=', 'draft')],
            'waiting': [('state', 'in', ('confirmed', 'waiting'))],
            'ready': [('state', '=', 'assigned')],
            'late': [('scheduled_date', '<', time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)),
                     ('state', 'in', ('assigned', 'waiting', 'confirmed'))],
            'backorder': [('backorder_id', '!=', False), ('state', 'in', ('confirmed', 'assigned', 'waiting'))],
        }

        context = {
            'search_default_picking_type_code': '%s',
            'search_default_%s': True,
            'search_default_group_by_picking_type': True
        }

        stock_data = []
        for operation in sorted(set(self.mapped('code'))):
            op_type = "Receipts" if operation == 'incoming' else ("Delivery" if operation == 'outgoing' else operation)
            results = {}
            for field in domains:
                data = self.env['stock.picking'].search_read(
                    domains[field] + [('state', 'not in', ('done', 'cancel')), ('picking_type_id', 'in', self.ids),
                                      ('picking_type_code', '=', operation)], ['picking_type_code'])
                state = "available" if field == 'ready' else field
                res_data = {
                    'val': len(data),
                    'domain': json.dumps([d.get('id') for d in data]),
                    'context': str(context) % (operation, state),
                    'name': "All %s %s" % (op_type.capitalize(), field.capitalize())
                }
                results.update({field: res_data})
            results.update({
                'name': 'All %s' % op_type.capitalize(),
                'context': str({"search_default_picking_type_code": operation})
            })
            stock_data.append(results)

        return stock_data
        # return self.test_data_stock()

    # stock data test #
    def test_data_stock(self):
        receipts = {
            'name': 'All Receipts',
            'context': '{"search_default_picking_type_code": "incoming"}',
            'ready': {
                'val': 5, 'name': 'All Receipts Ready', 'domain': json.dumps([]),
                'context': '{"search_default_picking_type_code": "incoming", "search_default_available": True}'
            },
            'waiting': {
                'val': 5, 'name': 'All Receipts Waiting', 'domain': json.dumps([]),
                'context': '{"search_default_picking_type_code": "incoming", "search_default_waiting": True}'
            },
            'late': {
                'val': 5, 'name': 'All Receipts Late', 'domain': json.dumps([]),
                'context': '{"search_default_picking_type_code": "incoming", "search_default_late": True}'
            },
            'backorder': {
                'val': 5, 'name': 'All Receipts Backorders', 'domain': json.dumps([]),
                'context': '{"search_default_picking_type_code": "incoming", "search_default_backorder": True}'
            },
        }

        internal = {
            'name': 'All Internal Transfer',
            'context': '{"search_default_picking_type_code": "internal"}',
            'ready': {
                'val': 5, 'name': 'All Internal Ready', 'domain': json.dumps([]),
                'context': '{"search_default_picking_type_code": "internal", "search_default_available": True}'
            },
            'waiting': {
                'val': 5, 'name': 'All Internal Waiting', 'domain': json.dumps([]),
                'context': '{"search_default_picking_type_code": "internal", "search_default_waiting": True}'
            },
            'late': {
                'val': 5, 'name': 'All Internal Late', 'domain': json.dumps([]),
                'context': '{"search_default_picking_type_code": "internal", "search_default_late": True}'
            },
            'backorder': {
                'val': 5, 'name': 'All Internal Backorders', 'domain': json.dumps([]),
                'context': '{"search_default_picking_type_code": "internal", "search_default_backorder": True}'
            },
        }
        delivery = {
            'name': 'All Delivery',
            'context': '{"search_default_picking_type_code": "outgoing"}',
            'ready': {
                'val': 5, 'name': 'All Delivery Ready', 'domain': json.dumps([]),
                'context': '{"search_default_picking_type_code": "outgoing", "search_default_available": True}'
            },
            'waiting': {
                'val': 5, 'name': 'All Delivery Waiting', 'domain': json.dumps([]),
                'context': '{"search_default_picking_type_code": "outgoing", "search_default_waiting": True}'
            },
            'late': {
                'val': 5, 'name': 'All Delivery Late', 'domain': json.dumps([]),
                'context': '{"search_default_picking_type_code": "outgoing", "search_default_late": True}'
            },
            'backorder': {
                'val': 5, 'name': 'All Delivery Backorders', 'domain': json.dumps([]),
                'context': '{"search_default_picking_type_code": "outgoing", "search_default_backorder": True}'
            },
        }
        return receipts, internal, delivery
