from django import forms

from books.models import Books


class AddBookForm(forms.ModelForm):
    summary = forms.CharField(
        widget=forms.Textarea(attrs={'width': "100%", 'rows': "6", }))

    description = forms.CharField(
        widget=forms.Textarea(attrs={'width': "100%", 'rows': "3", }))

    class Meta:
        model = Books
        fields = "__all__"


class UpdateBookForm(forms.ModelForm):
    summary = forms.CharField(
        widget=forms.Textarea(attrs={'width': "100%", 'rows': "6", }))

    description = forms.CharField(
        widget=forms.Textarea(attrs={'width': "100%", 'rows': "3", }))

    class Meta:
        model = Books
        exclude = ('owner',)
