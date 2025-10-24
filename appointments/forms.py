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
        exclude = ['cliente', 'stato', 'creato_il', 'modificato_il']
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
        # Se è una creazione, aggiungi stato nascosto con default
        if not self.instance:
            self.fields['stato'] = forms.CharField(
                initial='confermato',
                widget=forms.HiddenInput()
            )
        # Se è una modifica, aggiungi il campo stato visibile
        elif self.instance:
            self.fields['stato'] = forms.ChoiceField(
                choices=self.instance.STATI,
                initial=self.instance.stato,
                widget=forms.Select(attrs={'class': 'form-control'})
            )