#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barber_shop.settings')
django.setup()

from appointments.models import Barbiere

# Mappatura nome barbiere -> foto
photo_mapping = {
    'Giuseppe Barbiere': 'barber_shop/foto/giuseppe_il_barbiere.png',
    'Antonio Stilista': 'barber_shop/foto/Salvone_il_barbiere.png',
    'Marco Esperto': 'barber_shop/foto/marco.png',
    'Davide Giovane': 'barber_shop/foto/davide_giovane.png',
    'Giovanni di San vito lo capo': 'barber_shop/foto/sanvitolocaèo.png',
    'Salvone il baribiere pazzo': 'barber_shop/foto/Salvone_il_barbiere.png',
    'Paolo il carnefice': 'barber_shop/foto/paolo_il_carnefice.png',
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

print(f"Barbieri totali: {Barbiere.objects.count()}")