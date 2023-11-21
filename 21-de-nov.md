<odoo>
  <data>
    <!-- List Product -->
    <record model="ir.ui.view" id="pruebas_stock.list">
      <field name="name">pruebas_stock list</field>
      <field name="model">pruebas_stock.producto</field>
      <field name="arch" type="xml">
        <tree>
            <field name="name"/>
            <field name="solicitor"/>
            <field name="product"/>
        </tree>
      </field>
    </record>

    <!-- List Asignar -->
    <record model="ir.ui.view" id="pruebas_stock.asignar_list">
      <field name="name">pruebas_stock list</field>
      <field name="model">pruebas_stock.asing_line</field>
      <field name="arch" type="xml">
        <tree>
            <field name="name"/>
            <field name="quantity"/>
        </tree>
      </field>
    </record>

    <!-- From Pruebas Stock --> 
    <record model="ir.ui.view" id="pruebas_stock.form">
      <field name="name">pruebas_stock form</field>
      <field name="model">pruebas_stock.producto</field>
      <field name="arch" type="xml">
        <form>
          <sheet>
            <group>
              <field name="name"/>
              <field name="solicitor"/>
              <field name="product"/>
            </group>
          </sheet>
        </form>
      </field>
    </record>


    <!-- From Asignar -->
    <record model="ir.ui.view" id="pruebas_stock.asignar_form">
      <field name="name">pruebas_stock form</field>
      <field name="model">pruebas_stock.asing_line</field>
      <field name="arch" type="xml">
        <form>
          <sheet>
            <group>
              <field name="name"/>
              <field name="quantity"/>
            </group>
          </sheet>
        </form>
    </field>
    </record>

  <!-- Acciones -->
    <record model="ir.actions.act_window" id="pruebas_stock.action_window">
      <field name="name">pruebas_stock window</field>
      <field name="res_model">pruebas_stock.producto</field>
      <field name="view_mode">tree,form</field>
    </record>  

    <record model="ir.actions.act_window" id="pruebas_stock.asignar_window">
      <field name="name">pruebas_stock window</field>
      <field name="res_model">pruebas_stock.asing_line</field>
      <field name="view_mode">form</field>
    </record>
  </data>
</odoo>


# -*- coding: utf-8 -*-

from odoo import models, fields, api


class asing_product(models.Model):
    _name = 'pruebas_stock.producto'
    _description = 'pruebas_stock.producto'

    name = fields.Char(string="Nombre del Acta", required=True)
    solicitor = fields.Many2one('hr.employee', string="Solicitante")
    product = fields.Many2one(models_name="pruebas_stock.asing_line", inverse_name="name", string="Productos")


class asing_product_line(models.Model):
    _name = 'pruebas_stock.asing_line'
    _description = 'pruebas_stock.asing_line'

    name = fields.Char(string="Nombre del Producto", required=True)
    quantity = fields.Integer(string="Cantidad")



