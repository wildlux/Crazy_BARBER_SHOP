#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barber_shop.settings')
django.setup()

from appointments.models import Servizio

# Servizi di esempio
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

# Aggiungi servizi se non esistono
for data in servizi_data:
    servizio, created = Servizio.objects.get_or_create(
        nome=data['nome'],
        defaults=data
    )
    if created:
        print(f"Aggiunto servizio: {servizio.nome}")
    else:
        print(f"Servizio già esistente: {servizio.nome}")

print(f"Totale servizi nel DB: {Servizio.objects.count()}")