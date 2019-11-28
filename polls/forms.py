from django import forms

class AddTask(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text', 'pub_date',)
        pub_date = forms.DateField(
            widget=forms.DateInput(
                attrs={
                    'type': 'date',
                }
            )
        )
