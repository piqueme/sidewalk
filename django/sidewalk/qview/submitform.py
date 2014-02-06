from django import forms

def make_submit_form(quest):
	fields = {}
	challenges = quest.challenge_set.all()
	for i in range(len(challenges)):
		fields['verification photo ' + str(i + 1)] = forms.FileField()
	return type('SubmitForm', (forms.BaseForm,), {'base_fields': fields})

def make_verification_notes_form(quest):
        fields = {}
        challenges = quest.challenge_set.all()
        for i in range(len(challenges)):
            fields['verification notes ' + str(i + 1)] = forms.CharField(widget=forms.TextArea)
        return type('VerNotesForm', (forms.BaseForm,), {'base_fields': fields})
