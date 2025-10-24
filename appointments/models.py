from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class Cliente(models.Model):
    """Rappresenta un cliente del parrucchiere"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100, verbose_name="Nome completo")
    email = models.EmailField(unique=True)
    telefono = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?[\d\s\-\(\)]+$', 'Inserisci un numero di telefono valido (es. +39 123 456 7890 o 0123456789)')]
    )
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
    
    def clean(self):
        """Validazione personalizzata per richiedere appuntamenti futuri"""
        from django.utils import timezone
        now = timezone.now()
        
        if self.data_ora < now:
            raise ValidationError("Per favore controlla la data e anche i dati mancanti per favore")
        super().clean()
