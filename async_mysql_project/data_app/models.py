from django.db import models

class Services_backup_one(models.Model):
    id = models.BigAutoField(primary_key=True)  # Поле id как первичный ключ
    id_id = models.TextField(verbose_name='ID', default='')
    name = models.TextField(verbose_name='Service Name', default='')
    status = models.TextField(verbose_name='Status', default='')
    way = models.TextField(verbose_name='Way', default='')
    initiator = models.TextField(verbose_name='Initiator', default='')
    KTSSR = models.TextField(verbose_name='KTSSR', default='')
    KOSGU = models.TextField(verbose_name='KOSGU', default='')
    DopFC = models.TextField(verbose_name='DopFC', default='')
    NMCC = models.TextField(verbose_name='NMCC', default='')
    saving = models.TextField(verbose_name='Saving', default='')
    counterparty = models.TextField(verbose_name='Counterparty', default='')
    registration_number = models.TextField(verbose_name='Registration Number', default='')
    contract_number = models.TextField(verbose_name='Contract Number', default='')
    contract_date = models.TextField(verbose_name='Contract Date', default='')
    end_date = models.TextField(verbose_name='End Date', default='')
    contract_price = models.TextField(verbose_name='Contract Price', default='')
    execution_contract_plan = models.TextField(verbose_name='Execution Contract Plan', default='')
    remainder_old_year = models.TextField(verbose_name='Remainder Old Year', default='')
    january_one = models.TextField(verbose_name='January One', default='')
    february = models.TextField(verbose_name='February', default='')
    march = models.TextField(verbose_name='March', default='')
    april = models.TextField(verbose_name='April', default='')
    may = models.TextField(verbose_name='May', default='')
    june = models.TextField(verbose_name='June', default='')
    july = models.TextField(verbose_name='July', default='')
    august = models.TextField(verbose_name='August', default='')
    september = models.TextField(verbose_name='September', default='')
    october = models.TextField(verbose_name='October', default='')
    november = models.TextField(verbose_name='November', default='')
    december = models.TextField(verbose_name='December', default='')
    january_two = models.TextField(verbose_name='January Two', default='')
    execution_contract_fact = models.TextField(verbose_name='Execution Contract Fact', default='')
    paid_last_year = models.TextField(verbose_name='Paid Last Year', default='')
    date_january_one = models.TextField(verbose_name='Date January One', default='')
    sum_january_one = models.TextField(verbose_name='Sum January One', default='')
    date_february = models.TextField(verbose_name='Date February', default='')
    sum_february = models.TextField(verbose_name='Sum February', default='')
    date_march = models.TextField(verbose_name='Date March', default='')
    sum_march = models.TextField(verbose_name='Sum March', default='')
    date_april = models.TextField(verbose_name='Date April', default='')
    sum_april = models.TextField(verbose_name='Sum April', default='')
    date_may = models.TextField(verbose_name='Date May', default='')
    sum_may = models.TextField(verbose_name='Sum May', default='')
    date_june = models.TextField(verbose_name='Date June', default='')
    sum_june = models.TextField(verbose_name='Sum June', default='')
    date_july = models.TextField(verbose_name='Date July', default='')
    sum_july = models.TextField(verbose_name='Sum July', default='')
    date_august = models.TextField(verbose_name='Date August', default='')
    sum_august = models.TextField(verbose_name='Sum August', default='')
    date_september = models.TextField(verbose_name='Date September', default='')
    sum_september = models.TextField(verbose_name='Sum September', default='')
    date_october = models.TextField(verbose_name='Date October', default='')
    sum_october = models.TextField(verbose_name='Sum October', default='')
    date_november = models.TextField(verbose_name='Date November', default='')
    sum_november = models.TextField(verbose_name='Sum November', default='')
    date_december = models.TextField(verbose_name='Date December', default='')
    sum_december = models.TextField(verbose_name='Sum December', default='')
    date_january_two = models.TextField(verbose_name='Date January Two', default='')
    sum_january_two = models.TextField(verbose_name='Sum January Two', default='')
    execution = models.TextField(verbose_name='Execution', default='')
    contract_balance = models.TextField(verbose_name='Contract Balance', default='')
    color = models.TextField(verbose_name='Color', default='')

    class Meta:
        db_table = 'services_backup_one'  # Указываем имя таблицы в базе данных
        verbose_name = 'Service backup one'
        verbose_name_plural = 'Services backup one'

    def __str__(self):
        return self.name

