from django import forms

from books.models import Books
from comment.models import Comment


class AddCommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'width': "100%", 'rows': "6", }))

    class Meta:
        model = Comment
        fields = "__all__"
