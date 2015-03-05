from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from petrol_server.app.petrol import models
from petrol_server.app.petrol.resources import TransactionResource


class TransactionsAdmin(ImportExportModelAdmin):
    resource_class = TransactionResource


class CompanyAdmin(admin.ModelAdmin):
    fields = ('title', 'users')


admin.site.register(models.User)
admin.site.register(models.Card)
admin.site.register(models.Company, CompanyAdmin)
admin.site.register(models.CardTransaction, TransactionsAdmin)

