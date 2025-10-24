# ============================================================
# PROGETTO DJANGO COMPLETO - GESTIONALE PARRUCCHIERE
# Pronto da installare e testare!
# ============================================================

"""
📁 STRUTTURA DEL PROGETTO:

barber_shop/
├── manage.py
├── requirements.txt
├── barber_shop/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── appointments/
    ├── __init__.py
    ├── admin.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── migrations/
    └── templates/
        └── appointments/
            ├── base.html
            ├── home.html
            ├── registrazione.html
            ├── login.html
            ├── lista_appuntamenti.html
            └── crea_appuntamento.html
"""

# ============================================================
# STEP 1: INSTALLAZIONE
# ============================================================

"""
1. Apri il terminale e crea una cartella per il progetto:

   mkdir barber_shop
   cd barber_shop

2. Crea un ambiente virtuale Python:

   python -m venv venv
   
3. Attiva l'ambiente virtuale:
   
   Windows:  venv\Scripts\activate
   Mac/Linux: source venv/bin/activate

4. Installa Django:

   pip install django

5. Crea il progetto Django:

   django-admin startproject barber_shop .
   
   (Nota il punto finale! Crea il progetto nella cartella corrente)

6. Crea l'app appointments:

   python manage.py startapp appointments

Ora sei pronto per copiare il codice qui sotto! 👇
"""


# ============================================================
# FILE: requirements.txt
# ============================================================
"""
Django==4.2.7
Pillow==10.1.0
"""


# ============================================================
# FILE: barber_shop/settings.py
# Aggiungi queste modifiche al file settings.py esistente
# ============================================================

"""
# Trova la lista INSTALLED_APPS e aggiungi 'appointments':

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appointments',  # ← AGGIUNGI QUESTA RIGA
]

# Trova LANGUAGE_CODE e cambialo in italiano:

LANGUAGE_CODE = 'it-it'
TIME_ZONE = 'Europe/Rome'
USE_I18N = True
USE_TZ = True

# Alla fine del file aggiungi:

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/appuntamenti/'
"""


# ============================================================
# FILE: barber_shop/urls.py
# ============================================================

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('appointments.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# ============================================================
# FILE: appointments/models.py
# ============================================================

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Cliente(models.Model):
    """Rappresenta un cliente del parrucchiere"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100, verbose_name="Nome completo")
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    data_registrazione = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nome} ({self.email})"
    
    class Meta:
        verbose_name_plural = "Clienti"


class Barbiere(models.Model):
    """Rappresenta un barbiere che lavora nel negozio"""
    nome = models.CharField(max_length=100)
    specialita = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='barbieri/', null=True, blank=True)
    attivo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Barbieri"


class Servizio(models.Model):
    """Tipi di servizi offerti"""
    nome = models.CharField(max_length=100)
    descrizione = models.TextField()
    durata_minuti = models.IntegerField(help_text="Durata del servizio in minuti")
    prezzo = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"{self.nome} (€{self.prezzo} - {self.durata_minuti}min)"
    
    class Meta:
        verbose_name_plural = "Servizi"


class Appuntamento(models.Model):
    """Rappresenta un singolo appuntamento"""
    STATI = [
        ('confermato', 'Confermato'),
        ('completato', 'Completato'),
        ('cancellato', 'Cancellato'),
        ('in_attesa', 'In Attesa'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='appuntamenti')
    barbiere = models.ForeignKey(Barbiere, on_delete=models.CASCADE, related_name='appuntamenti')
    servizio = models.ForeignKey(Servizio, on_delete=models.CASCADE)
    data_ora = models.DateTimeField(verbose_name="Data e ora")
    stato = models.CharField(max_length=20, choices=STATI, default='confermato')
    note = models.TextField(blank=True, null=True)
    creato_il = models.DateTimeField(auto_now_add=True)
    modificato_il = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.cliente.nome} - {self.data_ora.strftime('%d/%m/%Y %H:%M')}"
    
    class Meta:
        verbose_name_plural = "Appuntamenti"
        ordering = ['-data_ora']
        
    def is_passato(self):
        """Verifica se l'appuntamento è nel passato"""
        return self.data_ora < timezone.now()


# ============================================================
# FILE: appointments/forms.py
# ============================================================

from django import forms
from django.contrib.auth.models import User
from .models import Appuntamento, Cliente


class RegistrazioneForm(forms.Form):
    """Form per registrare un nuovo cliente"""
    nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mario Rossi'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'mario@example.com'})
    )
    telefono = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '333 1234567'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    conferma_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Conferma password'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        conferma = cleaned_data.get('conferma_password')
        
        if password and conferma and password != conferma:
            raise forms.ValidationError("Le password non corrispondono!")
        
        return cleaned_data
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Questa email è già registrata!")
        return email