class Services_backup_two(models.Model):
    id = models.BigAutoField(primary_key=True)  # Поле id как первичный ключ
    id_id = models.TextField(verbose_name='ID', default='')
    name = models.TextField(verbose_name='Service Name', default='')
    status = models.TextField(verbose_name='Status', default='')
    way = models.TextField(verbose_name='Way', default='')
    initiator = models.TextField(verbose_name='Initiator', default='')
    KTSSR = models.TextField(verbose_name='KTSSR', default='')
    KOSGU = models.TextField(verbose_name='KOSGU', default='')
    DopFC = models.TextField(verbose_name='DopFC', default='')
    NMCC = models.TextField(verbose_name='NMCC', default='')
    saving = models.TextField(verbose_name='Saving', default='')
    counterparty = models.TextField(verbose_name='Counterparty', default='')
    registration_number = models.TextField(verbose_name='Registration Number', default='')
    contract_number = models.TextField(verbose_name='Contract Number', default='')
    contract_date = models.TextField(verbose_name='Contract Date', default='')
    end_date = models.TextField(verbose_name='End Date', default='')
    contract_price = models.TextField(verbose_name='Contract Price', default='')
    execution_contract_plan = models.TextField(verbose_name='Execution Contract Plan', default='')
    remainder_old_year = models.TextField(verbose_name='Remainder Old Year', default='')
    january_one = models.TextField(verbose_name='January One', default='')
    february = models.TextField(verbose_name='February', default='')
    march = models.TextField(verbose_name='March', default='')
    april = models.TextField(verbose_name='April', default='')
    may = models.TextField(verbose_name='May', default='')
    june = models.TextField(verbose_name='June', default='')
    july = models.TextField(verbose_name='July', default='')
    august = models.TextField(verbose_name='August', default='')
    september = models.TextField(verbose_name='September', default='')
    october = models.TextField(verbose_name='October', default='')
    november = models.TextField(verbose_name='November', default='')
    december = models.TextField(verbose_name='December', default='')
    january_two = models.TextField(verbose_name='January Two', default='')
    execution_contract_fact = models.TextField(verbose_name='Execution Contract Fact', default='')
    paid_last_year = models.TextField(verbose_name='Paid Last Year', default='')
    date_january_one = models.TextField(verbose_name='Date January One', default='')
    sum_january_one = models.TextField(verbose_name='Sum January One', default='')
    date_february = models.TextField(verbose_name='Date February', default='')
    sum_february = models.TextField(verbose_name='Sum February', default='')
    date_march = models.TextField(verbose_name='Date March', default='')
    sum_march = models.TextField(verbose_name='Sum March', default='')
    date_april = models.TextField(verbose_name='Date April', default='')
    sum_april = models.TextField(verbose_name='Sum April', default='')
    date_may = models.TextField(verbose_name='Date May', default='')
    sum_may = models.TextField(verbose_name='Sum May', default='')
    date_june = models.TextField(verbose_name='Date June', default='')
    sum_june = models.TextField(verbose_name='Sum June', default='')
    date_july = models.TextField(verbose_name='Date July', default='')
    sum_july = models.TextField(verbose_name='Sum July', default='')
    date_august = models.TextField(verbose_name='Date August', default='')
    sum_august = models.TextField(verbose_name='Sum August', default='')
    date_september = models.TextField(verbose_name='Date September', default='')
    sum_september = models.TextField(verbose_name='Sum September', default='')
    date_october = models.TextField(verbose_name='Date October', default='')
    sum_october = models.TextField(verbose_name='Sum October', default='')
    date_november = models.TextField(verbose_name='Date November', default='')
    sum_november = models.TextField(verbose_name='Sum November', default='')
    date_december = models.TextField(verbose_name='Date December', default='')
    sum_december = models.TextField(verbose_name='Sum December', default='')
    date_january_two = models.TextField(verbose_name='Date January Two', default='')
    sum_january_two = models.TextField(verbose_name='Sum January Two', default='')
    execution = models.TextField(verbose_name='Execution', default='')
    contract_balance = models.TextField(verbose_name='Contract Balance', default='')
    color = models.TextField(verbose_name='Color', default='')

    class Meta:
        db_table = 'services_backup_two'  # Указываем имя таблицы в базе данных
        verbose_name = 'Service backup two'
        verbose_name_plural = 'Services backup two'

    def __str__(self):
        return self.name

