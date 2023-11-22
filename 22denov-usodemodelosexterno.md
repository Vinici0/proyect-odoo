```
<odoo>
    <data>

        <!-- View -->
        <record model="ir.ui.view" id="produc_stock.list">
            <field name="name">produc_stock list</field>
            <field name="model">produc_stock.produc_stock</field>
            <field name="arch" type="xml">
                <tree>
                    <field name="name"/>
                    <field name="applicant"/>
                    <field name="product_lines_ids"/>
                </tree>
            </field>
        </record>

        <!-- View -->
        <record model="ir.ui.view" id="produc_stock.list_line">
            <field name="name">produc_stock list</field>
            <field name="model">produc_stock.produc_stock_line</field>
            <field name="arch" type="xml">
                <tree>
                    <field name="id_product"/>
                    <field name="name"/>
                    <field name="quantity"/>
                    <field name="serie"/>
                </tree>
            </field>
        </record>

   
        <!-- Form -->
        <record model="ir.ui.view" id="produc_stock.form">
            <field name="name">produc_stock form</field>
            <field name="model">produc_stock.produc_stock</field>
            <field name="arch" type="xml">
                <form>
                    <sheet>
                        <group>
                            <field name="name"/>
                            <field name="applicant"/>
                        </group>
                        <notebook>
                            <page string="Product Lines" >
                                <field name="product_lines_ids">
                                    <tree editable="bottom">
                                        <field name="id_product" invisible="1"/>
                                        <field name="name"/>
                                        <field name="quantity"/>
                                        <field name="serie"/>
                                    </tree>
                                </field>
                            </page>
                        </notebook>
                    </sheet>

                </form>
            </field>
        </record>

        <!-- Form -->
        <record model="ir.ui.view" id="produc_stock.form_line">
            <field name="name">produc_stock form</field>
            <field name="model">produc_stock.produc_stock_line</field>
            <field name="arch" type="xml">
                <form>
                    <sheet>
                        <group>
                            <field name="id_product"/>
                            <field name="name"/>
                            <field name="quantity"/>
                            <field name="serie"/>
                        </group>
                    </sheet>

                </form>
            </field>
        </record>

        <!-- actions opening views on models -->
        <record model="ir.actions.act_window" id="produc_stock.action_window">
            <field name="name">produc_stock window</field>
            <field name="res_model">produc_stock.produc_stock</field>
            <field name="view_mode">tree,form</field>
        </record>

        <record model="ir.actions.act_window" id="produc_stock.action_window_line">
            <field name="name">produc_stock window</field>
            <field name="res_model">produc_stock.produc_stock_line</field>
            <field name="view_mode">tree,form</field>
        </record>



        <!-- Top menu item -->

        <menuitem name="produc_stock" id="produc_stock.menu_root"/>

        <!-- menu categories -->

        <menuitem name="Menu 1" id="produc_stock.menu_1" parent="produc_stock.menu_root"/>

        <!-- actions -->

        <menuitem name="List" id="produc_stock.menu_1_list" parent="produc_stock.menu_1"
                  action="produc_stock.action_window"/>

        <menuitem name="Form" id="produc_stock.menu_1_form" parent="produc_stock.menu_1"
                    action="produc_stock.action_window_line"/>  

               

    </data>
</odoo>
```

Modelo
```
# -*- coding: utf-8 -*-

from odoo import models, fields, api

class produc_stock(models.Model):
    _name = 'produc_stock.produc_stock'
    _description = 'produc_stock.produc_stock'

    name = fields.Char(string='Nombres')
    applicant = fields.Many2one('hr.employee', string='Solicitante')
    product_lines_ids = fields.One2many('produc_stock.produc_stock_line',
                                        'id_product',
                                        string='Producto')

class produc_stock_line(models.Model):
    _name = 'produc_stock.produc_stock_line'
    _description = 'produc_stock.produc_stock_line'
    #ID_PRODUCTO = Relaciona con la clase principal de arriba
    id_product = fields.Many2one('produc_stock.produc_stock', string='id producto')

    #PRODUCTO = Relaciona con la clase product.template
    name = fields.Many2one('product.template', string='Producto')
    serie = fields.Char(string='Serie')
    quantity = fields.Integer(string='Cantidad')


```
