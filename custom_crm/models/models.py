# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class Visit(models.Model):
    # Estandar: Nombre del modelo y el nombre de la clase
    _name = 'custom_crm.visit'
    _description = 'visit'

    # Campos
    name = fields.Char(string="Description")
    customer = fields.Many2one(string="Customer", comodel_name="res.partner")
    # DateTime: Almacenado la fecha y la hora
    date = fields.Datetime(string="Date")
    type = fields.Selection([('P', 'Presencial'), ('V', 'Virtual')], string="Type", required=True)
    done = fields.Boolean(string="Done", readonly=True)
    image = fields.Binary(string="Image")

    def toggle_state(self):
        self.done = not self.done

    def f_create(self):
        visit = {
            'name': 'Visita 1',
            'customer': 1,
            'date': '2020-06-01 10:00:00',
            'type': 'P',
            'done': False,
        }
        print(visit)
        # Nombre del modeo y el metodo create para guardar el registro en la base de datos
        self.env['custom_crm.visit'].create(visit)

    def f_search_update(self):
        # Buscar el registro en la base de datos
        visit = self.env['custom_crm.visit'].search([('name', '=', 'dawdadawd')])
        print("Visita encontrada: ", visit, visit.name)

        # Actualizar el registro
        visit_v = self.env['custom_crm.visit'].browse([2])
        print("Visita encontrada - one: ", visit_v, visit_v.name)

        # Actualizar el registro
        visit_v.write({'name': 'Grupo SCANNER'})

    def f_search_delete(self):
        # Buscar el registro en la base de datos
        visit = self.env['custom_crm.visit'].browse([2])
        print("Visita encontrada: ", visit, visit.name)

        # Eliminar el registro
        visit.unlink()


class VisitReport(models.AbstractModel):
    _name = 'report.custom_crm.report_visit_card'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('custom_crm.report_visit_card')
        return {
            'doc_ids': docids,
            'doc_model': self.env['custom_crm.visit'],
            'docs': self.env['custom_crm.visit'].browse(docids)
        }

class CustomSaleOrder(models.Model):
    #Modelo a cual se va a amplicar la funcionalidad
    _inherit = 'sale.order'
    zone = fields.Selection([('N', 'Norte'), ('S', 'Sur'), ('E', 'Este'), ('O', 'Oeste')], string="Zone", required=True)
