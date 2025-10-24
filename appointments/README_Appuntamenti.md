# Spiegazione del Sistema di Inserimento Appuntamenti in Django

Questo documento spiega come funziona il processo di inserimento di un appuntamento nel sistema barber shop, dal punto di vista della programmazione Django. Si fa riferimento ai file del codice sorgente nell'app `appointments`.

## Panoramica Generale

Il sistema utilizza Django per gestire la prenotazione di appuntamenti. Il processo coinvolge modelli, form, viste e template per garantire una validazione robusta e un'interfaccia utente intuitiva.

## Modelli Coinvolti

### Appuntamento (models.py)

Il modello principale è `Appuntamento` definito in `appointments/models.py`:

- **Campi principali**:
  - `cliente`: ForeignKey a Cliente (l'utente loggato).
  - `barbiere`: ForeignKey a Barbiere (selezionato dall'utente).
  - `servizio`: ForeignKey a Servizio (tipo di servizio richiesto).
  - `data_ora`: DateTimeField per data e ora dell'appuntamento.
  - `stato`: CharField con scelte predefinite (confermato, completato, etc.).
  - `note`: TextField opzionale.

- **Validazione personalizzata** (metodo `clean`):
  - Controlla che `data_ora` sia nel futuro rispetto all'ora corrente.
  - Se la data è nel passato, solleva `ValidationError` con messaggio: "Per favore controlla la data e anche i dati mancanti per favore".
  - Questo previene appuntamenti retroattivi.

Altri modelli correlati:
- `Cliente`: Rappresenta l'utente che prenota.
- `Barbiere`: I barbieri disponibili.
- `Servizio`: I tipi di servizi offerti.

## Form per l'Inserimento (forms.py)

Il form `AppuntamentoForm` in `appointments/forms.py` è un ModelForm basato su `Appuntamento`:

- **Campi esclusi**: `cliente`, `stato`, `creato_il`, `modificato_il` (gestiti automaticamente).
- **Widget personalizzati**:
  - `data_ora`: DateTimeInput con `type='datetime-local'` per un picker nativo.
  - Altri campi: Select per barbiere e servizio, Textarea per note.

- **Inizializzazione** (`__init__`):
  - Filtra barbieri attivi.
  - Imposta stato predefinito a 'confermato' per nuovi appuntamenti.

## Viste per la Gestione (views.py)

Le viste gestiscono le richieste HTTP e coordinano modelli e form.

### crea_appuntamento (views.py:152-189)

- **GET**: Mostra il form vuoto con barbieri e servizi disponibili.
- **POST**:
  - Valida il form con `form.is_valid()`.
  - Se valido: Salva l'appuntamento associandolo al cliente loggato, mostra messaggio di successo e reindirizza a `lista_appuntamenti`.
  - Se non valido: Mostra errori nel form e messaggio: "Per favore controlla la data e anche i dati mancanti per favore".

### modifica_appuntamento (views.py:194-229)

- Simile a `crea_appuntamento`, ma per modificare appuntamenti esistenti.
- Carica l'istanza esistente e aggiorna i campi.

### Altre viste correlate
- `lista_appuntamenti`: Mostra appuntamenti filtrabili.
- `api_slot_disponibili`: API JSON per orari disponibili (usata via AJAX).

## Template per l'Interfaccia (crea_appuntamento.html)

Il template `appointments/templates/appointments/crea_appuntamento.html` rende il form:

- Estende `base.html`.
- Mostra campi del form con errori in rosso: `<p style="color: red;">{{ form.data_ora.errors }}</p>`.
- JavaScript per:
  - Caricare slot disponibili via AJAX quando si cambia barbiere o data.
  - Disabilitare date passate impostando `min` sull'input `datetime-local`.

## Flusso di Inserimento

1. **Richiesta GET**: L'utente accede a `/crea-appuntamento/`, la vista restituisce il form vuoto.
2. **Selezione dati**: L'utente compila barbiere, servizio, data_ora, note.
3. **Validazione lato client**: JavaScript disabilita date passate.
4. **Submit POST**: Il form viene inviato, la vista valida con `form.is_valid()`.
5. **Validazione modello**: Il metodo `clean` di `Appuntamento` controlla la data.
6. **Salvataggio**: Se tutto ok, salva nel DB e reindirizza con messaggio di successo.
7. **Errori**: Se invalid, mostra errori in rosso e messaggio personalizzato.

## Validazione e Sicurezza

- **Server-side**: Validazione in modello e form previene dati invalidi.
- **Client-side**: Min attribute e AJAX migliorano UX.
- **Autenticazione**: Viste decorate con `@login_required` per utenti loggati.
- **CSRF**: Token nel form per sicurezza.

## Riferimenti al Codice

- `appointments/models.py:54-104`: Definizione modello e validazione.
- `appointments/forms.py:43-74`: Form e widget.
- `appointments/views.py:152-189`: Vista creazione.
- `appointments/templates/appointments/crea_appuntamento.html`: Template e JS.

Questo sistema garantisce un'inserimento sicuro e user-friendly per gli appuntamenti.