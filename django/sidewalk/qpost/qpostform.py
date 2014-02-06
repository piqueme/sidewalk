from django import forms

stat_list = ['WISDOM',
             'VITALITY',
             'EATING',
             'SPIRITUAL',
             'FANCY',
             'THRIFTY',
             'NATURE',
             'WORLDLY',
             'HIPSTER']

stat_flavor = ['Brainpower is magic.', 
               'An apple a day keeps the doctor away.',
               'What greater joy is there than food?',
               'It is important to replenish your mana.',
               'My moustache curls in circles.',
               'Coupons never really expire.',
               'I hear the sounds of birds in early morning.',
               'Fez on my head.',
               'So you have no knowledge of this band?']


class QuestPostForm(forms.Form):
    quest_name = forms.CharField(max_length = 100, widget=forms.TextInput(attrs={'placeholder': 'Quest Name', 'class': 'form-control', 'id': 'name'}))
    quest_icon = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'icon'}))
    description = forms.CharField(max_length = 200, widget=forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control', 'id': 'description'}))

    def __init__(self, *args, **kwargs):
        stats = kwargs.pop('stats')
        super(QuestPostForm, self).__init__(*args, **kwargs)
        for index in range(len(stats)):
            self.fields[('stat_' + stats[index])] = forms.IntegerField(label=stats[index], min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control stat', 'value': 0}))

    def clean_image(self):
        image = self.cleaned_data.get('image',False)
        if image:
            if image._size > 2*1024*1024:
                raise ValidationError("Image file too large ( > 2mb )")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")
