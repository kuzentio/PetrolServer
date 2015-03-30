# -*- coding: utf-8 -*-
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from petrol_server.app.petrol import models
from petrol_server.app.petrol.resources import TransactionResource




class CardTransactionsAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        queryset = super(CardTransactionsAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return queryset.filter(is_approved=False)

        return queryset


    def get_actions(self, request):
        actions = super(CardTransactionsAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            del actions['make_not_approved']

        return actions

    def make_approved(self, request, queryset):
        queryset.update(is_approved=True)

    def make_not_approved(self, request, queryset):
        queryset.update(is_approved=False)

    actions = ['make_approved', 'make_not_approved']
    list_display = ['made_at', 'is_approved', 'is_no_need_attention', 'card_holder']
    ordering = ['made_at',]
    resource_class = TransactionResource

    make_approved.short_description = u'Провести эти транзакции'
    make_not_approved.short_description = u'Не проводить эти транзакции'



admin.site.register(models.User)
admin.site.register(models.Company)
admin.site.register(models.Card)
admin.site.register(models.CardTransaction, CardTransactionsAdmin)
admin.site.register(models.Cardholder)

