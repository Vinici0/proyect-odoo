```
# -*- coding: utf-8 -*-
from odoo import http


class Employee(http.Controller):
    @http.route('/employee/employee', auth='public')
    def index(self, **kw):
        return "Hello, world"
    
    
    @http.route('/employee/location', auth='public', website=False, type='json', methods=['GET', 'POST'])
    def location(self, **kw):
        locations = http.request.env['employee.location'].sudo().search([])
        location_list = []
        for location in locations:
            location_list.append({
                'name': location.name,
                'street_address': location.street_address,
                'city': location.city
            })
        return location_list
```
```
from odoo import models, fields, api

class employee(models.Model):
    _name = 'employee.employee'
    _description = 'Empleado'

    name = fields.Char(string='Nombre')
    email = fields.Char(string='Correo Electrónico')
    phone = fields.Char(string='Teléfono')
    status = fields.Selection([('active','Activo'),('inactive','Inactivo')], string='Estado')
    department = fields.Many2one('employee.department', string='Departamento')
    
    
class department(models.Model):
    _name = 'employee.department'
    _description = 'Departamento'

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')
    employee = fields.One2many('employee.employee', inverse_name='department', string='Empleados')
    location = fields.Many2one('employee.location', string='Ubicación')
    
    
class location(models.Model):
    _name = 'employee.location'
    _description = 'Ubicación'

    name = fields.Char(string='Nombre')
    street_address = fields.Char(string='Dirección')
    postal_code = fields.Char(string='Código Postal')
    city = fields.Char(string='Ciudad')
    department = fields.One2many('employee.department', inverse_name='location', string='Departamento')
```







```
<odoo>
  <data>


    <!--                          Tree                             -->
    <record model="ir.ui.view" id="employee.list">
      <field name="name">employee list</field>
      <field name="model">employee.employee</field>
      <field name="arch" type="xml">
        <tree>
          <field name="name" />
          <field name="email" />
          <field name="phone" />
          <field name="status" />
          <field name="department" />
        </tree>
      </field>
    </record>

    <record model="ir.ui.view" id="employee.department_list">
      <field name="name">department list</field>
      <field name="model">employee.department</field>
      <field name="arch" type="xml">
        <tree>
          <field name="name" />
          <field name="description" />
          <field name="employee" />
          <field name="location" />
        </tree>
      </field>
    </record>


    <record model="ir.ui.view" id="employee.location_list">
      <field name="name">location list</field>
      <field name="model">employee.location</field>
      <field name="arch" type="xml">
        <tree>
          <field name="name" />
          <field name="street_address" />
          <field name="postal_code" />
          <field name="city" />
          <field name="department" />
        </tree>
      </field>
    </record>

    <!--                          Form                            -->
    <record model="ir.ui.view" id="employee.form">
      <field name="name">employee form</field>
      <field name="model">employee.employee</field>
      <field name="arch" type="xml">
        <form>
          <sheet>
            <group>
              <field name="name" />
              <field name="email" />
              <field name="phone" />
              <field name="status" />
              <field name="department" />
            </group>
          </sheet>
        </form>
      </field>
    </record>

    <record model="ir.ui.view" id="employee.department_form">
      <field name="name">department form</field>
      <field name="model">employee.department</field>
      <field name="arch" type="xml">
        <form>
          <sheet>
            <group>
              <field name="name" />
              <field name="description" />
              <field name="employee" />
              <field name="location" />
            </group>
          </sheet>
        </form>
      </field>
    </record>

    <record model="ir.ui.view" id="employee.location_form">
      <field name="name">location form</field>
      <field name="model">employee.location</field>
      <field name="arch" type="xml">
        <form>
          <sheet>
            <group>
              <field name="name" />
              <field name="street_address" />
              <field name="postal_code" />
              <field name="city" />
              <field name="department" />
            </group>
          </sheet>
        </form>
      </field>
    </record>

    <!-- actions opening views on models -->

    <record model="ir.actions.act_window" id="employee.action_window">
      <field name="name">Employee</field>
      <field name="res_model">employee.employee</field>
      <field name="view_mode">tree,form</field>
    </record>

    <record model="ir.actions.act_window" id="employee.department_window">
      <field name="name">Department</field>
      <field name="res_model">employee.department</field>
      <field name="view_mode">tree,form</field>
    </record>

    <record model="ir.actions.act_window" id="employee.location_window">
      <field name="name">Location</field>
      <field name="res_model">employee.location</field>
      <field name="view_mode">tree,form</field>
    </record>


    <!-- Top menu item -->
    <menuitem name="Administracion" id="employee.menu_root" />

    <!-- menu categories -->
    <menuitem name="Empleados" id="employee.menu_1" parent="employee.menu_root" />


    <!-- actions -->
    <menuitem name="Infomracion Empleados" id="employee.menu_1_list" parent="employee.menu_1"
      action="employee.action_window" />

    <menuitem name="Infomracion Departamentos" id="employee.menu_2_list" parent="employee.menu_1"
      action="employee.department_window" />

    <menuitem name="Infomracion Locaciones" id="employee.menu_3_list" parent="employee.menu_1"
      action="employee.location_window" />
  </data>
</odoo>

```






id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_employee_employee,employee.employee,model_employee_employee,base.group_user,1,1,1,1
access_employee_department,employee.department,model_employee_department,base.group_user,1,1,1,1
access_employee_location,employee.location,model_employee_location,base.group_user,1,1,1,1
