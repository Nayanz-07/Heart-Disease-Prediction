import os
import json
import joblib
import numpy as np
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .forms import PredictionForm
from .models import PredictionRecord

# ── Load ML model & scaler at startup ──────────────────────────────────────
MODEL_DIR = os.path.join(settings.BASE_DIR, 'prediction', 'ml_model')

def _load_artifact(filename):
    path = os.path.join(MODEL_DIR, filename)
    if os.path.exists(path):
        return joblib.load(path)
    return None

MODEL   = _load_artifact('heart_model.pkl')
SCALER  = _load_artifact('scaler.pkl')
FEATURES = _load_artifact('features.pkl') or [
    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'oldpeak'
]

# ── Recommendation data ─────────────────────────────────────────────────────
RECOMMENDATIONS_HIGH_RISK = {
    'medicines': [
        ('Aspirin', 'Blood thinner – reduces clot risk (consult doctor)'),
        ('Statins (e.g. Atorvastatin)', 'Lowers LDL cholesterol'),
        ('Beta-blockers', 'Reduces heart rate and blood pressure'),
        ('ACE Inhibitors', 'Relaxes blood vessels, lowers BP'),
        ('Nitroglycerin', 'Relieves chest pain / angina'),
    ],
    'foods': [
        ('Oats & Whole Grains', 'Lowers bad cholesterol'),
        ('Fatty Fish (Salmon, Sardines)', 'Rich in Omega-3 fatty acids'),
        ('Leafy Greens (Spinach, Kale)', 'High in antioxidants and nitrates'),
        ('Berries', 'Reduce blood pressure and inflammation'),
        ('Avocados', 'Healthy monounsaturated fats'),
        ('Nuts & Seeds', 'Heart-healthy fats and fibre'),
        ('Dark Chocolate (70%+)', 'Flavonoids reduce blood pressure'),
        ('Garlic & Turmeric', 'Natural anti-inflammatory'),
    ],
    'routine': [
        '🌅 Wake up by 6:00 AM – start day with a glass of warm water',
        '🧘 10–15 min of meditation or deep breathing exercises',
        '🚶 30–45 min brisk walk or light cardio every morning',
        '🥣 Eat a healthy low-sodium breakfast by 8:00 AM',
        '💊 Take prescribed medicines as per doctor schedule',
        '🥗 Light, balanced lunch; avoid oily/fried foods',
        '😴 Afternoon rest (15–20 min) if needed',
        '🚴 Light exercise / yoga in the evening (30 min)',
        '🍵 Herbal tea (green tea / chamomile) instead of coffee',
        '📵 Reduce screen time 1 hour before bed',
        '🌙 Sleep by 10:00 PM – 7–8 hours of quality sleep',
    ],
    'exercise': [
        ('Brisk Walking', '30 min daily – best beginner cardio'),
        ('Swimming', 'Low-impact, excellent for heart'),
        ('Cycling', '20–30 min, moderate pace'),
        ('Yoga / Pranayama', 'Reduces stress and BP'),
        ('Light Strength Training', '2–3 times/week with doctor approval'),
        ('Deep Breathing', '5 min daily – Anulom Vilom'),
    ],
}

RECOMMENDATIONS_LOW_RISK = {
    'medicines': [
        ('No immediate medication required', 'Maintain healthy lifestyle'),
        ('Multivitamins (if deficient)', 'Consult a nutritionist'),
        ('Omega-3 Supplements', 'Beneficial for heart health'),
    ],
    'foods': [
        ('Fresh Fruits & Vegetables', 'Rich in vitamins and minerals'),
        ('Whole Grains', 'Fibre for good cholesterol'),
        ('Lean Protein (Chicken, Lentils)', 'Muscle maintenance'),
        ('Low-fat Dairy', 'Calcium without excess fat'),
        ('Green Tea', 'Antioxidants for heart health'),
        ('Nuts (Almonds, Walnuts)', 'Healthy fats in moderation'),
    ],
    'routine': [
        '🌅 Wake up by 6:30 AM and hydrate well',
        '🏃 30 min of any physical activity you enjoy',
        '🥗 Balanced, home-cooked meals throughout the day',
        '💧 Drink 8–10 glasses of water daily',
        '🧘 Practice stress management – hobby, reading, music',
        '🚭 Avoid smoking and limit alcohol',
        '🌙 Sleep 7–8 hours every night',
    ],
    'exercise': [
        ('Jogging / Running', '20–30 min daily'),
        ('Cycling or Swimming', 'Great cardiovascular activity'),
        ('Gym / Weight Training', '3–4 times/week'),
        ('Sports (Badminton, Tennis)', 'Fun and effective'),
        ('Yoga', 'Flexibility and mental wellness'),
    ],
}


@login_required
def home(request):
    """Main dashboard with info, prediction form, and results."""
    form = PredictionForm()
    context = {
        'form': form,
        'user': request.user,
        'recent_predictions': PredictionRecord.objects.filter(
            user=request.user
        )[:5],
    }
    return render(request, 'prediction/home.html', context)


@login_required
def predict(request):
    """Handle prediction form submission via AJAX or POST."""
    if request.method != 'POST':
        return redirect('prediction:home')

    form = PredictionForm(request.POST)

    if not form.is_valid():
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Invalid form data', 'errors': form.errors}, status=400)
        return redirect('prediction:home')

    # ── Extract features in model order ─────────────────────────────────────
    data = form.cleaned_data
    feature_values = [float(data[f]) for f in FEATURES]
    X = np.array([feature_values])

    # ── Predict ──────────────────────────────────────────────────────────────
    if MODEL is None or SCALER is None:
        # Model not trained yet – return a demo response
        prediction, probability = 0, 0.15
    else:
        X_scaled  = SCALER.transform(X)
        prediction = int(MODEL.predict(X_scaled)[0])
        probability = float(MODEL.predict_proba(X_scaled)[0][1])

    # ── Save record ──────────────────────────────────────────────────────────
    record = PredictionRecord.objects.create(
        user=request.user,
        age=data['age'], sex=data['sex'], cp=data['cp'],
        trestbps=data['trestbps'], chol=data['chol'], fbs=data['fbs'],
        restecg=data['restecg'], thalach=data['thalach'], oldpeak=data['oldpeak'],
        prediction=prediction, probability=probability,
    )

    # ── Build recommendations ─────────────────────────────────────────────────
    recs = RECOMMENDATIONS_HIGH_RISK if prediction == 1 else RECOMMENDATIONS_LOW_RISK

    result = {
        'prediction': prediction,
        'probability': round(probability * 100, 1),
        'result_label': record.result_label,
        'risk_level': record.risk_level,
        'medicines': recs['medicines'],
        'foods': recs['foods'],
        'routine': recs['routine'],
        'exercise': recs['exercise'],
        'record_id': record.id,
    }

    # AJAX request → JSON response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(result)

    # Normal POST → render with results
    return render(request, 'prediction/home.html', {
        'form': PredictionForm(),
        'result': result,
        'user': request.user,
        'recent_predictions': PredictionRecord.objects.filter(user=request.user)[:5],
    })


@login_required
def history(request):
    """Show prediction history for the logged-in user."""
    records = PredictionRecord.objects.filter(user=request.user)
    return render(request, 'prediction/history.html', {
        'records': records,
        'user': request.user,
    })


