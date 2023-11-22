![Captura de pantalla de 2023-11-22 09-55-16](https://github.com/Vinici0/proyect-odoo/assets/75345399/919bb8a4-aa8c-44c1-b317-bb287366294b)

Agregar boton en la tabla:

```
        <record model="ir.ui.view" id="employee.department_form">
            <field name="name">department form</field>
            <field name="model">employee.department</field>
            <field name="arch" type="xml">
                <form>
                    <sheet>
                        <group>
                            <field name="name"/>
                            <field name="description"/>
                            <field name="employee" widget="many2many" options="{'no_create': True}">
                                <tree editable="bottom">
                                    <field name="name"/>
                                    <field name="email"/>
                                    <field name="phone"/>
                                    <field name="status"/>
                                </tree>
                            </field>
                            <field name="location"/>
                        </group>
                    </sheet>
                </form>
            </field>
        </record>
```

Modelos:

```
class employee(models.Model):
    _name = 'employee.employee'
    _description = 'Empleado'
    name = fields.Char(string='Nombre')
    email = fields.Char(string='Correo Electrónico')
    phone = fields.Char(string='Teléfono')
    status = fields.Selection([('active', 'Activo'), ('inactive', 'Inactivo')], string='Estado')
    department = fields.Many2one('employee.department', string='Departamento')


class department(models.Model):
    _name = 'employee.department'
    _description = 'Departamento'
    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')
    employee = fields.One2many('hr_employee', inverse_name='department', string='Empleados')
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
