from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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
            messages.error(request, 'Per favore controlla la data e anche i dati mancanti per favore')
    
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
            messages.error(request, 'Per favore controlla la data e anche i dati mancanti per favore')
    
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
