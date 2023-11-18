Como puedo hacer para que f_search_delete recupere el valor del boton del rwo seleccionado   
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
    
   
    def f_search_delete(self):
        # Buscar el registro en la base de datos
        visit = self.env['custom_crm.visit'].browse([2])
        print("Visita encontrada: ", visit, visit.name)

        # Eliminar el registro
        # visit.unlink()
        
        
        
                    <button name="f_search_delete"  string="Buscar y borrar" type="object" class="oe_highlight"/>
