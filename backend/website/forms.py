from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full bg-slate-800 border border-slate-700 rounded-md px-4 py-2.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400",
                "placeholder": "Your name",
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full bg-slate-800 border border-slate-700 rounded-md px-4 py-2.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400",
                "placeholder": "your@email.com",
            }),
            "message": forms.Textarea(attrs={
                "class": "w-full bg-slate-800 border border-slate-700 rounded-md px-4 py-2.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400",
                "placeholder": "How can we help?",
                "rows": 5,
            }),
        }
