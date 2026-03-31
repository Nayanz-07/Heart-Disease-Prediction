from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Hardcoded hospital data – replace with DB entries after running migrations
HOSPITALS = [
    {"name": "All India Institute of Medical Sciences (AIIMS)", "city": "New Delhi", "state": "Delhi",
     "specialization": "Cardiology, Cardiac Surgery, Multi-Speciality", "contact": "+91-11-26588500",
     "email": "director@aiims.edu", "beds": 2478, "rating": 4.9},
    {"name": "Apollo Hospitals", "city": "Chennai", "state": "Tamil Nadu",
     "specialization": "Interventional Cardiology, Heart Transplant, Cardiac ICU", "contact": "+91-44-28293333",
     "email": "info@apollohospitals.com", "beds": 1000, "rating": 4.8},
    {"name": "Fortis Escorts Heart Institute", "city": "New Delhi", "state": "Delhi",
     "specialization": "Cardiac Surgery, Angioplasty, Pacemaker Implantation", "contact": "+91-11-47135000",
     "email": "fehi@fortishealthcare.com", "beds": 310, "rating": 4.8},
    {"name": "Narayana Health (NH) – Rabindranath Tagore International", "city": "Kolkata", "state": "West Bengal",
     "specialization": "Cardiac Bypass, Pediatric Cardiology, Heart Failure", "contact": "+91-33-71220000",
     "email": "rtiics@narayanahealth.org", "beds": 450, "rating": 4.7},
    {"name": "Medanta – The Medicity", "city": "Gurugram", "state": "Haryana",
     "specialization": "Heart Transplant, Robotic Cardiac Surgery, Electrophysiology", "contact": "+91-124-4141414",
     "email": "info@medanta.org", "beds": 1500, "rating": 4.8},
    {"name": "Kokilaben Dhirubhai Ambani Hospital", "city": "Mumbai", "state": "Maharashtra",
     "specialization": "Cardiac Catheterization, Valve Replacement, Arrhythmia", "contact": "+91-22-30999999",
     "email": "info@kokilabenhospital.com", "beds": 750, "rating": 4.7},
    {"name": "Sri Jayadeva Institute of Cardiovascular Sciences", "city": "Bengaluru", "state": "Karnataka",
     "specialization": "Cardiology, Cardiac Surgery, Cardiac Rehabilitation", "contact": "+91-80-22977777",
     "email": "info@jayadevacardiology.com", "beds": 1000, "rating": 4.8},
    {"name": "Christian Medical College (CMC)", "city": "Vellore", "state": "Tamil Nadu",
     "specialization": "Congenital Heart Disease, Cardiothoracic Surgery", "contact": "+91-416-2281000",
     "email": "cardiaccmc@cmcvellore.ac.in", "beds": 2600, "rating": 4.9},
    {"name": "Amrita Institute of Medical Sciences", "city": "Kochi", "state": "Kerala",
     "specialization": "Heart Transplant, Cardiac Electrophysiology, TAVR", "contact": "+91-484-2801234",
     "email": "cardiology@aims.amrita.edu", "beds": 1350, "rating": 4.7},
    {"name": "Wockhardt Hospital", "city": "Mumbai", "state": "Maharashtra",
     "specialization": "Minimally Invasive Heart Surgery, Stenting, Bypass", "contact": "+91-22-26558888",
     "email": "info@wockhardthospitals.com", "beds": 300, "rating": 4.5},
    {"name": "Max Super Speciality Hospital", "city": "New Delhi", "state": "Delhi",
     "specialization": "Coronary Artery Disease, Heart Failure, Valve Disease", "contact": "+91-11-26515050",
     "email": "info@maxhealthcare.in", "beds": 500, "rating": 4.6},
    {"name": "Manipal Hospital", "city": "Bengaluru", "state": "Karnataka",
     "specialization": "Cardiac Surgery, Cardiac Imaging, Preventive Cardiology", "contact": "+91-80-25024444",
     "email": "info@manipalhospitals.com", "beds": 600, "rating": 4.6},
    {"name": "NIMHANS & Narayana Multispeciality Hospital", "city": "Mysuru", "state": "Karnataka",
     "specialization": "Cardiology, Neuro-Cardiac Care", "contact": "+91-821-2440020",
     "email": "contact@narayanahealth.org", "beds": 200, "rating": 4.4},
    {"name": "KIMS – Krishna Institute of Medical Sciences", "city": "Hyderabad", "state": "Telangana",
     "specialization": "Cardiac Cath Lab, Heart Failure Clinic, EP Lab", "contact": "+91-40-44885000",
     "email": "info@kimshospitals.com", "beds": 1000, "rating": 4.6},
    {"name": "Lilavati Hospital and Research Centre", "city": "Mumbai", "state": "Maharashtra",
     "specialization": "Interventional Cardiology, Preventive Cardiology", "contact": "+91-22-26751000",
     "email": "info@lilavatihospital.com", "beds": 323, "rating": 4.5},
]


@login_required
def hospitals_list(request):
    """Display list of top cardiac hospitals in India."""
    query = request.GET.get('q', '').strip()
    state_filter = request.GET.get('state', '').strip()

    hospitals = HOSPITALS

    if query:
        hospitals = [h for h in hospitals if
                     query.lower() in h['name'].lower() or
                     query.lower() in h['city'].lower()]

    if state_filter:
        hospitals = [h for h in hospitals if
                     state_filter.lower() in h['state'].lower()]

    states = sorted(set(h['state'] for h in HOSPITALS))

    return render(request, 'hospitals/hospitals.html', {
        'hospitals': hospitals,
        'query': query,
        'state_filter': state_filter,
        'states': states,
        'total': len(hospitals),
    })
