from django.db import models

class DataTable(models.Model):
    id = models.BigAutoField(primary_key=True)  # Поле id как первичный ключ
    id_id = models.CharField(max_length=500, verbose_name='id_id', default='Unknown Address')
    name = models.CharField(max_length=500, verbose_name='name', default='Unknown Address')
    snils = models.CharField(max_length=500, verbose_name='snils', default='Unknown Address')
    location = models.CharField(max_length=500, verbose_name='location', default='Unknown Address')
    address_p = models.CharField(max_length=500, verbose_name='address_p', default='Unknown Address')
    address = models.CharField(max_length=500, verbose_name='address', default='Unknown Address')
    benefit = models.CharField(max_length=500, verbose_name='benefit', default='Unknown Address')
    number = models.CharField(max_length=500, verbose_name='number', default='Unknown Address')
    year = models.CharField(max_length=500, verbose_name='year', default='Unknown Address')
    cost = models.CharField(max_length=500, verbose_name='cost', default='Unknown Address')
    certificate = models.CharField(max_length=500, verbose_name='certificate', default='Unknown Address')
    date_number_get = models.CharField(max_length=500, verbose_name='date_number_get', default='Unknown Address')
    date_number_cancellation = models.CharField(max_length=500, verbose_name='date_number_cancellation', default='Unknown Address')
    date_number_no_one = models.CharField(max_length=500, verbose_name='date_number_no_one', default='Unknown Address')
    date_number_no_two = models.CharField(max_length=500, verbose_name='date_number_no_two', default='Unknown Address')
    certificate_no = models.CharField(max_length=500, verbose_name='certificate_no', default='Unknown Address')
    reason = models.CharField(max_length=500, verbose_name='reason', default='Unknown Address')
    track = models.CharField(max_length=500, verbose_name='track', default='Unknown Address')
    date_post = models.CharField(max_length=500, verbose_name='date_post', default='Unknown Address')
    comment = models.CharField(max_length=500, verbose_name='comment', default='Unknown Address')
    color = models.CharField(max_length=500, null=True, blank=True, verbose_name='color', default='Unknown Address')

    class Meta:
        db_table = 'services'  # Указываем имя таблицы в базе данных
        verbose_name = 'Data Table'
        verbose_name_plural = 'Data Tables'

    def __str__(self):
        return self.name
