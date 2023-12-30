# -*- coding: utf-8 -*-
import logging
import datetime

_logger = logging.getLogger(__name__)

import psycopg2
from psycopg2.extras import DictCursor, RealDictCursor

from odoo import http
from odoo.http import Response, request
from odoo.tools import config


class BotpressControllerPosventa(http.Controller):
    @http.route('/get-servicios-complementarios/', type="json", auth='public', methods=['GET'], cors="*", csrf=False)
    def get_servicios_complementarios(self, **kw):
        try:
            servicios = http.request.env['botpress_comunication.servicio_complementario'].sudo().search_read(
                [('active', '=', True)], ["name", "categoria"])
            for servicio in servicios:
                servicio['categoria'] = servicio['categoria'][0]
            return servicios
        except Exception as e:
            _logger.info("Error en la obtención de los servicios complementarios " + str(e))
            return {'error': str(e)}

    @http.route('/get-soporte-tecnico/', type="json", auth='public', methods=['GET'], cors="*", csrf=False)
    def get_soporte_tecnico(self, **kw):
        try:
            soportetec = http.request.env['botpress_comunication.soporte_tecnico'].sudo().search(
                [('active', '=', True)])
            res = {
                'lista': [],
                'opciones': {}
            }
            for soporte in soportetec:
                if str(soporte.id) not in res['opciones']:
                    print("nuevo")
                    res['lista'].append({
                        'id': soporte.id,
                        'name': soporte.name
                    })
                    res['opciones'][str(soporte.id)] = []
                for opcion in soporte.opciones:
                    res['opciones'][str(soporte.id)].append({
                        'id': opcion.id,
                        'name': opcion.name,
                        'categoria': opcion.categoria.id
                    })
            print(res)
            return res
        except Exception as e:
            _logger.info("Error en la obtención de los servicios complementarios " + str(e))
            return {'error': str(e)}

    @http.route('/verificar-ticket/', type="json", auth='none', method=['POST'], cors="*", csrf=False)
    def _nuevo_ticket(self, **kw):
        try:
            data = request.jsonrequest
            categoria_ticket = int(data['categoria_ticket'])
            contrato = int(data['contrato'])
            conn = psycopg2.connect(
                host=config['gserp_db_host'],
                database=config['gserp_db_name'],
                user=config['gserp_db_user'],
                password=config['gserp_db_password'])
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"""select c.name from analytic_sale_order_line l, product_product p, product_template t, codigo_servicio c 
                    where l.subscription_product_line_id={contrato} and l.product_id=p.id and p.product_tmpl_id=t.id and 
                    t.tipo_servicio='principal' and l.codigo_servicio=c.id limit 1;"""
            cursor.execute(query)
            cuenta = cursor.fetchall()
            categoria_ticket = http.request.env['botpress_comunication.ticket_categoria_ref'].sudo().search(
                [('id', '=', categoria_ticket)], limit=1)
            # Verificación de señales
            querycoincidencia = f"""select * from website_support_ticket where category={categoria_ticket.identificador_categoria} and 
                                sub_category_id={categoria_ticket.identificador_subcategoria} and cod_service='{cuenta}' and 
                                subservice_id={categoria_ticket.identificador_descripcion if categoria_ticket.identificador_descripcion != 0 else 'null'};"""
            cursor.execute(querycoincidencia)
            ticket_coincidente = cursor.fetchall()
            if len(ticket_coincidente) > 0:
                res = {"ticket_creado": True, "ticket_id": ticket_coincidente[0]['id']}
            else:
                res = {"ticket_creado": False}
            return res
        except Exception as e:
            _logger.info("Error en la creacion de ticket " + str(e))
            return {'status': 500, 'error': str(e)}


    @http.route('/crear-ticket/', type="json", auth='none', method=['POST'], cors="*", csrf=False)
    def _nuevo_ticket(self, **kw):
        try:
            data = request.jsonrequest
            print(data)
            fecha = datetime.datetime.now()
            contrato = int(data['contrato'])
            partner_id = int(data['partner_id'])
            name = data['name']
            email = data['email']
            description = data['comentario']
            categoria_ticket = int(data['categoria_ticket'])
            conn = psycopg2.connect(
                host=config['gserp_db_host'],
                database=config['gserp_db_name'],
                user=config['gserp_db_user'],
                password=config['gserp_db_password'])
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"""select c.name from analytic_sale_order_line l, product_product p, product_template t, codigo_servicio c 
                    where l.subscription_product_line_id={contrato} and l.product_id=p.id and p.product_tmpl_id=t.id and 
                    t.tipo_servicio='principal' and l.codigo_servicio=c.id limit 1;"""
            cursor.execute(query)
            cuenta = cursor.fetchall()
            query = f"""select number_next from ir_sequence where code='website.support.ticket';"""
            cursor.execute(query)
            secuencia = cursor.fetchall()
            cuenta = cuenta[0]['name']
            categoria_ticket = http.request.env['botpress_comunication.ticket_categoria_ref'].sudo().search(
                [('id', '=', categoria_ticket)], limit=1)
            query = f"""select s.id sla, r.id sla_rule from website_support_sla_rule r, website_support_sla s 
                where s.name='{categoria_ticket.prioridad}' and r.name='{categoria_ticket.prioridad}' limit 1;"""
            cursor.execute(query)
            sla = cursor.fetchall()
            print(sla)
            conn2 = psycopg2.connect(
                host=config['db_host_matrix'],
                database=config['db_name_matrix'],
                user=config['db_user_matrix'],
                password=config['db_password_matrix'])
            cursor2 = conn2.cursor(cursor_factory=RealDictCursor)
            query = f"""select concat(mazs.name, ' ', rcs.name) zona, macs.direccion as direccion, mazs.nombre_zona_servicio
                from matrix_admin_zona_servicio mazs, matrix_admin_codigo_servicio macs
                join res_country_state rcs on macs.provincia = rcs.id
                where mazs.id = macs.zona_servicio_id and macs.name ='{cuenta}'
                and macs.name not like 'V%%' and macs.name not like 'I%%' and macs.name not like 'L%%'
                and macs.name not like 'T%%' and macs.name not like 'X%%' limit 1;"""
            cursor2.execute(query)
            direccion = cursor2.fetchall()
            print(direccion)
            cursor2.close()
            conn2.close()
            subject = 'CORRECTIVO' if categoria_ticket.identificador_categoria == 8 else (
                'QUEJAS' if categoria_ticket.identificador_categoria == 5 else 'REQUERIMIENTO')
            query = f"""insert into website_support_ticket (ticket_number,channel,partner_id,person_name,category,sub_category_id,email,description,subject,cod_service,cod_service_address,
                                priority_id,sla_timer,sla_id,sla_rule_id,subservice_id,zona,state,create_date,statebar,unattended) values ({secuencia[0]['number_next']},'GS BOT',{partner_id},'{name}',
                                {categoria_ticket.identificador_categoria},{categoria_ticket.identificador_subcategoria},'{email}','{description}',
                                '{subject}','{cuenta}','{direccion[0]['direccion']}',{categoria_ticket.priority},{categoria_ticket.sla_time},{sla[0]['sla']},{sla[0]['sla_rule']},
                                {categoria_ticket.identificador_descripcion if categoria_ticket.identificador_descripcion != 0 else 'null'},'{direccion[0]['zona']}',9,'{fecha}','por_atender',true)"""
            ticket_coincidente = cursor.fetchall()
            if len(ticket_coincidente)>0:
                res = {"ticket_creado": True, "ticket_id": ticket_coincidente[0]['id']}
            else: #Ejecuta el insert
                cursor.execute(query)
                query = f"""update ir_sequence set number_next={secuencia[0]['number_next'] + 1} where code='website.support.ticket';"""
                cursor.execute(query)
                conn.commit()
            cursor.close()
            conn.close()
            return {'status': 200, 'status_response': "ok", 'ticket': secuencia[0]['number_next']}
        except Exception as e:
            _logger.info("Error en la creacion de ticket " + str(e))
            return {'status': 500, 'error': str(e)}