class AppuntamentoForm(forms.ModelForm):
    """Form per creare/modificare un appuntamento"""
    class Meta:
        model = Appuntamento
        fields = ['barbiere', 'servizio', 'data_ora', 'note']
        widgets = {
            'barbiere': forms.Select(attrs={'class': 'form-control'}),
            'servizio': forms.Select(attrs={'class': 'form-control'}),
            'data_ora': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
                format='%Y-%m-%dT%H:%M'
            ),
            'note': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Note opzionali...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostra solo barbieri attivi
        self.fields['barbiere'].queryset = self.fields['barbiere'].queryset.filter(attivo=True)


# ============================================================
# FILE: appointments/views.py
# ============================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import Appuntamento, Cliente, Barbiere, Servizio
from .forms import RegistrazioneForm, AppuntamentoForm
from datetime import datetime, timedelta


# ===== HOME PAGE (GET) =====
def home(request):
    """
    Home page - usa solo GET
    """
    context = {
        'barbieri': Barbiere.objects.filter(attivo=True),
        'servizi': Servizio.objects.all(),
    }
    return render(request, 'appointments/home.html', context)


# ===== REGISTRAZIONE (GET + POST) =====
def registrazione(request):
    """
    GET  -> Mostra il form di registrazione
    POST -> Crea il nuovo cliente
    """
    if request.method == 'POST':
        # 📝 POST: Processa il form
        form = RegistrazioneForm(request.POST)
        
        if form.is_valid():
            # Crea l'utente Django
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            
            # Crea il cliente
            cliente = Cliente.objects.create(
                user=user,
                nome=form.cleaned_data['nome'],
                email=form.cleaned_data['email'],
                telefono=form.cleaned_data['telefono']
            )
            
            # Login automatico
            login(request, user)
            messages.success(request, f'Benvenuto {cliente.nome}! Registrazione completata.')
            
            # Redirect dopo POST (pattern POST-REDIRECT-GET)
            return redirect('lista_appuntamenti')
        else:
            # Form non valido - mostra errori
            messages.error(request, 'Correggi gli errori nel form.')
    
    else:
        # 📖 GET: Mostra il form vuoto
        form = RegistrazioneForm()
    
    return render(request, 'appointments/registrazione.html', {'form': form})


# ===== LOGIN (GET + POST) =====
def login_view(request):
    """
    GET  -> Mostra il form di login
    POST -> Effettua il login
    """
    if request.method == 'POST':
        # 📝 POST: Processa il login
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Autentica l'utente
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bentornato!')
            return redirect('lista_appuntamenti')
        else:
            messages.error(request, 'Email o password non corretti.')
    
    # 📖 GET: Mostra il form di login
    return render(request, 'appointments/login.html')


# ===== LOGOUT (POST) =====
@require_http_methods(["POST"])
def logout_view(request):
    """
    Solo POST per sicurezza
    """
    logout(request)
    messages.success(request, 'Logout effettuato.')
    return redirect('home')


# ===== LISTA APPUNTAMENTI CON FILTRI (GET) =====
@login_required
def lista_appuntamenti(request):
    """
    GET con parametri URL per filtrare
    Esempio: /appuntamenti/?data=2025-10-15&barbiere=1&stato=confermato
    """
    # Prendi il cliente loggato
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        messages.error(request, 'Profilo cliente non trovato.')
        return redirect('home')
    
    # Inizia con tutti gli appuntamenti del cliente
    appuntamenti = Appuntamento.objects.filter(cliente=cliente)
    
    # 📖 LEGGI i parametri GET dall'URL
    data_filtro = request.GET.get('data')
    barbiere_id = request.GET.get('barbiere')
    stato_filtro = request.GET.get('stato')
    
    # Applica i filtri se presenti
    if data_filtro:
        appuntamenti = appuntamenti.filter(data_ora__date=data_filtro)
    
    if barbiere_id:
        appuntamenti = appuntamenti.filter(barbiere_id=barbiere_id)
    
    if stato_filtro:
        appuntamenti = appuntamenti.filter(stato=stato_filtro)
    
    context = {
        'appuntamenti': appuntamenti,
        'barbieri': Barbiere.objects.filter(attivo=True),
        'stati': Appuntamento.STATI,
        # Mantieni i filtri selezionati
        'filtro_data': data_filtro,
        'filtro_barbiere': barbiere_id,
        'filtro_stato': stato_filtro,
    }
    
    return render(request, 'appointments/lista_appuntamenti.html', context)


