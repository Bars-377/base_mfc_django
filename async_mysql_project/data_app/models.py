from django.db import models

class Services(models.Model):
    id = models.BigAutoField(primary_key=True)  # Поле id как первичный ключ
    id_id = models.TextField(verbose_name='ID', default='Unknown ID')
    name = models.TextField(verbose_name='Service Name', default='Unknown Service')
    status = models.TextField(verbose_name='Status', default='Unknown Status')
    way = models.TextField(verbose_name='Way', default='Unknown Way')
    initiator = models.TextField(verbose_name='Initiator', default='Unknown Initiator')
    KTSSR = models.TextField(verbose_name='KTSSR', default='Unknown KTSSR')
    KOSGU = models.TextField(verbose_name='KOSGU', default='Unknown KOSGU')
    DopFC = models.TextField(verbose_name='DopFC', default='Unknown DopFC')
    NMCC = models.TextField(verbose_name='NMCC', default='Unknown NMCC')
    saving = models.TextField(verbose_name='Saving', default='Unknown Saving')
    counterparty = models.TextField(verbose_name='Counterparty', default='Unknown Counterparty')
    registration_number = models.TextField(verbose_name='Registration Number', default='Unknown Registration Number')
    contract_number = models.TextField(verbose_name='Contract Number', default='Unknown Contract Number')
    contract_date = models.TextField(verbose_name='Contract Date', default='Unknown Contract Date')
    end_date = models.TextField(verbose_name='End Date', default='Unknown End Date')
    contract_price = models.TextField(verbose_name='Contract Price', default='Unknown Contract Price')
    execution_contract_plan = models.TextField(verbose_name='Execution Contract Plan', default='Unknown Plan')
    january_one = models.TextField(verbose_name='January One', default='Unknown January One')
    february = models.TextField(verbose_name='February', default='Unknown February')
    march = models.TextField(verbose_name='March', default='Unknown March')
    april = models.TextField(verbose_name='April', default='Unknown April')
    may = models.TextField(verbose_name='May', default='Unknown May')
    june = models.TextField(verbose_name='June', default='Unknown June')
    july = models.TextField(verbose_name='July', default='Unknown July')
    august = models.TextField(verbose_name='August', default='Unknown August')
    september = models.TextField(verbose_name='September', default='Unknown September')
    october = models.TextField(verbose_name='October', default='Unknown October')
    november = models.TextField(verbose_name='November', default='Unknown November')
    december = models.TextField(verbose_name='December', default='Unknown December')
    january_two = models.TextField(verbose_name='January Two', default='Unknown January Two')
    execution_contract_fact = models.TextField(verbose_name='Execution Contract Fact', default='Unknown Fact')
    date_january_one = models.TextField(verbose_name='Date January One', default='Unknown Date')
    sum_january_one = models.TextField(verbose_name='Sum January One', default='Unknown Sum')
    date_february = models.TextField(verbose_name='Date February', default='Unknown Date')
    sum_february = models.TextField(verbose_name='Sum February', default='Unknown Sum')
    date_march = models.TextField(verbose_name='Date March', default='Unknown Date')
    sum_march = models.TextField(verbose_name='Sum March', default='Unknown Sum')
    date_april = models.TextField(verbose_name='Date April', default='Unknown Date')
    sum_april = models.TextField(verbose_name='Sum April', default='Unknown Sum')
    date_may = models.TextField(verbose_name='Date May', default='Unknown Date')
    sum_may = models.TextField(verbose_name='Sum May', default='Unknown Sum')
    date_june = models.TextField(verbose_name='Date June', default='Unknown Date')
    sum_june = models.TextField(verbose_name='Sum June', default='Unknown Sum')
    date_july = models.TextField(verbose_name='Date July', default='Unknown Date')
    sum_july = models.TextField(verbose_name='Sum July', default='Unknown Sum')
    date_august = models.TextField(verbose_name='Date August', default='Unknown Date')
    sum_august = models.TextField(verbose_name='Sum August', default='Unknown Sum')
    date_september = models.TextField(verbose_name='Date September', default='Unknown Date')
    sum_september = models.TextField(verbose_name='Sum September', default='Unknown Sum')
    date_october = models.TextField(verbose_name='Date October', default='Unknown Date')
    sum_october = models.TextField(verbose_name='Sum October', default='Unknown Sum')
    date_november = models.TextField(verbose_name='Date November', default='Unknown Date')
    sum_november = models.TextField(verbose_name='Sum November', default='Unknown Sum')
    date_december = models.TextField(verbose_name='Date December', default='Unknown Date')
    sum_december = models.TextField(verbose_name='Sum December', default='Unknown Sum')
    date_january_two = models.TextField(verbose_name='Date January Two', default='Unknown Date')
    sum_january_two = models.TextField(verbose_name='Sum January Two', default='Unknown Sum')
    execution = models.TextField(verbose_name='Execution', default='Unknown Execution')
    contract_balance = models.TextField(verbose_name='Contract Balance', default='Unknown Balance')
    color = models.TextField(verbose_name='Color', default='Unknown Color')

    class Meta:
        db_table = 'services_base'  # Указываем имя таблицы в базе данных
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.name

