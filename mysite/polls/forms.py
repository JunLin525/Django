from django import forms
from .models import Question, Choice
import datetime
from datetime import datetime

class QuestionForm(forms.ModelForm):
    pub_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=False)
    
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']
    widgets = {
            'pub_date': forms.HiddenInput(), # 隱藏 pub_date 欄位
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # 只有當表單是新建時才會設置 pub_date
            self.fields['pub_date'].initial = datetime.now()


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']