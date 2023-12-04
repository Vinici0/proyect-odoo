mport psycopg2
import logging
import time
from odoo import fields, models, api, _
from psycopg2.extras import RealDictCursor
from odoo.tools import config

logger = logging.getLogger(name_)


class SyncAssets(models.Model):
    _name = 'master_sync.sync_assets'
    _description = 'master_sync.sync_assets'

    name = fields.Char(string="Nombre Activo")
    origin = fields.Char(string="Tabla escogida")
    id_stock = fields.Integer(string="Stock")
    action = fields.Char(string="Accion Realizada")

    @api.model
    def sync_account(self):
        print('master_sync.sync_assets')
        conn11 = None
        conn14 = None
        try:
            actualizados = 0
            creados = 0

            conn11 = psycopg2.connect(
                host=config['gserp_db_host'],
                database=config['gserp_db_name'],
                user=config['gserp_db_user'],
                password=config['gserp_db_password'])
            cursor11 = conn11.cursor(cursor_factory=RealDictCursor)
            conn14 = psycopg2.connect(
                host=config['db_host'],
                database=config['db_name'],
                user=config['db_user'],
                password=config['db_password'])
            cursor14 = conn14.cursor(cursor_factory=RealDictCursor)

            query = f"""SELECT * FROM account_account"""
            cursor11.execute(query)
            cursor14.execute(query)
            result_account11 = cursor11.fetchall()
            result_account14 = cursor14.fetchall()
            cont = 0
            for account11 in result_account11:
                exist = False
                for account14 in result_account14:
                    if account11['id'] == account14['id']:
                        exist = True
                        if account11['name'] == account14['name']:
                            if account11['user_type_id']:
                                self.check_user_type(cursor11, cursor14, account11['user_type_id'])
                            if account11['code']:
                                cont += 1
                                self.check_code_repit(account11, cursor14, conn14, cont)

                            print('actualiza ', account11['id'])

                            #TODO: Terminado
                            query = f"""UPDATE account_account SET code = '{account11['code']}', 
                                                                deprecated = {account11['deprecated']}, 
                                                                user_type_id = {account11['user_type_id']}, 
                                                                internal_type = '{account11['internal_type']}', 
                                                                reconcile = {account11['reconcile']}, 
                                                                note = '{account11['note']}',
                                                                company_id = {account11['company_id']},                                                                 
                                                                internal_group = '{account11['report_type']}'
                                                                WHERE  id = {account11['id']}"""
                            cursor14.execute(query)
                            conn14.commit()
                        else:
                            print('actualiza ', account11['id'])
                            if account11['user_type_id']:
                                self.check_user_type(cursor11, cursor14, account11['user_type_id'])
                            if account11['code']:
                                cont += 1
                                self.check_code_repit(account11, cursor14, conn14, cont)

                            #TODO: Terminado
                            query = f"""UPDATE account_account SET name = '{account11['name']}', 
                                                                code = '{account11['code']}', 
                                                                deprecated = {account11['deprecated']}, 
                                                                user_type_id = {account11['user_type_id']}, 
                                                                internal_type = '{account11['internal_type']}', 
                                                                reconcile = {account11['reconcile']}, 
                                                                note = '{account11['note']}',
                                                                company_id = {account11['company_id']},                                                         
                                                                internal_group = '{account11['report_type']}'
                                                                WHERE  id = {account11['id']}"""
                            cursor14.execute(query)
                            conn14.commit()

                if not exist:
                    print('crea ', account11['id'])

                    if account11['user_type_id']:
                        print('type id ', account11['user_type_id'])
                        self.check_user_type(cursor11, cursor14, account11['user_type_id'])
                    if account11['code']:
                        cont += 1
                        self.check_code_repit(account11, cursor14, conn14, cont)
                        
                       #TODO: Terminado
                    query = f"""INSERT INTO account_account (id, 
                                                            name, 
                                                            code, 
                                                            deprecated, 
                                                            user_type_id, 
                                                            internal_type, 
                                                            reconcile, 
                                                            note,
                                                            company_id,                                                             
                                                            internal_group) 
                                                            VALUES ({account11['id']}, 
                                                            '{account11['name']}',
                                                            '{account11['code']}', 
                                                            {account11['deprecated']}, 
                                                            {account11['user_type_id']}, 
                                                            '{account11['internal_type']}', 
                                                            {account11['reconcile']}, 
                                                            '{account11['note']}',
                                                            {account11['company_id']},                                                                 
                                                            '{account11['report_type']}')"""
                    cursor14.execute(query)
                    conn14.commit()

            self.account_journal(cursor14, cursor11,conn14, conn11)
            self.account_asset(cursor14, cursor11,conn14, conn11)
            print('*****SIN PROBLEMAS*******')

        except (Exception, psycopg2.DatabaseError) as error:
            _logger.info("Error %s" % str(error))

        finally:
            if conn11 is not None:
                conn11.close()
            if conn14 is not None:
                conn14.close()

    def check_code_repit(self, account11, cursor14, conn14, cont):
        encontrar2 = self.env['account.account'].search([('code', '=', account11['code'])])
        if encontrar2:
            if encontrar2.id != account11['id']:
                query = f"""update account_account set code = 'PENDIENTE{cont}' where id = {encontrar2.id}"""
                cursor14.execute(query)
                conn14.commit()

    def check_user_type(self, cursor11, cursor14, aid):
        query = f"""SELECT * FROM account_account_type WHERE id = {aid}"""
        cursor11.execute(query)
        cursor14.execute(query)
        type11 = cursor11.fetchone()
        type14 = cursor14.fetchone()
        print(aid)
        print(type11)
        print(type14)
        if type11 and type14:
            if type11['id'] == type14['id']:
                if type11['name'] != type14['name']:
                    print('actualiza type 1', type11['id'])
                    query = f"""UPDATE account_account_type SET name = '{type11['name']}', 
                                                    include_initial_balance = {type11['include_initial_balance']}, 
                                                    type = '{type11['type']}', 
                                                    internal_group = '{type11['report_type']}'
                                                    WHERE  id = {type11['id']}"""
                    cursor14.execute(query)
        else:
            print('actualiza type 1', type11['id'])
            query = f"""INSERT INTO account_account_type (id,
                                                    name,
                                                    include_initial_balance,
                                                    type,
                                                    internal_group) 
                                                    VALUES ({type11['id']},
                                                    '{type11['name']}',
                                                    {type11['include_initial_balance']},
                                                    '{type11['type']}',
                                                    '{type11['report_type']}'
                                                    )"""
            cursor14.execute(query)

    def account_journal(self, cursor14, cursor11,conn14, conn11):
        query = f"""SELECT * FROM account_journal"""
        cursor11.execute(query)
        cursor14.execute(query)
        result_journal11 = cursor11.fetchall()
        result_journal14 = cursor14.fetchall()
        cont2 = 0
        for journal11 in result_journal11:
            exist = False
            for journal14 in result_journal14:
                if journal11['id'] == journal14['id']:
                    exist = True
                    if journal11['name'] != journal14['name']:
                        # if account11['user_type_id']:
                        #     self.check_user_type(cursor11, cursor14, account11['user_type_id'])
                        # if account11['code']:
                        #     cont += 1
                        #     self.check_code_repit(account11, cursor14, conn14, cont)

                        print('actualiza ', journal11['id'])
                        self.validate_fk_journal(journal11)
                        cont2 += 1
                        self.check_code_repit_journal(journal11, cursor14, conn14, cont2)
                        query = f"""UPDATE account_journal SET name = '{journal11['name']}', 
                                                code = '{journal11['code']}', 
                                                active = {journal11['active']}, 
                                                type = '{journal11['type']}', 
                                                payment_credit_account_id = {journal11['default_credit_account_id']}, 
                                                payment_debit_account_id = {journal11['default_debit_account_id']},
                                                sequence = {journal11['sequence']},                                                                 
                                                company_id = '{journal11['company_id']}',
                                                refund_sequence = {journal11['refund_sequence']},
                                                at_least_one_inbound = {journal11['at_least_one_inbound']},
                                                at_least_one_outbound = {journal11['at_least_one_outbound']},
                                                bank_statements_source = '{journal11['bank_statements_source']}',
                                                show_on_dashboard = {journal11['show_on_dashboard']},
                                                color = {journal11['color']},
                                                invoice_reference_type = 'invoice',    
                                                invoice_reference_model = 'odoo'
                                                WHERE  id = {journal11['id']}"""
                        cursor14.execute(query)

            if not exist:
                print('crea ', journal11)
                self.validate_fk_journal(journal11)
                cont2 += 1
                self.check_code_repit_journal(journal11, cursor14, conn14, cont2)
                query = f"""INSERT INTO account_journal (id, 
                                                        name, 
                                                        code,
                                                        active,
                                                        type,
                                                        payment_credit_account_id,
                                                        payment_debit_account_id,
                                                        sequence,                                                            
                                                        company_id,
                                                        refund_sequence,
                                                        at_least_one_inbound,
                                                        at_least_one_outbound, 
                                                        bank_statements_source, 
                                                        show_on_dashboard,
                                                        invoice_reference_type,
                                                        invoice_reference_model,
                                                        color)                                          
                                                        VALUES ({journal11['id']}, 
                                                        '{journal11['name']}',
                                                        '{journal11['code']}', 
                                                         {journal11['active']},
                                                         '{journal11['type']}',
                                                         {journal11['default_credit_account_id']},
                                                         {journal11['default_debit_account_id']},
                                                         {journal11['sequence']},
                                                         {journal11['company_id']},
                                                         '{journal11['refund_sequence']}',
                                                         {journal11['at_least_one_inbound']},
                                                         {journal11['at_least_one_outbound']},
                                                         '{journal11['bank_statements_source']}',                                                        
                                                         {journal11['show_on_dashboard']},
                                                         'invoice',
                                                         'odoo',
                                                         {journal11['color']})"""
                cursor14.execute(query)
        conn14.commit()

    def check_code_repit_journal(self, account11, cursor14, conn14, cont):
        print('entra', account11['code'])
        encontrar2 = self.env['account.journal'].search([('code', '=', account11['code']), ('name', '=', account11['name'])])
        print('entra', encontrar2)
        if encontrar2:
            if encontrar2.id != account11['id']:
                print('entra', encontrar2.id)
                query = f"""update account_journal set code = 'Pe{cont}' where id = {encontrar2.id}"""
                cursor14.execute(query)
                conn14.commit()

    def validate_fk_journal(self, journal11):
        journal11['default_credit_account_id'] = 'null' if not journal11[
            'default_credit_account_id'] else journal11['default_credit_account_id']
        journal11['default_debit_account_id'] = 'null' if not journal11['default_debit_account_id'] else \
            journal11['default_debit_account_id']

    #TODO: Terminado
    def account_asset(self, cursor14, cursor11,conn14, conn11):
        query11 = f"""SELECT * FROM account_asset_asset"""
        query14 = f"""SELECT * FROM account_asset"""
        cursor11.execute(query11)
        cursor14.execute(query14)
        result_asset11 = cursor11.fetchall()
        result_asset14 = cursor14.fetchall()
        # cont2 = 0
        print('account_asset_asset')
        for asset11 in result_asset11:
            exist = False
            for asset14 in result_asset14:
                if asset11['id'] == asset14['id']:
                    exist = True
                    if asset11['name'] != asset14['name']:
                        if asset11['category_id']:
                            
                            self.check_account_category(cursor11, cursor14, asset11['category_id'], conn14)

                        print('actualiza ', asset11['id'])
                        asset11['partner_id'] = 'null' if not asset11['partner_id'] else asset11['partner_id']
                        # self.validate_fk_journal(journal11)
                        # cont2 += 1
                        # self.check_code_repit_journal(journal11, cursor14, conn14, cont2)
                        query = f"""UPDATE account_asset SET name = '{asset11['name']}', 
                                                        code = '{asset11['code']}', 
                                                        active = {asset11['active']}, 
                                                        purchase_value = {asset11['value']}, 
                                                        depreciation_base = {asset11['value']},
                                                        company_currency_id = 2, 
                                                        company_id = {asset11['company_id']},
                                                        profile_id = {asset11['category_id']},                                                                 
                                                        date_start = '{asset11['date']}',
                                                        state = '{asset11['state']}',
                                                        partner_id = {asset11['partner_id']},
                                                        method = '{asset11['method']}',
                                                        method_number = {asset11['method_number']},
                                                        method_period = {asset11['method_period']},
                                                        method_progress_factor = {asset11['method_progress_factor']},    
                                                        method_time = '{asset11['method_time']}',
                                                        prorata = {asset11['prorata']},
                                                        salvage_value = {asset11['salvage_value']}
                                                        WHERE  id = {asset11['id']}"""
                        cursor14.execute(query)
                    else:
                        print('actualiza ', asset11['id'])
                        if asset11['category_id']:
                            self.check_account_category(cursor11, cursor14, asset11['category_id'], conn14)

                        print('actualiza ', asset11['id'])
                        asset11['partner_id'] = 'null' if not asset11['partner_id'] else asset11['partner_id']
                        # self.validate_fk_journal(journal11)
                        # cont2 += 1
                        # self.check_code_repit_journal(journal11, cursor14, conn14, cont2)
                        query = f"""UPDATE account_asset SET code = '{asset11['code']}', 
                                                        active = {asset11['active']}, 
                                                        purchase_value = {asset11['value']}, 
                                                        depreciation_base = {asset11['value']},
                                                        company_currency_id = 2, 
                                                        company_id = {asset11['company_id']},
                                                        profile_id = {asset11['category_id']},                                                                 
                                                        date_start = '{asset11['date']}',
                                                        state = '{asset11['state']}',
                                                        partner_id = {asset11['partner_id']},
                                                        method = '{asset11['method']}',
                                                        method_number = {asset11['method_number']},
                                                        method_period = {asset11['method_period']},
                                                        method_progress_factor = {asset11['method_progress_factor']},    
                                                        method_time = '{asset11['method_time']}',
                                                        prorata = {asset11['prorata']},
                                                        salvage_value = {asset11['salvage_value']}
                                                        WHERE  id = {asset11['id']}"""
                        cursor14.execute(query)

            if not exist:
                print(asset11)
                if asset11['category_id']:
                    self.check_account_category(cursor11, cursor14, asset11['category_id'], conn14)
                asset11['partner_id'] = 'null' if not asset11['partner_id'] else asset11['partner_id']
                query = f"""INSERT INTO account_asset (id,
                                                        name, 
                                                        code,  
                                                        active,                                                    
                                                        purchase_value,
                                                        depreciation_base
                                                        company_currency_id, 
                                                        company_id, 
                                                        profile_id,                                                                  
                                                        date_start, 
                                                        state,
                                                        partner_id, 
                                                        method,
                                                        method_number, 
                                                        method_period,                                                                                                            
                                                        method_progress_factor,
                                                        method_time, 
                                                        prorata,
                                                        salvage_value)                              
                                                        VALUES ({asset11['id']}, 
                                                        '{asset11['name']}',
                                                        '{asset11['code']}', 
                                                        {asset11['active']},
                                                        {asset11['value']},
                                                        {asset11['value']},
                                                        2,
                                                        {asset11['company_id']},
                                                        {asset11['category_id']},
                                                        '{asset11['date']}',
                                                        '{asset11['state']}',
                                                        {asset11['partner_id']},
                                                        '{asset11['method']}',
                                                        {asset11['method_number']},
                                                        {asset11['method_period']},                                                                                                         
                                                        {asset11['method_progress_factor']},
                                                        '{asset11['method_time']}',
                                                        {asset11['prorata']},
                                                        {asset11['salvage_value']}
                                                        )"""
                cursor14.execute(query)
        self.sync_depreciation_lines(cursor11, cursor14, conn14)
        conn14.commit()

    #TODO: Terminado
    def sync_depreciation_lines(self, cursor11, cursor14, conn14):
        query11 = f"""SELECT * FROM account_asset_depreciation_line"""
        query14 = f"""SELECT * FROM account_asset_line"""
        cursor11.execute(query11)
        cursor14.execute(query14)
        depreciation11 = cursor11.fetchall()
        depreciation14 = cursor14.fetchall()

        for depre11 in depreciation11:
            exist = False
            for depre14 in depreciation14:
                if depre11['id'] == depre14['id']:
                    exist = True
                    if depre11['name'] != depre14['name']:
                        query = f"""UPDATE account_asset_line SET name = '{depre11['name']}', 
                                                asset_id = {depre11['asset_id']},                                                                  
                                                amount = {depre11['amount']},
                                                remaining_value = {depre11['remaining_value']},
                                                depreciated_value = {depre11['depreciated_value']},
                                                line_date = '{depre11['depreciation_date']}',
                                                move_check = {depre11['move_check']},
                                                company_id = 1                                                                                            
                                                WHERE  id = {depre11['id']}"""
                        cursor14.execute(query)
                        conn14.commit()
            if not exist:
                print('inserta profile', depre11['id'])
                query = f"""INSERT INTO account_asset_line (id,
                                                name,
                                                asset_id,                                                                 
                                                amount,
                                                remaining_value, 
                                                depreciated_value, 
                                                line_date,
                                                move_check, 
                                                company_id)  
                                                VALUES ({depre11['id']},
                                                '{depre11['name']}',
                                                {depre11['asset_id']},
                                                {depre11['amount']},
                                                {depre11['remaining_value']},
                                                {depre11['depreciated_value']},
                                                '{depre11['depreciation_date']}',
                                                {depre11['move_check']},
                                                1
                                                )"""
                cursor14.execute(query)
                conn14.commit()

    #TODO: Terminado
    def check_account_category(self, cursor11, cursor14, cid, conn14):
        query11 = f"""SELECT * FROM account_asset_category WHERE id = {cid}"""
        query14 = f"""SELECT * FROM account_asset_profile WHERE id = {cid}"""
        cursor11.execute(query11)
        cursor14.execute(query14)
        category11 = cursor11.fetchone()
        profile14 = cursor14.fetchone()

        if category11 and profile14:
            if category11['id'] == profile14['id']:
                if category11['name'] != profile14['name']:
                    print('actualiza profile', category11['id'])
                    query = f"""UPDATE account_asset_profile SET name = '{category11['name']}', 
                                    active = {category11['active']},                                                                  
                                    account_asset_id = {category11['account_asset_id']},
                                    account_depreciation_id = {category11['account_depreciation_id']},
                                    account_expense_depreciation_id = {category11['account_depreciation_expense_id']},
                                    journal_id = {category11['journal_id']},
                                    company_id = {category11['company_id']},
                                    method = '{category11['method']}',
                                    method_number = {category11['method_number']},
                                    
                                    method_progress_factor = {category11['method_progress_factor']},
                                    method_time = '{category11['method_time']}',
                                    prorata = {category11['prorata']},
                                    open_asset = {category11['open_asset']}
                                    WHERE  id = {category11['id']}"""
                    cursor14.execute(query)
                    conn14.commit()
        else:
            print('inserta profile', category11['id'])
            query = f"""INSERT INTO account_asset_profile (id,
                                                        name,
                                                        active,                                                                                            
                                                        account_asset_id,
                                                        account_depreciation_id, 
                                                        account_expense_depreciation_id, 
                                                        journal_id,
                                                        company_id, 
                                                        method,
                                                        method_number, 
                                                         
                                                        method_progress_factor, 
                                                        method_time,
                                                        prorata,
                                                        open_asset)  
                                                        VALUES ({category11['id']},
                                                        '{category11['name']}',
                                                        {category11['active']},                                                       
                                                        {category11['account_asset_id']},
                                                        {category11['account_depreciation_id']},
                                                        {category11['account_depreciation_expense_id']},
                                                        {category11['journal_id']},
                                                        {category11['company_id']},
                                                        '{category11['method']}',
                                                        {category11['method_number']},
                                                        
                                                        {category11['method_progress_factor']},
                                                        '{category11['method_time']}',
                                                        {category11['prorata']},
                                                        {category11['open_asset']}
                                                        )"""
            cursor14.execute(query)
            conn14.commit()
