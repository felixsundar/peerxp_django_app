from django import forms

class NewTicketForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lastName'] = forms.CharField(label='Last Name', initial=user.last_name)
        self.fields['email'] = forms.EmailField(label='Email', initial=user.email)

    subject = forms.CharField(label='Subject', max_length=255)
    departmentId = forms.ChoiceField(
        label='Department',
        choices=[(74304000000010772, 'PeerXP Test'), (74304000000129045, 'Customer Support'), (74304000000135307, 'Human Resource')],
        widget=forms.Select
    ) 
    description = forms.CharField(label='Description', max_length=3000, widget=forms.Textarea)
    category = forms.CharField(label='Category', max_length=255)
    priority = forms.ChoiceField(
        label='Priority',
        choices=[('Low','Low'), ('Medium','Medium'), ('High','High')],
        widget=forms.Select
    )

class EditTicketForm(forms.Form):
    subject = forms.CharField(label='Subject', max_length=255)
    departmentId = forms.ChoiceField(
        label='Department',
        choices=[(74304000000010772, 'PeerXP Test'), (74304000000129045, 'Customer Support'), (74304000000135307, 'Human Resource')],
        widget=forms.Select
    ) 
    description = forms.CharField(label='Description', max_length=3000, widget=forms.Textarea)
    category = forms.CharField(label='Category', max_length=255)
    priority = forms.ChoiceField(
        label='Priority',
        choices=[('Low','Low'), ('Medium','Medium'), ('High','High')],
        widget=forms.Select
    )
    status = forms.ChoiceField(
        label='Status',
        choices=[('Open','Open'), ('On Hold','On Hold'), ('Escalated', 'Escalated'), ('Closed','Closed')],
        widget=forms.Select
    )