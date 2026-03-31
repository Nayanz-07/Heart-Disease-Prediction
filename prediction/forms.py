from django import forms


class PredictionForm(forms.Form):
    """Form for heart disease prediction input."""

    SEX_CHOICES = [(1, 'Male'), (0, 'Female')]
    CP_CHOICES = [
        (0, 'Typical Angina'),
        (1, 'Atypical Angina'),
        (2, 'Non-Anginal Pain'),
        (3, 'Asymptomatic'),
    ]
    FBS_CHOICES = [(1, 'Yes (>120 mg/dl)'), (0, 'No (≤120 mg/dl)')]
    RESTECG_CHOICES = [
        (0, 'Normal'),
        (1, 'ST-T Wave Abnormality'),
        (2, 'Left Ventricular Hypertrophy'),
    ]

    age = forms.IntegerField(
        min_value=1, max_value=120,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'placeholder': 'e.g. 45',
            'id': 'id_age'
        }),
        label='Age (years)'
    )
    sex = forms.ChoiceField(
        choices=SEX_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_sex'}),
        label='Gender'
    )
    cp = forms.ChoiceField(
        choices=CP_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_cp'}),
        label='Chest Pain Type'
    )
    trestbps = forms.IntegerField(
        min_value=50, max_value=300,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'placeholder': 'e.g. 120',
            'id': 'id_trestbps'
        }),
        label='Resting Blood Pressure (mmHg)'
    )
    chol = forms.IntegerField(
        min_value=50, max_value=700,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'placeholder': 'e.g. 200',
            'id': 'id_chol'
        }),
        label='Serum Cholesterol (mg/dl)'
    )
    fbs = forms.ChoiceField(
        choices=FBS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_fbs'}),
        label='Fasting Blood Sugar > 120 mg/dl'
    )
    restecg = forms.ChoiceField(
        choices=RESTECG_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_restecg'}),
        label='Resting ECG Results'
    )
    thalach = forms.IntegerField(
        min_value=50, max_value=250,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'placeholder': 'e.g. 150',
            'id': 'id_thalach'
        }),
        label='Maximum Heart Rate Achieved (bpm)'
    )
    oldpeak = forms.FloatField(
        min_value=0.0, max_value=10.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'placeholder': 'e.g. 1.5', 'step': '0.1',
            'id': 'id_oldpeak'
        }),
        label='Oldpeak – ST Depression (mm)'
    )
