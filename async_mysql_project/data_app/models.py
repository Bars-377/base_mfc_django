# from django.db import models

# class DataTable(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

from django.db import models

class DataTable(models.Model):
    id_id = models.CharField(max_length=500, verbose_name='ID')
    name = models.CharField(max_length=500, verbose_name='Name')
    snils = models.CharField(max_length=500, verbose_name='SNILS')
    location = models.CharField(max_length=500, verbose_name='Location')
    address_p = models.CharField(max_length=500, verbose_name='Address P')
    address = models.CharField(max_length=500, verbose_name='Address')
    benefit = models.CharField(max_length=500, verbose_name='Benefit')
    number = models.CharField(max_length=500, verbose_name='Number')
    year = models.CharField(max_length=500, verbose_name='Year')
    cost = models.CharField(max_length=500, verbose_name='Cost')
    certificate = models.CharField(max_length=500, verbose_name='Certificate')
    date_number_get = models.CharField(max_length=500, verbose_name='Date Number Get')
    date_number_cancellation = models.CharField(max_length=500, verbose_name='Date Number Cancellation')
    date_number_no_one = models.CharField(max_length=500, verbose_name='Date Number No One')
    date_number_no_two = models.CharField(max_length=500, verbose_name='Date Number No Two')
    certificate_no = models.CharField(max_length=500, verbose_name='Certificate No')
    reason = models.CharField(max_length=500, verbose_name='Reason')
    track = models.CharField(max_length=500, verbose_name='Track')
    date_post = models.CharField(max_length=500, verbose_name='Date Post')
    comment = models.CharField(max_length=500, verbose_name='Comment')
    color = models.CharField(max_length=500, null=True, blank=True, verbose_name='Color')

    class Meta:
        db_table = 'services'  # Указываем имя таблицы в базе данных
        verbose_name = 'Data Table'
        verbose_name_plural = 'Data Tables'

    def __str__(self):
        return self.name
