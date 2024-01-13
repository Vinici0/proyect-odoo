### Los herrajes, herramientas, etc., deben facturarse con el motivo MATERIALES, para eso debe crearse en el producto un check y qué se elija el producto con el cual facturar

```
 @api.model
    def get_info_factura(self, invoice_id, node):
         for line in invoice_line_data:
                        producto = self.env['product.template'].search([('id','=',line['product_id'])])
                        if producto.rango == 'materiales' or (producto.type == 'service' and producto.is_service_invoice == True):
                         
                    for line in invoice_line_data:
                        producto = self.env['product.template'].search([('id','=',line['product_id'])])
                        if producto.type == 'service' and producto.is_service_invoice == False:
                            #Resto del codigo

      return node
```
