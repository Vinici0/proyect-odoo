# -*- coding: utf-8 -*-
from odoo import http

# class AccountMigration(http.Controller):
#     @http.route('/account_migration/account_migration/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_migration/account_migration/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_migration.listing', {
#             'root': '/account_migration/account_migration',
#             'objects': http.request.env['account_migration.account_migration'].search([]),
#         })

#     @http.route('/account_migration/account_migration/objects/<model("account_migration.account_migration"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_migration.object', {
#             'object': obj
#         })