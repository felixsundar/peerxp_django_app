from django import forms

class NewTicketForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lastName'] = forms.CharField(label='Last Name', initial=user.last_name)
        self.fields['email'] = forms.EmailField(label='Email', initial=user.email)

    departmentId = forms.ChoiceField(
        label='Department',
        choices=[(74304000000010772, 'PeerXP Test'), (74304000000129045, 'Customer Support'), (74304000000135307, 'Human Resource')],
        widget=forms.Select
    )
    category = forms.CharField(label='Category', max_length=255, required=True) 
    subject = forms.CharField(label='Subject', max_length=255, required=True)
    description = forms.CharField(label='Description', max_length=3000, required=False, widget=forms.Textarea)
    priority = forms.ChoiceField(
        label='Priority',
        choices=[('Low','Low'), ('Medium','Medium'), ('High','High')],
        widget=forms.Select
    )