class ServicesTwo(models.Model):
    id = models.BigAutoField(primary_key=True)  # Поле id как первичный ключ
    id_id = models.TextField(verbose_name='ID', default='Unknown ID')
    KOSGU = models.TextField(verbose_name='KOSGU', default='Unknown KOSGU')
    DopFC = models.TextField(verbose_name='DopFC', default='Unknown DopFC')
    budget_planned = models.TextField(verbose_name='Budget Planned', default='Unknown Budget Planned')
    off_budget_planned = models.TextField(verbose_name='Off Budget Planned', default='Unknown Off Budget Planned')
    budget_concluded = models.TextField(verbose_name='Budget Concluded', default='Unknown Budget Concluded')
    off_budget_concluded = models.TextField(verbose_name='Off Budget Concluded', default='Unknown Off Budget Concluded')
    budget_remainder = models.TextField(verbose_name='Budget Remainder', default='Unknown Budget Remainder')
    off_budget_remainder = models.TextField(verbose_name='Off Budget Remainder', default='Unknown Off Budget Remainder')
    color = models.TextField(verbose_name='Color', default='Unknown Color')

    class Meta:
        db_table = 'services_two'  # Указываем имя таблицы в базе данных
        verbose_name = 'Service Two'
        verbose_name_plural = 'Services Two'

    def __str__(self):
        return self.id_id

class ServicesVault(models.Model):
    id = models.BigAutoField(primary_key=True)  # Поле id как первичный ключ
    id_id = models.TextField(verbose_name='ID', default='Unknown ID')
    name = models.TextField(verbose_name='Name', default='Unknown Name')
    KOSGU = models.TextField(verbose_name='KOSGU', default='Unknown KOSGU')
    DopFC = models.TextField(verbose_name='DopFC', default='Unknown DopFC')
    budget_limit = models.TextField(verbose_name='Budget Limit', default='Unknown Budget Limit')
    off_budget_limit = models.TextField(verbose_name='Off Budget Limit', default='Unknown Off Budget Limit')
    budget_planned = models.TextField(verbose_name='Budget Planned', default='Unknown Budget Planned')
    off_budget_planned = models.TextField(verbose_name='Off Budget Planned', default='Unknown Off Budget Planned')
    budget_bargaining = models.TextField(verbose_name='Budget Bargaining', default='Unknown Budget Bargaining')
    off_budget_bargaining = models.TextField(verbose_name='Off Budget Bargaining', default='Unknown Off Budget Bargaining')
    budget_concluded = models.TextField(verbose_name='Budget Concluded', default='Unknown Budget Concluded')
    off_budget_concluded = models.TextField(verbose_name='Off Budget Concluded', default='Unknown Off Budget Concluded')
    budget_completed = models.TextField(verbose_name='Budget Completed', default='Unknown Budget Completed')
    off_budget_completed = models.TextField(verbose_name='Off Budget Completed', default='Unknown Off Budget Completed')
    budget_execution = models.TextField(verbose_name='Budget Execution', default='Unknown Budget Execution')
    off_budget_execution = models.TextField(verbose_name='Off Budget Execution', default='Unknown Off Budget Execution')
    budget_remainder = models.TextField(verbose_name='Budget Remainder', default='Unknown Budget Remainder')
    off_budget_remainder = models.TextField(verbose_name='Off Budget Remainder', default='Unknown Off Budget Remainder')
    budget_plans = models.TextField(verbose_name='Budget Plans', default='Unknown Budget Plans')
    off_budget_plans = models.TextField(verbose_name='Off Budget Plans', default='Unknown Off Budget Plans')
    color = models.TextField(verbose_name='Color', default='Unknown Color')

    class Meta:
        db_table = 'services_vault'  # Указываем имя таблицы в базе данных
        verbose_name = 'Service Vault'
        verbose_name_plural = 'Service Vaults'

    def __str__(self):
        return self.name
