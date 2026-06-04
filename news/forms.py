from django import forms
from .models import Comment, CommentLike


class CommentForm(forms.ModelForm):
    parent_comment_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Comment
        fields = ['text', 'parent_comment']