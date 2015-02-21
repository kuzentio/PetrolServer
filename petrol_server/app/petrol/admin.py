from django.contrib import admin
from petrol_server.app.petrol import models


admin.site.register(models.User)
admin.site.register(models.Card)
admin.site.register(models.Company)
admin.site.register(models.CardTransaction)


class UploadFile(admin.ModelAdmin):
    change_form_template = 'add_transactions.html'
