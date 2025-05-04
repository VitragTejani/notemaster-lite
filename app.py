from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/simulate', methods=['GET', 'POST'])
def simulate():
    case_type = request.args.get('case', 'pneumonia')  # default to pneumonia if nothing selected

    # Define clinical cases + model answers
    cases = {
        "pneumonia": {
            "title": "Internal Medicine: Pneumonia",
            "case_details": [
                ("Patient", "65M admitted with fever and productive cough."),
                ("Chief Complaint", "\"I've had a fever and cough for 3 days.\""),
                ("HPI", "3 days of productive cough (yellow sputum) and intermittent fever. No chest pain or SOB."),
                ("PMH", "Hypertension, Diabetes Mellitus"),
                ("Medications", "Lisinopril, Metformin"),
                ("Allergies", "NKDA"),
                ("Social History", "Retired teacher, never smoked, no alcohol use."),
                ("Vitals", "Temp 38.5°C, HR 95 bpm, BP 130/80, RR 20, SpO2 97%"),
                ("Exam", "Crackles in RLL. No wheezes."),
                ("Labs", "WBC 14,000/mm³"),
                ("CXR", "Right lower lobe infiltrate.")
            ],
            "model_answer": {
                "subjective": "65M with 3-day history of fever and productive cough. Denies chest pain or SOB. (Clear summary of chief complaint and relevant negatives.)",
                "objective": "Temp 38.5°C, HR 95 bpm, BP 130/80, RR 20. Crackles RLL. WBC 14k. CXR shows RLL infiltrate. (Focused on vitals, exam, labs.)",
                "assessment": "Community-acquired pneumonia, likely RLL. (Specific diagnosis and location.)",
                "plan": "IV ceftriaxone and azithromycin. Monitor vitals, encourage fluids, repeat CXR in 48h. (Treatment and follow-up.)",
                "pro_tip": "Example: \"65M with 3-day productive cough, febrile, crackles RLL, CXR infiltrate. CAP likely. Starting ceftriaxone and azithromycin.\""
            }
        },
        # ... (rest of your cases stay unchanged)
        # [Hypertension, UTI, Appendicitis, Peds Rash, Depression as you already have them]
    }

    case_data = cases.get(case_type, cases['pneumonia'])

    if request.method == 'POST':
        subjective = request.form.get('subjective')
        objective = request.form.get('objective')
        assessment = request.form.get('assessment')
        plan = request.form.get('plan')

        # ✅ NEW: Pass user answers to the template too
        return render_template(
            'soap_note.html',
            case=case_data,
            show_answer=True,
            user_answer={
                'subjective': subjective,
                'objective': objective,
                'assessment': assessment,
                'plan': plan
            }
        )

    return render_template('soap_note.html', case=case_data, show_answer=False)


if __name__ == '__main__':
    app.run(debug=True)
    