class Services(models.Model):
    id = models.BigAutoField(primary_key=True)  # Поле id как первичный ключ
    id_id = models.TextField(verbose_name='ID', default='')
    name = models.TextField(verbose_name='Service Name', default='')
    status = models.TextField(verbose_name='Status', default='')
    way = models.TextField(verbose_name='Way', default='')
    initiator = models.TextField(verbose_name='Initiator', default='')
    KTSSR = models.TextField(verbose_name='KTSSR', default='')
    KOSGU = models.TextField(verbose_name='KOSGU', default='')
    DopFC = models.TextField(verbose_name='DopFC', default='')
    NMCC = models.TextField(verbose_name='NMCC', default='')
    saving = models.TextField(verbose_name='Saving', default='')
    counterparty = models.TextField(verbose_name='Counterparty', default='')
    registration_number = models.TextField(verbose_name='Registration Number', default='')
    contract_number = models.TextField(verbose_name='Contract Number', default='')
    contract_date = models.TextField(verbose_name='Contract Date', default='')
    end_date = models.TextField(verbose_name='End Date', default='')
    contract_price = models.TextField(verbose_name='Contract Price', default='')
    execution_contract_plan = models.TextField(verbose_name='Execution Contract Plan', default='')
    remainder_old_year = models.TextField(verbose_name='Remainder Old Year', default='')
    january_one = models.TextField(verbose_name='January One', default='')
    february = models.TextField(verbose_name='February', default='')
    march = models.TextField(verbose_name='March', default='')
    april = models.TextField(verbose_name='April', default='')
    may = models.TextField(verbose_name='May', default='')
    june = models.TextField(verbose_name='June', default='')
    july = models.TextField(verbose_name='July', default='')
    august = models.TextField(verbose_name='August', default='')
    september = models.TextField(verbose_name='September', default='')
    october = models.TextField(verbose_name='October', default='')
    november = models.TextField(verbose_name='November', default='')
    december = models.TextField(verbose_name='December', default='')
    january_two = models.TextField(verbose_name='January Two', default='')
    execution_contract_fact = models.TextField(verbose_name='Execution Contract Fact', default='')
    paid_last_year = models.TextField(verbose_name='Paid Last Year', default='')
    date_january_one = models.TextField(verbose_name='Date January One', default='')
    sum_january_one = models.TextField(verbose_name='Sum January One', default='')
    date_february = models.TextField(verbose_name='Date February', default='')
    sum_february = models.TextField(verbose_name='Sum February', default='')
    date_march = models.TextField(verbose_name='Date March', default='')
    sum_march = models.TextField(verbose_name='Sum March', default='')
    date_april = models.TextField(verbose_name='Date April', default='')
    sum_april = models.TextField(verbose_name='Sum April', default='')
    date_may = models.TextField(verbose_name='Date May', default='')
    sum_may = models.TextField(verbose_name='Sum May', default='')
    date_june = models.TextField(verbose_name='Date June', default='')
    sum_june = models.TextField(verbose_name='Sum June', default='')
    date_july = models.TextField(verbose_name='Date July', default='')
    sum_july = models.TextField(verbose_name='Sum July', default='')
    date_august = models.TextField(verbose_name='Date August', default='')
    sum_august = models.TextField(verbose_name='Sum August', default='')
    date_september = models.TextField(verbose_name='Date September', default='')
    sum_september = models.TextField(verbose_name='Sum September', default='')
    date_october = models.TextField(verbose_name='Date October', default='')
    sum_october = models.TextField(verbose_name='Sum October', default='')
    date_november = models.TextField(verbose_name='Date November', default='')
    sum_november = models.TextField(verbose_name='Sum November', default='')
    date_december = models.TextField(verbose_name='Date December', default='')
    sum_december = models.TextField(verbose_name='Sum December', default='')
    date_january_two = models.TextField(verbose_name='Date January Two', default='')
    sum_january_two = models.TextField(verbose_name='Sum January Two', default='')
    execution = models.TextField(verbose_name='Execution', default='')
    contract_balance = models.TextField(verbose_name='Contract Balance', default='')
    color = models.TextField(verbose_name='Color', default='')

    class Meta:
        db_table = 'services'  # Указываем имя таблицы в базе данных
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.name

