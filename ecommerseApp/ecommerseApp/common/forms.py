from django import forms


class SearchForm(forms.Form):
    search_term = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Search',
                   'class': 'form-control',
                   'style': 'width: 310px;'
                   }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_term'].label = ''
