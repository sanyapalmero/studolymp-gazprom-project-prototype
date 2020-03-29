from django import forms


class TaskForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    until_to = forms.DateTimeField()
