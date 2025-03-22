# -*- coding: utf-8 -*-
# from odoo import http


# class GestionDocumentsStage(http.Controller):
#     @http.route('/gestion_documents_stage/gestion_documents_stage', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_documents_stage/gestion_documents_stage/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_documents_stage.listing', {
#             'root': '/gestion_documents_stage/gestion_documents_stage',
#             'objects': http.request.env['gestion_documents_stage.gestion_documents_stage'].search([]),
#         })

#     @http.route('/gestion_documents_stage/gestion_documents_stage/objects/<model("gestion_documents_stage.gestion_documents_stage"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_documents_stage.object', {
#             'object': obj
#         })