# ===== CREA APPUNTAMENTO (GET + POST) =====
@login_required
def crea_appuntamento(request):
    """
    GET  -> Mostra il form per creare appuntamento
    POST -> Crea l'appuntamento nel database
    """
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        messages.error(request, 'Profilo cliente non trovato.')
        return redirect('home')
    
    if request.method == 'POST':
        # 📝 POST: Crea l'appuntamento
        form = AppuntamentoForm(request.POST)
        
        if form.is_valid():
            appuntamento = form.save(commit=False)
            appuntamento.cliente = cliente
            appuntamento.save()
            
            messages.success(request, f'Appuntamento prenotato per il {appuntamento.data_ora.strftime("%d/%m/%Y alle %H:%M")}!')
            
            # Redirect dopo POST di successo
            return redirect('lista_appuntamenti')
        else:
            messages.error(request, 'Correggi gli errori nel form.')
    
    else:
        # 📖 GET: Mostra il form vuoto
        form = AppuntamentoForm()
    
    context = {
        'form': form,
        'barbieri': Barbiere.objects.filter(attivo=True),
        'servizi': Servizio.objects.all(),
    }
    
    return render(request, 'appointments/crea_appuntamento.html', context)


# ===== MODIFICA APPUNTAMENTO (GET + POST) =====
@login_required
def modifica_appuntamento(request, appuntamento_id):
    """
    GET  -> Mostra il form pre-compilato
    POST -> Aggiorna l'appuntamento
    """
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        messages.error(request, 'Profilo cliente non trovato.')
        return redirect('home')
    
    # Prendi l'appuntamento (solo se appartiene al cliente)
    appuntamento = get_object_or_404(Appuntamento, id=appuntamento_id, cliente=cliente)
    
    if request.method == 'POST':
        # 📝 POST: Aggiorna l'appuntamento
        form = AppuntamentoForm(request.POST, instance=appuntamento)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Appuntamento modificato con successo!')
            return redirect('lista_appuntamenti')
        else:
            messages.error(request, 'Correggi gli errori nel form.')
    
    else:
        # 📖 GET: Mostra il form pre-compilato
        form = AppuntamentoForm(instance=appuntamento)
    
    context = {
        'form': form,
        'appuntamento': appuntamento,
        'modifica': True,
    }
    
    return render(request, 'appointments/crea_appuntamento.html', context)


# ===== CANCELLA APPUNTAMENTO (POST) =====
@login_required
@require_http_methods(["POST"])
def cancella_appuntamento(request, appuntamento_id):
    """
    Solo POST per sicurezza!
    Non usare mai GET per cancellare dati!
    """
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        messages.error(request, 'Profilo cliente non trovato.')
        return redirect('home')
    
    appuntamento = get_object_or_404(Appuntamento, id=appuntamento_id, cliente=cliente)
    
    # Cambia lo stato invece di eliminare
    appuntamento.stato = 'cancellato'
    appuntamento.save()
    
    messages.success(request, 'Appuntamento cancellato.')
    return redirect('lista_appuntamenti')


