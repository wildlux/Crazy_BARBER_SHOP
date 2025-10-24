from django.contrib import admin
from .models import Cliente, Barbiere, Servizio, Appuntamento


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'telefono', 'data_registrazione']
    search_fields = ['nome', 'email']
    list_filter = ['data_registrazione']


@admin.register(Barbiere)
class BarbiereAdmin(admin.ModelAdmin):
    list_display = ['nome', 'specialita', 'attivo']
    list_filter = ['attivo']
    search_fields = ['nome']


@admin.register(Servizio)
class ServizioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'prezzo', 'durata_minuti']
    list_filter = ['prezzo']
    search_fields = ['nome']


@admin.register(Appuntamento)
class AppuntamentoAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'barbiere', 'servizio', 'data_ora', 'stato', 'creato_il']
    list_filter = ['stato', 'barbiere', 'data_ora']
    search_fields = ['cliente__nome', 'cliente__email']
    date_hierarchy = 'data_ora'
