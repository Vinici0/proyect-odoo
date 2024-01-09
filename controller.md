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
Bootpress

```
const data = [
  {
    id: 1,
    name: "Vincio",
  },
  {
    id: 2,
    name: "Luna",
  },
  {
    id: 3,
    name: "Aurora",
  },
  {
    id: 4,
    name: "Esmeralda",
  },
  {
    id: 5,
    name: "Ciro",
  },
  {
    id: 6,
    name: "Dante",
  },
  {
    id: 7,
    name: "Isabella",
  },
  {
    id: 8,
    name: "Oliver",
  },
  {
    id: 9,
    name: "Oliver9",
  },
  {
    id: 10,
    name: "Oliver10",
  },
];

let opciones = [];

data.forEach((ser) => {
  opciones.push({ title: ser.name, value: ser.id + "" });
});

console.log(opciones);

const pagination = async () => {
  temp.isSiguiente = event.payload.payload === "SIGUIENTE" ? true : false;
  temp.isAnterior = event.payload.payload === "ANTERIOR" ? true : false;
};

const dataValues = async () => {
  let page = Number(temp.page),
    pageSize = 3;

  temp.page = temp.isSiguiente === true ? (page = page + 1) : page;

  const data = [
    {
      id: 1,
      name: "Vincio",
    },
    {
      id: 2,
      name: "Luna",
    },
    {
      id: 3,
      name: "Aurora",
    },
    {
      id: 4,
      name: "Esmeralda",
    },
    {
      id: 5,
      name: "Ciro",
    },
    {
      id: 6,
      name: "Dante",
    },
    {
      id: 7,
      name: "Isabella",
    },
    {
      id: 8,
      name: "Oliver",
    },
    {
      id: 9,
      name: "Oliver9",
    },
    {
      id: 10,
      name: "Oliver10",
    },
  ];

  const startIndex = page * pageSize;
  const endIndex = startIndex + pageSize;

  // Filtrar los elementos para obtener solo los de la página actual
  const currentPageData = data.slice(startIndex, endIndex);

  let opciones = [];

  currentPageData.forEach((ser) => {
    opciones.push({ title: ser.name, value: ser.id + "" });
  });

  //la opcion de anteriro y siguente agrega
  if (page > 0) {
    opciones.unshift({ title: "Anterior", value: "anterior" });
  }

  if (endIndex < data.length) {
    opciones.push({ title: "Siguiente", value: "siguiente" });
  }

  const messageselect = {
    type: "single-choice",
    skill: "choice",
    text: `Seleccione la categoría de servicio del que requiere más información:`,
    dropdownPlaceholder: "Seleccione...",
    choices: opciones,
    markdown: true,
  };

  await bp.events.replyToEvent(event, [messageselect]);
  //bloquuear la opcion que el usuario pueda escribir
  if(event.payload.type === "text"){
    await bp.events.replyToEvent(event, {type: 'text', text: 'Por favor seleccione una opción de la lista.'})
  }


};

return dataValues();

```