# ===== API JSON: SLOT DISPONIBILI (GET) =====
@login_required
def api_slot_disponibili(request):
    """
    Restituisce gli slot orari disponibili in formato JSON
    GET: /api/slot-disponibili/?data=2025-10-15&barbiere=1
    """
    data_str = request.GET.get('data')
    barbiere_id = request.GET.get('barbiere')
    
    if not data_str or not barbiere_id:
        return JsonResponse({'error': 'Parametri mancanti'}, status=400)
    
    try:
        data = datetime.strptime(data_str, '%Y-%m-%d').date()
        barbiere = Barbiere.objects.get(id=barbiere_id)
    except (ValueError, Barbiere.DoesNotExist):
        return JsonResponse({'error': 'Parametri non validi'}, status=400)
    
    # Trova appuntamenti già prenotati
    appuntamenti_occupati = Appuntamento.objects.filter(
        barbiere=barbiere,
        data_ora__date=data,
        stato='confermato'
    ).values_list('data_ora', flat=True)
    
    orari_occupati = [app.time() for app in appuntamenti_occupati]
    
    # Genera slot dalle 9:00 alle 18:00 ogni 30 minuti
    slot_disponibili = []
    ora_corrente = datetime.min.time().replace(hour=9, minute=0)
    ora_fine = datetime.min.time().replace(hour=18, minute=0)
    
    current_time = datetime.combine(datetime.today(), ora_corrente)
    end_time = datetime.combine(datetime.today(), ora_fine)
    
    while current_time < end_time:
        if current_time.time() not in orari_occupati:
            slot_disponibili.append({
                'ora': current_time.strftime('%H:%M'),
                'disponibile': True
            })
        current_time += timedelta(minutes=30)
    
    return JsonResponse({
        'data': data_str,
        'barbiere': barbiere.nome,
        'slot': slot_disponibili
    })


# ============================================================
# FILE: appointments/urls.py
# ============================================================

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


# ============================================================
# FILE: appointments/admin.py
# ============================================================

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


# ============================================================
# TEMPLATES HTML
# ============================================================

# Crea la cartella: appointments/templates/appointments/
# Poi crea questi file:


# ============================================================
# FILE: appointments/templates/appointments/base.html
# ============================================================

