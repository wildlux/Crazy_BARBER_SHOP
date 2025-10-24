from django.urls import path
from . import views

urlpatterns = [
    # Pagine principali
    path('', views.home, name='home'),
    path('registrazione/', views.registrazione, name='registrazione'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Gestione appuntamenti
    path('appuntamenti/', views.lista_appuntamenti, name='lista_appuntamenti'),
    path('appuntamenti/nuovo/', views.crea_appuntamento, name='crea_appuntamento'),
    path('appuntamenti/<int:appuntamento_id>/modifica/', views.modifica_appuntamento, name='modifica_appuntamento'),
    path('appuntamenti/<int:appuntamento_id>/cancella/', views.cancella_appuntamento, name='cancella_appuntamento'),
    
    # API JSON
    path('api/slot-disponibili/', views.api_slot_disponibili, name='api_slot'),
]