from django.db import models
from django.contrib.auth.models import User


class PredictionRecord(models.Model):
    """Store each prediction made by a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')

    # Input features
    age = models.IntegerField()
    sex = models.IntegerField()             # 0=Female, 1=Male
    cp = models.IntegerField()              # Chest pain type 0-3
    trestbps = models.IntegerField()        # Resting blood pressure
    chol = models.IntegerField()            # Serum cholesterol
    fbs = models.IntegerField()             # Fasting blood sugar >120 mg/dl
    restecg = models.IntegerField()         # Resting ECG results 0-2
    thalach = models.IntegerField()         # Maximum heart rate achieved
    oldpeak = models.FloatField()           # ST depression induced by exercise

    # Output
    prediction = models.IntegerField()      # 0=No Disease, 1=Disease
    probability = models.FloatField()       # Probability of disease (0–1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        result = "Heart Disease" if self.prediction == 1 else "No Disease"
        return f"{self.user.username} | {result} | {self.created_at.strftime('%Y-%m-%d')}"

    @property
    def result_label(self):
        return "Heart Disease Detected" if self.prediction == 1 else "No Heart Disease"

    @property
    def risk_level(self):
        if self.probability >= 0.75:
            return "High Risk"
        elif self.probability >= 0.50:
            return "Moderate Risk"
        else:
            return "Low Risk"