BASE_HTML = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Barbershop{% endblock %}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding-bottom: 50px;
        }
        
        .navbar {
            background: rgba(255,255,255,0.95);
            padding: 15px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .navbar-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .navbar h1 {
            color: #667eea;
            font-size: 1.8em;
        }
        
        .navbar nav a {
            color: #333;
            text-decoration: none;
            margin-left: 20px;
            font-weight: 500;
            transition: color 0.3s;
        }
        
        .navbar nav a:hover {
            color: #667eea;
        }
        
        .container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 20px;
        }
        
        .messages {
            margin-bottom: 20px;
        }
        
        .message {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        
        .message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .form-control {
            width: 100%;
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            margin-bottom: 15px;
        }
        
        .form-control:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
            color: #333;
        }
        
        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5568d3;
            transform: translateY(-2px);
        }
        
        .btn-success {
            background: #4caf50;
            color: white;
        }
        
        .btn-danger {
            background: #f44336;
            color: white;
        }
        
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        table th {
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }
        
        table td {
            padding: 12px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        table tr:hover {
            background: #f5f5f5;
        }
        
        .badge {
            padding: 5px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 500;
        }
        
        .badge-success {
            background: #c8e6c9;
            color: #2e7d32;
        }
        
        .badge-danger {
            background: #ffcdd2;
            color: #c62828;
        }
        
        .badge-warning {
            background: #ffe0b2;
            color: #e65100;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <div class="navbar-content">
            <h1>💈 Barbershop</h1>
            <nav>
                <a href="{% url 'home' %}">Home</a>
                {% if user.is_authenticated %}
                    <a href="{% url 'lista_appuntamenti' %}">Miei Appuntamenti</a>
                    <a href="{% url 'crea_appuntamento' %}">Prenota</a>
                    <form method="POST" action="{% url 'logout' %}" style="display: inline;">
                        {% csrf_token %}
                        <button type="submit" style="background: none; border: none; color: #333; cursor: pointer; font: inherit; margin-left: 20px; font-weight: 500;">Logout</button>
                    </form>
                {% else %}
                    <a href="{% url 'login' %}">Login</a>
                    <a href="{% url 'registrazione' %}">Registrati</a>
                {% endif %}
            </nav>
        </div>
    </div>
    
    <div class="container">
        {% if messages %}
            <div class="messages">
                {% for message in messages %}
                    <div class="message {{ message.tags }}">
                        {{ message }}
                    </div>
                {% endfor %}
            </div>
        {% endif %}
        
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""


# ============================================================
# FILE: appointments/templates/appointments/home.html
# ============================================================

HOME_HTML = """
{% extends 'appointments/base.html' %}

{% block title %}Home - Barbershop{% endblock %}

{% block content %}
<div class="card">
    <h1 style="color: #667eea; margin-bottom: 20px;">💈 Benvenuto nel nostro Barbershop!</h1>
    <p style="font-size: 1.2em; color: #666; margin-bottom: 30px;">
        Prenota il tuo appuntamento online in pochi click!
    </p>
    
    {% if not user.is_authenticated %}
        <div style="margin-bottom: 30px;">
            <a href="{% url 'registrazione' %}" class="btn btn-primary" style="margin-right: 10px;">
                Registrati Ora
            </a>
            <a href="{% url 'login' %}" class="btn btn-secondary">
                Accedi
            </a>
        </div>
    {% else %}
        <div style="margin-bottom: 30px;">
            <a href="{% url 'crea_appuntamento' %}" class="btn btn-success">
                Prenota Appuntamento
            </a>
        </div>
    {% endif %}
    
    <h2 style="color: #333; margin-top: 40px; margin-bottom: 20px;">I Nostri Barbieri</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
        {% for barbiere in barbieri %}
        <div style="background: #f5f5f5; padding: 20px; border-radius: 10px;">
            <h3 style="color: #667eea;">{{ barbiere.nome }}</h3>
            <p style="color: #666;">{{ barbiere.specialita }}</p>
        </div>
        {% endfor %}
    </div>
    
    <h2 style="color: #333; margin-top: 40px; margin-bottom: 20px;">I Nostri Servizi</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
        {% for servizio in servizi %}
        <div style="background: #f5f5f5; padding: 20px; border-radius: 10px;">
            <h3 style="color: #667eea;">{{ servizio.nome }}</h3>
            <p style="color: #666;">{{ servizio.descrizione }}</p>
            <p style="font-weight: bold; color: #4caf50; margin-top: 10px;">
                €{{ servizio.prezzo }} - {{ servizio.durata_minuti }} minuti
            </p>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
"""


# ============================================================
# FILE: appointments/templates/appointments/registrazione.html
# ============================================================

REGISTRAZIONE_HTML = """
{% extends 'appointments/base.html' %}

{% block title %}Registrazione{% endblock %}

{% block content %}
<div class="card" style="max-width: 600px; margin: 0 auto;">
    <h1 style="color: #667eea; margin-bottom: 30px;">📝 Registrazione</h1>
    
    <!-- FORM POST per registrarsi -->
    <form method="POST" action="{% url 'registrazione' %}">
        {% csrf_token %}
        
        <div class="form-group">
            <label>Nome Completo:</label>
            {{ form.nome }}
            {% if form.nome.errors %}
                <p style="color: red;">{{ form.nome.errors }}</p>
            {% endif %}
        </div>
        
        <div class="form-group">
            <label>Email:</label>
            {{ form.email }}
            {% if form.email.errors %}
                <p style="color: red;">{{ form.email.errors }}</p>
            {% endif %}
        </div>
        
        <div class="form-group">
            <label>Telefono:</label>
            {{ form.telefono }}
            {% if form.telefono.errors %}
                <p style="color: red;">{{ form.telefono.errors }}</p>
            {% endif %}
        </div>
        
        <div class="form-group">
            <label>Password:</label>
            {{ form.password }}
            {% if form.password.errors %}
                <p style="color: red;">{{ form.password.errors }}</p>
            {% endif %}
        </div>
        
        <div class="form-group">
            <label>Conferma Password:</label>
            {{ form.conferma_password }}
            {% if form.conferma_password.errors %}
                <p style="color: red;">{{ form.conferma_password.errors }}</p>
            {% endif %}
        </div>
        
        {% if form.non_field_errors %}
            <p style="color: red;">{{ form.non_field_errors }}</p>
        {% endif %}
        
        <button type="submit" class="btn btn-primary">Registrati</button>
        <a href="{% url 'login' %}" style="margin-left: 10px;">Hai già un account? Accedi</a>
    </form>
</div>
{% endblock %}
"""


# ============================================================
# FILE: appointments/templates/appointments/login.html
# ============================================================

LOGIN_HTML = """
{% extends 'appointments/base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
<div class="card" style="max-width: 500px; margin: 0 auto;">
    <h1 style="color: #667eea; margin-bottom: 30px;">🔐 Login</h1>
    
    <!-- FORM POST per login -->
    <form method="POST" action="{% url 'login' %}">
        {% csrf_token %}
        
        <div class="form-group">
            <label>Email:</label>
            <input type="email" name="email" class="form-control" required>
        </div>
        
        <div class="form-group">
            <label>Password:</label>
            <input type="password" name="password" class="form-control" required>
        </div>
        
        <button type="submit" class="btn btn-primary">Accedi</button>
        <a href="{% url 'registrazione' %}" style="margin-left: 10px;">Non hai un account? Registrati</a>
    </form>
</div>
{% endblock %}
"""


# ============================================================
# FILE: appointments/templates/appointments/lista_appuntamenti.html
# ============================================================

LISTA_HTML = """
{% extends 'appointments/base.html' %}

{% block title %}I Miei Appuntamenti{% endblock %}

{% block content %}
<div class="card">
    <h1 style="color: #667eea; margin-bottom: 30px;">📅 I Miei Appuntamenti</h1>
    
    <a href="{% url 'crea_appuntamento' %}" class="btn btn-success" style="margin-bottom: 20px;">
        ➕ Nuovo Appuntamento
    </a>
    
    <!-- FORM GET per filtrare -->
    <form method="GET" action="{% url 'lista_appuntamenti' %}" style="background: #f5f5f5; padding: 20px; border-radius: 10px; margin-bottom: 30px;">
        <h3 style="margin-bottom: 15px;">🔍 Filtra Appuntamenti</h3>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
            <div class="form-group">
                <label>Data:</label>
                <input type="date" name="data" value="{{ filtro_data }}" class="form-control">
            </div>
            
            <div class="form-group">
                <label>Barbiere:</label>
                <select name="barbiere" class="form-control">
                    <option value="">Tutti</option>
                    {% for barbiere in barbieri %}
                        <option value="{{ barbiere.id }}" {% if filtro_barbiere == barbiere.id|stringformat:"s" %}selected{% endif %}>
                            {{ barbiere.nome }}
                        </option>
                    {% endfor %}
                </select>
            </div>
            
            <div class="form-group">
                <label>Stato:</label>
                <select name="stato" class="form-control">
                    <option value="">Tutti</option>
                    {% for stato_key, stato_label in stati %}
                        <option value="{{ stato_key }}" {% if filtro_stato == stato_key %}selected{% endif %}>
                            {{ stato_label }}
                        </option>
                    {% endfor %}
                </select>
            </div>
        </div>
        
        <button type="submit" class="btn btn-primary">Cerca</button>
        <a href="{% url 'lista_appuntamenti' %}" class="btn btn-secondary">Reset Filtri</a>
    </form>
    
    <!-- Tabella appuntamenti -->
    {% if appuntamenti %}
    <table>
        <thead>
            <tr>
                <th>Data e Ora</th>
                <th>Barbiere</th>
                <th>Servizio</th>
                <th>Prezzo</th>
                <th>Stato</th>
                <th>Azioni</th>
            </tr>
        </thead>
        <tbody>
            {% for app in appuntamenti %}
            <tr>
                <td>{{ app.data_ora|date:"d/m/Y H:i" }}</td>
                <td>{{ app.barbiere.nome }}</td>
                <td>{{ app.servizio.nome }}</td>
                <td>€{{ app.servizio.prezzo }}</td>
                <td>
                    {% if app.stato == 'confermato' %}
                        <span class="badge badge-success">{{ app.get_stato_display }}</span>
                    {% elif app.stato == 'cancellato' %}
                        <span class="badge badge-danger">{{ app.get_stato_display }}</span>
                    {% else %}
                        <span class="badge badge-warning">{{ app.get_stato_display }}</span>
                    {% endif %}
                </td>
                <td>
                    {% if app.stato == 'confermato' and not app.is_passato %}
                        <a href="{% url 'modifica_appuntamento' app.id %}" class="btn btn-primary" style="padding: 5px 15px; font-size: 14px;">
                            Modifica
                        </a>
                        
                        <!-- FORM POST per cancellare -->
                        <form method="POST" action="{% url 'cancella_appuntamento' app.id %}" style="display: inline;">
                            {% csrf_token %}
                            <button type="submit" class="btn btn-danger" style="padding: 5px 15px; font-size: 14px;" onclick="return confirm('Sicuro di voler cancellare?')">
                                Cancella
                            </button>
                        </form>
                    {% else %}
                        <span style="color: #999;">-</span>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
        <p style="text-align: center; color: #999; padding: 40px;">
            Nessun appuntamento trovato. <a href="{% url 'crea_appuntamento' %}">Prenota il tuo primo appuntamento!</a>
        </p>
    {% endif %}
</div>
{% endblock %}
"""


# ============================================================
# FILE: appointments/templates/appointments/crea_appuntamento.html
# ============================================================

CREA_HTML = """
{% extends 'appointments/base.html' %}

{% block title %}{% if modifica %}Modifica{% else %}Nuovo{% endif %} Appuntamento{% endblock %}

{% block content %}
<div class="card" style="max-width: 700px; margin: 0 auto;">
    <h1 style="color: #667eea; margin-bottom: 30px;">
        {% if modifica %}
            ✏️ Modifica Appuntamento
        {% else %}
            ➕ Nuovo Appuntamento
        {% endif %}
    </h1>
    
    <!-- FORM POST per creare/modificare -->
    <form method="POST">
        {% csrf_token %}
        
        <div class="form-group">
            <label>Barbiere:</label>
            {{ form.barbiere }}
            {% if form.barbiere.errors %}
                <p style="color: red;">{{ form.barbiere.errors }}</p>
            {% endif %}
        </div>
        
        <div class="form-group">
            <label>Servizio:</label>
            {{ form.servizio }}
            {% if form.servizio.errors %}
                <p style="color: red;">{{ form.servizio.errors }}</p>
            {% endif %}
        </div>
        
        <div class="form-group">
            <label>Data e Ora:</label>
            {{ form.data_ora }}
            {% if form.data_ora.errors %}
                <p style="color: red;">{{ form.data_ora.errors }}</p>
            {% endif %}
        </div>
        
        <div class="form-group">
            <label>Note (opzionale):</label>
            {{ form.note }}
            {% if form.note.errors %}
                <p style="color: red;">{{ form.note.errors }}</p>
            {% endif %}
        </div>
        
        <button type="submit" class="btn btn-success">
            {% if modifica %}Salva Modifiche{% else %}Prenota{% endif %}
        </button>
        <a href="{% url 'lista_appuntamenti' %}" class="btn btn-secondary">Annulla</a>
    </form>
    
    <!-- Mostra slot disponibili con AJAX -->
    <div id="slot-disponibili" style="margin-top: 30px; background: #f5f5f5; padding: 20px; border-radius: 10px; display: none;">
        <h3 style="margin-bottom: 15px;">⏰ Orari Disponibili</h3>
        <div id="slot-list"></div>
    </div>
</div>

<script>
// JavaScript per caricare slot disponibili
document.addEventListener('DOMContentLoaded', function() {
    const barbiereSelect = document.querySelector('[name="barbiere"]');
    const dataInput = document.querySelector('[name="data_ora"]');
    
    if (barbiereSelect && dataInput) {
        barbiereSelect.addEventListener('change', caricaSlot);
        dataInput.addEventListener('change', caricaSlot);
    }
    
    async function caricaSlot() {
        const barbiere = barbiereSelect.value;
        const dataTime = dataInput.value;
        
        if (!barbiere || !dataTime) return;
        
        const data = dataTime.split('T')[0];
        
        try {
            // Chiamata GET alla API
            const response = await fetch(`/api/slot-disponibili/?data=${data}&barbiere=${barbiere}`);
            const dati = await response.json();
            
            const container = document.getElementById('slot-disponibili');
            const slotList = document.getElementById('slot-list');
            
            if (dati.slot && dati.slot.length > 0) {
                container.style.display = 'block';
                slotList.innerHTML = '<p style="color: #4caf50; margin-bottom: 10px;">✅ Orari disponibili:</p>';
                
                const slotHtml = dati.slot.map(slot => 
                    `<button type="button" class="btn btn-secondary" style="margin: 5px; padding: 8px 20px; font-size: 14px;" onclick="selezionaSlot('${data}', '${slot.ora}')">${slot.ora}</button>`
                ).join('');
                
                slotList.innerHTML += slotHtml;
            } else {
                container.style.display = 'block';
                slotList.innerHTML = '<p style="color: #f44336;">❌ Nessun orario disponibile per questa data</p>';
            }
        } catch (error) {
            console.error('Errore:', error);
        }
    }
});

function selezionaSlot(data, ora) {
    const dataInput = document.querySelector('[name="data_ora"]');
    dataInput.value = `${data}T${ora}`;
}
</script>
{% endblock %}
"""


# ============================================================
# STEP 2: COMANDI PER COMPLETARE L'INSTALLAZIONE
# ============================================================

"""
Dopo aver copiato tutto il codice sopra nei file appropriati:

1. Crea le tabelle nel database:
   
   python manage.py makemigrations
   python manage.py migrate

2. Crea un superuser per l'admin:
   
   python manage.py createsuperuser
   
   Inserisci:
   - Username: admin
   - Email: admin@example.com
   - Password: (la tua password)

3. Avvia il server:
   
   python manage.py runserver

4. Apri il browser:
   
   http://localhost:8000/

5. Accedi all'admin per aggiungere barbieri e servizi:
   
   http://localhost:8000/admin/
   
   Aggiungi almeno:
   - 2-3 Barbieri (Marco, Giuseppe, Antonio)
   - 2-3 Servizi (Taglio €20, Barba €15, Taglio+Barba €30)

6. Torna su http://localhost:8000/ e prova a:
   - Registrarti come cliente
   - Prenotare un appuntamento
   - Filtrare gli appuntamenti
   - Modificare/cancellare un appuntamento
"""


# ============================================================
# STEP 3: COME TESTARE GET E POST
# ============================================================

"""
📖 TEST GET (con i filtri):

1. Vai su http://localhost:8000/appuntamenti/
2. Nell'URL aggiungi parametri manualmente:
   http://localhost:8000/appuntamenti/?data=2025-10-15&barbiere=1
3. Osserva come Django filtra gli appuntamenti!
4. Cambia i parametri nell'URL e ricarica
5. Usa i filtri nel form - vedi come l'URL cambia!


📝 TEST POST (creando appuntamento):

1. Vai su http://localhost:8000/appuntamenti/nuovo/
2. Compila il form
3. Apri DevTools del browser (F12) → scheda Network
4. Clicca "Prenota"
5. Nella scheda Network vedrai la richiesta POST
6. Clicca sulla richiesta per vedere:
   - Method: POST
   - Form Data: i tuoi dati (non nell'URL!)
7. Dopo il POST, vedi che Django fa un redirect (302)
8. Poi il browser fa un GET alla lista (200)


🧪 TEST CON DJANGO SHELL:

python manage.py shell

>>> from django.test import Client
>>> c = Client()
>>> 
>>> # Login prima
>>> c.login(username='tuaemail@example.com', password='tuapassword')
>>> 
>>> # TEST GET con parametri
>>> response = c.get('/appuntamenti/?data=2025-10-15')
>>> print(response.status_code)  # 200
>>> print(response.context['appuntamenti'])  # Vedi i risultati
>>> 
>>> # TEST POST
>>> response = c.post('/appuntamenti/nuovo/', {
...     'barbiere': 1,
...     'servizio': 1,
...     'data_ora': '2025-10-15 10:00',
... })
>>> print(response.status_code)  # 302 (redirect)
>>> print(response.url)  # /appuntamenti/
"""


# ============================================================
# RIEPILOGO FILE DA CREARE
# ============================================================

"""
✅ File Python da modificare/creare:
   - barber_shop/settings.py (modifica)
   - barber_shop/urls.py (sovrascrivi)
   - appointments/models.py
   - appointments/views.py
   - appointments/urls.py
   - appointments/forms.py
   - appointments/admin.py

✅ Template HTML da creare in appointments/templates/appointments/:
   - base.html
   - home.html
   - registrazione.html
   - login.html
   - lista_appuntamenti.html
   - crea_appuntamento.html

✅ Comandi da eseguire:
   1. python manage.py makemigrations
   2. python manage.py migrate
   3. python manage.py createsuperuser
   4. python manage.py runserver

✅ Poi aggiungi barbieri e servizi dall'admin!
"""