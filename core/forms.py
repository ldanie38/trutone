
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    phone = forms.CharField(max_length=40, required=False)
    process = forms.CharField(max_length=100, required=False)
    message = forms.CharField(widget=forms.Textarea, required=False)
    attachment = forms.FileField(required=False)
    website = forms.CharField(required=False, widget=forms.HiddenInput)  # honeypot

    def clean_website(self):
        if self.cleaned_data.get('website'):
            raise forms.ValidationError("Spam detected.")
        return self.cleaned_data.get('website')
