from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Comment, ContactMessage, Task


class ContactForm(forms.ModelForm):
    """Form for website visitors to send a message."""

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and " " in email:
            raise forms.ValidationError("Email must not contain spaces.")
        return email

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        help_texts = {
            "message": "We typically respond within 24 hours.",
        }
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


INPUT_CLASS = "w-full bg-slate-800 border border-slate-700 rounded-md px-4 py-2.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400"
ERROR_INPUT_CLASS = "w-full bg-slate-800 border border-pink-600 rounded-md px-4 py-2.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-pink-400"


class RegisterForm(UserCreationForm):
    """Custom registration form with email field and Tailwind styling."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": INPUT_CLASS,
            "placeholder": "your@email.com",
        }),
    )

    class Meta(UserCreationForm.Meta):
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": INPUT_CLASS,
            "placeholder": "Choose a username",
            "autofocus": True,
        })
        self.fields["password1"].widget.attrs.update({
            "class": INPUT_CLASS,
            "placeholder": "Enter a password",
        })
        self.fields["password2"].widget.attrs.update({
            "class": INPUT_CLASS,
            "placeholder": "Repeat password",
        })
        self.fields["username"].help_text = "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        self.fields["password1"].help_text = (
            "Your password can't be too similar to your personal info, "
            "must be at least 8 characters, can't be entirely numeric."
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and " " in email:
            raise forms.ValidationError("Email must not contain spaces.")
        return email


class CommentForm(forms.ModelForm):
    """Form for adding comments to a task."""

    class Meta:
        model = Comment
        fields = ["author", "body"]
        widgets = {
            "author": forms.TextInput(attrs={
                "class": "w-full bg-slate-800 border border-slate-700 rounded-md px-4 py-2.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400",
                "placeholder": "Your name",
                "autofocus": True,
            }),
            "body": forms.Textarea(attrs={
                "class": "w-full bg-slate-800 border border-slate-700 rounded-md px-4 py-2.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400",
                "placeholder": "Write a comment...",
                "rows": 3,
            }),
        }
