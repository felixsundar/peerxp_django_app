from django import forms

class NewTicketForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(label='Name', initial=user.first_name)
        self.fields['email'] = forms.EmailField(label='Email', initial=user.email)

    crushUsername = forms.CharField(label='Instagram Username of your crush', max_length=255, required=True)
    crushNickname = forms.CharField(label='Nickname for your crush', max_length=255, required=False)
    crushMessage = forms.CharField(label='Your Message', max_length=3000, required=False, widget=forms.Textarea)
    whomToInform = forms.ChoiceField(
        label='Who should be informed, if matched?',
        choices=[(1, 'Choose at random'), (2, 'Inform my crush')],
        initial=1,
        widget=forms.RadioSelect
    )

    def clean_crushUsername(self):
        field = self.cleaned_data['field']
        if not field:
            raise forms.ValidationError('Name can contain only alphabets and spaces.')
        return field
