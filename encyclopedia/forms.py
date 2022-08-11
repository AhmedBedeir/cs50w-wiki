from django import forms

class newEntry(forms.Form):
  title = forms.CharField(label= 'Title', max_length=50)
  content = forms.CharField(label= 'Content', widget= forms.Textarea)
class editEntry(forms.Form):
  content = forms.CharField(label='Content',widget=forms.Textarea)