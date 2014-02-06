from django import forms

class QuestSearchBar(forms.Form)
    query = forms.CharField(max_length = 100)
