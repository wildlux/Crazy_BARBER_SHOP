#!/usr/bin/env python
import os
import sys
import django
from django.utils import timezone
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barber_shop.settings')
django.setup()

from appointments.models import Cliente, Barbiere, Servizio, Appuntamento
from django.contrib.auth.models import User

# Dati di esempio per clienti
clienti_data = [
    {'nome': 'Mario Rossi', 'email': 'mario.rossi@example.com', 'telefono': '+39 333 123 4567'},
    {'nome': 'Luca Bianchi', 'email': 'luca.bianchi@example.com', 'telefono': '02 9876543'},
    {'nome': 'Giulia Verdi', 'email': 'giulia.verdi@example.com', 'telefono': '+39 345 678 9012'},
    {'nome': 'Francesco Neri', 'email': 'francesco.neri@example.com', 'telefono': '06 555 1234'},
    {'nome': 'Sara Gialli', 'email': 'sara.gialli@example.com', 'telefono': '+39 328 456 7890'},
]

# Dati di esempio per servizi
servizi_data = [
    {
        'nome': 'Taglio Capelli',
        'descrizione': 'Taglio professionale dei capelli con styling finale',
        'durata_minuti': 30,
        'prezzo': 20.00
    },
    {
        'nome': 'Shampoo',
        'descrizione': 'Lavaggio e trattamento shampoo con massaggio',
        'durata_minuti': 15,
        'prezzo': 10.00
    },
    {
        'nome': 'Taglio + Shampoo',
        'descrizione': 'Combinazione di taglio e shampoo per un servizio completo',
        'durata_minuti': 45,
        'prezzo': 25.00
    },
    {
        'nome': 'Barba',
        'descrizione': 'Modellatura e rifinitura della barba',
        'durata_minuti': 20,
        'prezzo': 15.00
    },
    {
        'nome': 'Taglio + Barba',
        'descrizione': 'Taglio capelli e modellatura barba',
        'durata_minuti': 50,
        'prezzo': 30.00
    },
    {
        'nome': 'Pacchetto Completo',
        'descrizione': 'Taglio, shampoo, barba e styling finale',
        'durata_minuti': 75,
        'prezzo': 45.00
    }
]

# Crea servizi
for data in servizi_data:
    servizio, created = Servizio.objects.get_or_create(
        nome=data['nome'],
        defaults=data
    )
    if created:
        print(f"Aggiunto servizio: {servizio.nome}")
    else:
        print(f"Servizio già esistente: {servizio.nome}")

# Dati di esempio per barbieri
barbieri_data = [
    {'nome': 'Giuseppe Barbiere', 'specialita': 'Tagli classici e moderni', 'foto': None, 'attivo': True},
    {'nome': 'Antonio Stilista', 'specialita': 'Styling e acconciature', 'foto': None, 'attivo': True},
    {'nome': 'Marco Esperto', 'specialita': 'Barbe e tagli tradizionali', 'foto': None, 'attivo': True},
    {'nome': 'Davide Giovane', 'specialita': 'Tagli alla moda per giovani', 'foto': None, 'attivo': True},
]

# Crea utenti e clienti
for cliente_data in clienti_data:
    # Crea utente se non esiste
    user, user_created = User.objects.get_or_create(
        username=cliente_data['email'],
        defaults={
            'email': cliente_data['email'],
            'first_name': cliente_data['nome'].split()[0],
            'last_name': ' '.join(cliente_data['nome'].split()[1:]) if len(cliente_data['nome'].split()) > 1 else '',
        }
    )
    if user_created:
        user.set_password('password123')  # Password di default per test
        user.save()
        print(f"Creato utente: {user.username}")
    
    # Crea cliente
    cliente, cliente_created = Cliente.objects.get_or_create(
        user=user,
        defaults=cliente_data
    )
    if cliente_created:
        print(f"Aggiunto cliente: {cliente.nome}")

# Crea barbieri
for barbiere_data in barbieri_data:
    barbiere, created = Barbiere.objects.get_or_create(
        nome=barbiere_data['nome'],
        defaults=barbiere_data
    )
    if created:
        print(f"Aggiunto barbiere: {barbiere.nome}")

# Mappatura nome barbiere -> foto
photo_mapping = {
    'Giuseppe Barbiere': 'barber_shop/foto/giuseppe_il_barbiere.png',
    'Antonio Stilista': 'barber_shop/foto/Salvone_il_barbiere.png',
    'Marco Esperto': 'barber_shop/foto/marco.png',
    'Davide Giovane': 'barber_shop/foto/davide_giovane.png',
}

# Aggiorna foto per barbieri esistenti
for barbiere in Barbiere.objects.all():
    if barbiere.nome in photo_mapping:
        foto_path = photo_mapping[barbiere.nome]
        if os.path.exists(foto_path):
            with open(foto_path, 'rb') as f:
                barbiere.foto.save(os.path.basename(foto_path), f, save=True)
                print(f"Aggiornata foto per {barbiere.nome}: {foto_path}")
        else:
            print(f"Foto non trovata per {barbiere.nome}: {foto_path}")
    else:
        print(f"Nessuna mappatura foto per {barbiere.nome}")

# Crea alcuni appuntamenti di esempio (se ci sono servizi)
servizi = list(Servizio.objects.all())
barbieri = list(Barbiere.objects.all())
clienti = list(Cliente.objects.all())

if servizi and barbieri and clienti:
    appuntamenti_data = [
        {'cliente': clienti[0], 'barbiere': barbieri[0], 'servizio': servizi[0], 'data_ora': timezone.now() + timedelta(days=1, hours=10), 'stato': 'confermato'},
        {'cliente': clienti[1], 'barbiere': barbieri[1], 'servizio': servizi[1], 'data_ora': timezone.now() + timedelta(days=2, hours=14), 'stato': 'confermato'},
        {'cliente': clienti[2], 'barbiere': barbieri[2], 'servizio': servizi[2], 'data_ora': timezone.now() + timedelta(days=3, hours=9), 'stato': 'in_attesa'},
    ]
    
    for app_data in appuntamenti_data:
        appuntamento, created = Appuntamento.objects.get_or_create(
            cliente=app_data['cliente'],
            barbiere=app_data['barbiere'],
            servizio=app_data['servizio'],
            data_ora=app_data['data_ora'],
            defaults={'stato': app_data['stato']}
        )
        if created:
            print(f"Aggiunto appuntamento: {appuntamento}")

print(f"\nRiepilogo finale:")
print(f"Clienti: {Cliente.objects.count()}")
print(f"Barbieri: {Barbiere.objects.count()}")
print(f"Servizi: {Servizio.objects.count()}")
print(f"Appuntamenti: {Appuntamento.objects.count()}")
print(f"Utenti: {User.objects.count()}")