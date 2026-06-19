from django import forms

from .models import ContactMessage, Task


class ContactForm(forms.ModelForm):
    """Form for website visitors to send a message."""

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


class TaskForm(forms.ModelForm):
    """Form for creating and editing tasks."""

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if title and len(title.strip()) < 2:
            raise forms.ValidationError("Title must be at least 2 characters.")
        return title.strip()

    class Meta:
        model = Task
        fields = ["title", "description", "completed"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full bg-slate-800 border border-slate-700 rounded-md px-4 py-2.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400",
                "placeholder": "Task title",
                "autofocus": True,
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full bg-slate-800 border border-slate-700 rounded-md px-4 py-2.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400",
                "placeholder": "Optional description",
                "rows": 3,
            }),
            "completed": forms.CheckboxInput(attrs={
                "class": "w-4 h-4 rounded border-slate-700 bg-slate-800 text-cyan-600 focus:ring-cyan-400",
            }),
        }
        help_texts = {
            "title": "Give your task a clear, concise title.",
            "description": "Add any additional details or notes (optional).",
        }
