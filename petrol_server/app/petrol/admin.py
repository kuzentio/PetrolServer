from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from petrol_server.app.petrol import models


class TransactionResource(resources.ModelResource):


    class Meta:
        model = models.CardTransaction
        fields = ('Made_at', 'card', 'azs', 'fuel', 'volume', 'price')

class TransactionsAdmin(ImportExportModelAdmin):
    resource_class = TransactionResource


admin.site.register(models.User)
admin.site.register(models.Card)
admin.site.register(models.Company)
admin.site.register(models.CardTransaction, TransactionsAdmin)

