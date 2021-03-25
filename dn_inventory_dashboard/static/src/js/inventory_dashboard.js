odoo.define('dn_inventory_dashboard.dn_InventoryDashboard', function(require) {
"use strict";
//console.log('inventory dashboard custom');

var core = require('web.core');
var KanbanController = require('web.KanbanController');
var KanbanModel = require('web.KanbanModel');
var KanbanRenderer = require('web.KanbanRenderer');
var KanbanView = require('web.KanbanView');
var view_registry = require('web.view_registry');

var QWeb = core.qweb;

//--------------------------------------------------------------------------
// Kanban View
//--------------------------------------------------------------------------

var StockKanbanDashboardController = KanbanController.extend({
    custom_events:_.extend({}, KanbanController.prototype.custom_events, {
        dashboard_open_action: '_onDashboardOpenAction',
    }),

    /**
     * @private
     * @param {OdooEvent} event
     */
    _onDashboardOpenAction: function(event) {
        let action_act_window = {
            name: event.data.action_name,
            res_model: "stock.picking",
            context: event.data.action_context,
            views: [[false, 'list'], [false, 'form']],
            type: 'ir.actions.act_window',
            view_mode: "list",
        }
        if(event.data.domain){
            action_act_window['domain'] = [['id', 'in', event.data.domain]]
        }
        return this.do_action(action_act_window);
    },
});

var StockKanbanDashboardRenderer = KanbanRenderer.extend({
    events:_.extend({}, KanbanRenderer.prototype.events, {
        'click .o_dn_inventory_action': '_onDashboardOpenClicked',
    }),

    _render: async function () {
        var self = this;
        const super_def = await this._super(...arguments);
        const stockValues = await this._rpc({
            model: "stock.picking.type",
            method: "get_stock_dashboard_data",
            args:[this.state.res_ids],
        });
        return Promise.all([super_def, stockValues]).then(function(results){
            const stock_dashboard = QWeb.render('dn.InventoryDashboard', {
                stockValues: results[1],
            });
            self.$el.prepend(stock_dashboard);
        });
    },

    _onDashboardOpenClicked: function(event) {
        event.preventDefault();
        var $action = $(event.currentTarget);
        this.trigger_up('dashboard_open_action', {
            action_name: $action.attr('title'),
            action_context: $action.attr('context'),
            domain: $action.data('domain'),
        });
    },
});

//
var StockKanbanDashboardView = KanbanView.extend({
    config: _.extend({}, KanbanView.prototype.config, {
        Renderer: StockKanbanDashboardRenderer,
        Controller: StockKanbanDashboardController,
    })
});

// add custom stock picking type kanban dashboard to view registry
view_registry.add('stock_picking_type_kanban_dashboard', StockKanbanDashboardView);

return {
    StockKanbanDashboardRenderer,
    StockKanbanDashboardController,
};

});