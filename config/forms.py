from django import forms


class InputForm(forms.Form):
    ticker = forms.CharField(label="ティッカーシンボル", max_length=255)

    def clean_ticker(self):
        ticker = self.cleaned_data["ticker"]
        if ticker.isalpha():
            return ticker

        raise forms.ValidationError("Not an alphabet is mixed.")
