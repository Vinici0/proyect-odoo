## Ubicar en el archivo controller_contabilidad.py
```
 @http.route('/get-invoice/id/', type="json", auth='public', method=['GET'], cors="*", csrf=False)
    def _get_invoice_pdf_id(self, **kw):
        try:

            data = request.jsonrequest
            id = data['id']
            common_gserp = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(urlgserp), context=s)

            #TODO: Verificar error
            uid_gserp = common_gserp.authenticate(db_gserp, user_gserp, password_gserp, {})
            models_gserp = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(urlgserp), context=s)
            factura = models_gserp.execute_kw(db_gserp, uid_gserp, password_gserp, 'botpress_comunication',
                                              'getFacturaById', [id], {})
            if factura != '':
                factura = factura.encode('ascii')
                aux = http.request.env['botpress_comunication.factura'].sudo().search([('name', '=', str(id))],
                                                                                      limit=1)
                if len(aux) == 1:  # Reemplaza si ya se ha generado un factura
                    aux.write({
                        'media': factura
                    })
                    factura = aux
                else:
                    factura = http.request.env['botpress_comunication.factura'].sudo().create({
                        'name': id,
                        'media': factura
                    })
                atta = http.request.env['ir.attachment'].sudo().search(
                    [('res_model', '=', 'botpress_comunication.factura'), ('res_field', '=', 'media'),
                     ('res_id', '=', factura.id)],
                    limit=1)
                ruta = atta._full_path(atta.store_fname)
                with open(str(ruta), "rb") as pdf:
                    factura = pdf.read()
            return Response(factura, content_type='application/pdf', status=200)

        #En caso de error
        except Exception as e:
            _logger.info("Error en la obtención de la factura por id", str(e))
            res = json.dumps({'error': str(e)}, ensure_ascii=False).encode('utf-8')
            return Response(res, content_type='application/json;charset=utf-8', status=500)
```


