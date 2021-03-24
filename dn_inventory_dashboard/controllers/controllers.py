# -*- coding: utf-8 -*-
# from odoo import http


# class DnInventoryDashboard(http.Controller):
#     @http.route('/dn_inventory_dashboard/dn_inventory_dashboard/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dn_inventory_dashboard/dn_inventory_dashboard/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dn_inventory_dashboard.listing', {
#             'root': '/dn_inventory_dashboard/dn_inventory_dashboard',
#             'objects': http.request.env['dn_inventory_dashboard.dn_inventory_dashboard'].search([]),
#         })

#     @http.route('/dn_inventory_dashboard/dn_inventory_dashboard/objects/<model("dn_inventory_dashboard.dn_inventory_dashboard"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dn_inventory_dashboard.object', {
#             'object': obj
#         })
