## Controller_informacion
```

  # TODO: VB
    @http.route('/get-ciudades-by-provincia/', type="json", auth='public', methods=['GET'], cors="*", csrf=False)
    def get_ciudades_by_provincia(self, **kw):
        try:
            data = request.jsonrequest
            id = int(data['id'])
            lista_ciudades = http.request.env['im_contact_city'].sudo().search([('state_id', '=', id)])
            ciudades = []
            for ciudad in lista_ciudades:
                ciudades.append({
                    'id': ciudad.id,
                    'name': ciudad.name if len(ciudad.name) <24 else (ciudad.name[:21] + '...')
                })
            return ciudades
        except Exception as e:
            _logger.info("Error en la obtención de ciudades y provincias " + str(e))
            return {'error': str(e)}
```
## Controller_informacion

```
    #TODO: Vinicio
    @http.route('/get-servicios-by-categoria/', type="json", auth='public', methods=['GET'], cors="*", csrf=False)
    def get_servicios_by_categoria(self, **kw):
        try:
            data = request.jsonrequest
            id = int(data['id'])
            listaservicios = http.request.env['botpress_comunication.lista_servicios'].sudo().search(
                [('active', '=', True), ('categoria', '=', id)], order='create_date desc')
            lista = []
            for servicio in listaservicios:
                lista.append({
                    'id': servicio.id,
                    'name': servicio.name,
                })
            return lista
        except Exception as e:
            _logger.info("Error en la obtención de los datos del cliente " + str(e))
            return {'error': str(e)}
```
