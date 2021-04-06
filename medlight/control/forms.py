from django import forms
from .models import Records

class RecordForm(forms.ModelForm):
    class Meta:
        model = Records
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'