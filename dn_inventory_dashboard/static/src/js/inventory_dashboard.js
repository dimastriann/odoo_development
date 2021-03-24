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

var StockKanbanDashboardModel = KanbanModel.extend({
    /**
     * @override
     */
    init: function() {
        this.stockDashboardValues = {};
        this._super.apply(this, arguments);
    },
    /**
     * @override
     */
    __get: function (localID) {
        var result = this._super.apply(this, arguments);
        if (_.isObject(result)) {
            result.stockDashboardValues = this.stockDashboardValues[localID];
        }
        return result;
    },
    /**
     * @override
     * @returns {Promise}
     */
    __load: function() {
        return this._loadDashboard(this._super.apply(this, arguments));
    },
    /**
     * @override
     * @returns {Promise}
     */
    __reload: function() {
        return this._loadDashboard(this._super.apply(this, arguments));
    },

    _loadDashboard: function(super_def) {
        var self = this;
        var dashboard_stock_def = this._rpc({
            model: "stock.picking.type",
            method: "get_stock_dashboard_data",
        });
        return Promise.all([super_def, dashboard_stock_def]).then(function(results){
            var id = results[0];
            var stockDashboardValues = results[1];
            self.stockDashboardValues[id] = stockDashboardValues;
            return id;
        });
    },
});

var StockKanbanDashboardController = KanbanController.extend({
    custom_events:_.extend({}, KanbanController.prototype.custom_events, {
        dashboard_open_action: '_onDashboardOpenAction',
    }),

    /**
     * @private
     * @param {OdooEvent} event
     */
    _onDashboardOpenAction: function(event) {
//        return this.do_action(event.data.action_name,
//            {additional_context: JSON.parse(event.data.action_context)});
        return this.do_action({
            name: event.data.action_name,
            res_model: "stock.picking",
            context: event.data.action_context,
            views: [[false, 'list'], [false, 'form']],
            type: 'ir.actions.act_window',
            view_mode: "list"
        });
    },
});

var StockKanbanDashboardRenderer = KanbanRenderer.extend({
    events:_.extend({}, KanbanRenderer.prototype.events, {
        'click .o_dn_inventory_action': '_onDashboardOpenClicked',
    }),

    _render: function () {
        var self = this;
        return this._super.apply(this, arguments).then(function () {
            var values = self.state.stockDashboardValues;
            console.log('values', values);
            var title_ex = 'Example Title';
            var stock_dashboard = QWeb.render('dn.InventoryDashboard', {
                stockValues: values,
                title_test: title_ex,
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
        });
    },
});

//
var StockKanbanDashboardView = KanbanView.extend({
    config: _.extend({}, KanbanView.prototype.config, {
        Model: StockKanbanDashboardModel,
        Renderer: StockKanbanDashboardRenderer,
        Controller: StockKanbanDashboardController,
    })
});

// add custom stock picking type kanban dashboard to view registry
view_registry.add('stock_picking_type_kanban_dashboard', StockKanbanDashboardView);

//return {
////    StockKanbanDashboardModel: StockKanbanDashboardModel,
//    StockKanbanDashboardRenderer: StockKanbanDashboardRenderer,
//    StockKanbanDashboardController: StockKanbanDashboardController,
//};

});