class Services_Three(models.Model):
    id = models.BigAutoField(primary_key=True)  # Поле id как первичный ключ
    id_id = models.TextField(verbose_name='ID', default='')
    KOSGU = models.TextField(verbose_name='KOSGU', default='')
    DopFC = models.TextField(verbose_name='DopFC', default='')
    budget_planned_old = models.TextField(verbose_name='Budget Planned Old', default='')
    off_budget_planned_old = models.TextField(verbose_name='Off Budget Planned Old', default='')
    budget_planned = models.TextField(verbose_name='Budget Planned', default='')
    off_budget_planned = models.TextField(verbose_name='Off Budget Planned', default='')
    budget_concluded = models.TextField(verbose_name='Budget Concluded', default='')
    off_budget_concluded = models.TextField(verbose_name='Off Budget Concluded', default='')
    budget_remainder = models.TextField(verbose_name='Budget Remainder', default='')
    off_budget_remainder = models.TextField(verbose_name='Off Budget Remainder', default='')
    color = models.TextField(verbose_name='Color', default='')

    class Meta:
        db_table = 'services_three'  # Указываем имя таблицы в базе данных
        verbose_name = 'Service Three'
        verbose_name_plural = 'Services Three'

    def __str__(self):
        return self.id_id

class Services_Two(models.Model):
    id = models.BigAutoField(primary_key=True)  # Поле id как первичный ключ
    id_id = models.TextField(verbose_name='ID', default='')
    name = models.TextField(verbose_name='Name', default='')
    KOSGU = models.TextField(verbose_name='KOSGU', default='')
    DopFC = models.TextField(verbose_name='DopFC', default='')
    budget_limit = models.TextField(verbose_name='Budget Limit', default='')
    off_budget_limit = models.TextField(verbose_name='Off Budget Limit', default='')
    budget_planned = models.TextField(verbose_name='Budget Planned', default='')
    off_budget_planned = models.TextField(verbose_name='Off Budget Planned', default='')
    budget_bargaining = models.TextField(verbose_name='Budget Bargaining', default='')
    off_budget_bargaining = models.TextField(verbose_name='Off Budget Bargaining', default='')
    budget_concluded = models.TextField(verbose_name='Budget Concluded', default='')
    off_budget_concluded = models.TextField(verbose_name='Off Budget Concluded', default='')
    budget_completed = models.TextField(verbose_name='Budget Completed', default='')
    off_budget_completed = models.TextField(verbose_name='Off Budget Completed', default='')
    budget_execution = models.TextField(verbose_name='Budget Execution', default='')
    off_budget_execution = models.TextField(verbose_name='Off Budget Execution', default='')
    budget_remainder = models.TextField(verbose_name='Budget Remainder', default='')
    off_budget_remainder = models.TextField(verbose_name='Off Budget Remainder', default='')
    budget_plans = models.TextField(verbose_name='Budget Plans', default='')
    off_budget_plans = models.TextField(verbose_name='Off Budget Plans', default='')
    color = models.TextField(verbose_name='Color', default='')

    class Meta:
        db_table = 'services_two'  # Указываем имя таблицы в базе данных
        verbose_name = 'Service Two'
        verbose_name_plural = 'Service Two'

    def __str__(self):
        return self.name

class UploadedFile(models.Model):
    file = models.FileField(upload_to="file/")  # Папка "file" внутри MEDIA_ROOT
    uploaded_at = models.DateTimeField(auto_now_add=True)

from datetime import timedelta

def formatted_timestamp(obj):
    # Добавляем 7 часов к timestamp
    adjusted_time = obj + timedelta(hours=7)  # Используйте obj напрямую
    return adjusted_time.strftime('%Y-%m-%d %H:%M')  # Форматируем дату и время

class UserActionLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=150)
    action = models.TextField()

    def __str__(self):
        return f"{formatted_timestamp(self.timestamp)} - {self.username}: {self.action}"