## Report Definition (<report>):
<report
    string="Informe visita"
    id="custom_crm_visit_report"
    model="custom_crm.visit"
    report_type="qweb-pdf"
    name="custom_crm.report_visit_card"
    file="custom_crm.report_visit_card"
    attachment_use="True"
/>


```
id: Es un identificador único para este informe. En este caso, custom_crm_visit_report.
model: Es el modelo de datos que se usará para generar el informe, en este caso, custom_crm.visit.
name: Es el nombre del informe que se utilizará para buscar la plantilla QWeb asociada, en este caso, custom_crm.report_visit_card.
file: Es el nombre del archivo del informe, en este caso, custom_crm.report_visit_card.
```

## 2 Plantilla QWeb (<template>):

```
<template id="report_visit_card">
    <!-- Contenido de la plantilla -->
</template>

```
id: Es un identificador único para esta plantilla, en este caso, report_visit_card.
El contenido de la plantilla utiliza la sintaxis QWeb para definir cómo se debe generar el informe.

## 3 Modelo de Informe (VisitReport):
```
class VisitReport(models.AbstractModel):
    _name = 'report.custom_crm.report_visit_card'
    @api.model
    def _get_report_values(self, docids, data=None):
        # Lógica para obtener los valores necesarios para la plantilla
    ```
- `_name`: Es el nombre técnico del modelo de informe.
- `_get_report_values`: Es un método que se llama para obtener los valores necesarios para generar el informe. En este caso, obtiene los valores del modelo `custom_crm.visit` para los documentos identificados por `docids`.

```
En resumen, el id en el informe (<report>) se utiliza para identificar y llamar al informe desde otras partes del sistema. El name en el informe se utiliza para encontrar la plantilla asociada (<template>). El modelo de informe (VisitReport) se encarga de proporcionar los valores necesarios para la generación del informe.



