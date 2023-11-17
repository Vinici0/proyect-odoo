# proyect-odoo


## Reportes
```
report/visit.xml
<odoo>
    <data>
        <report
            string="Informe visita"
            id="custom_crm_visit_report"
            model="custom_crm.visit"
            report_type="qweb-pdf"
            name="custom_crm.report_visit_card"
            file="custom_crm.report_visit_card"
            attachment_use="True"
        />
    </data>
</odoo>

Tienen que concidir el report_visit_card" con el -> name="custom_crm.report_visit_card"

view/tamplate.xml
<odoo>
    <data>
        <template id="report_visit_card">
            <t t-call="web.html_container">
                <t t-foreach="docs" t-as="o">
                    <t t-call="web.external_layout">
                        <div class="page">
                            <h2>Visita</h2>
                            <p>Cliente:
                                <span t-field="o.customer.name"/>
                            </p>
                            <p>Descripción:
                                <span t-field="o.name"/>
                            </p>
                            <p>Fecha:
                                <span t-field="o.date" t-options='{"format": "dd/MM/yyyy"}' />
                            </p>
                        </div>
                    </t>
                </t>
            </t>
        </template>
    </data>
</odoo>


```
