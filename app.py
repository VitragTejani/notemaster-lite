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
        "hypertension": {
            "title": "Internal Medicine: Hypertension Follow-Up",
            "case_details": [
                ("Patient", "58F visiting clinic for BP follow-up."),
                ("Chief Complaint", "\"I'm here for my regular BP check.\""),
                ("HPI", "No symptoms. Taking meds regularly."),
                ("PMH", "Hypertension, Hyperlipidemia"),
                ("Medications", "Amlodipine, Atorvastatin"),
                ("Allergies", "None"),
                ("Vitals", "BP 150/95, HR 80 bpm"),
                ("Exam", "Normal cardio and lungs."),
                ("Labs", "Na/K normal, Creatinine 1.0"),
            ],
            "model_answer": {
                "subjective": "58F here for routine hypertension follow-up. Asymptomatic, taking meds daily. (Simple, direct summary.)",
                "objective": "BP 150/95, HR 80 bpm. Normal cardio-pulmonary exam. Recent labs normal. (Vitals, key exam, labs.)",
                "assessment": "Sub-optimally controlled hypertension. (Clear diagnosis.)",
                "plan": "Increase amlodipine to 10 mg daily. Counsel on low-salt diet, recheck BP in 2 weeks. (Plan and lifestyle advice.)",
                "pro_tip": "Example: \"58F here for hypertension follow-up, BP still 150/95 despite meds. Increasing amlodipine and providing lifestyle counseling.\""
            }
        },
        "uti": {
            "title": "Family Medicine: Urinary Tract Infection",
            "case_details": [
                ("Patient", "25F with dysuria and urinary frequency."),
                ("Chief Complaint", "\"I feel burning when I pee.\""),
                ("HPI", "2 days of dysuria and frequency, no fever, no flank pain."),
                ("PMH", "None"),
                ("Vitals", "Temp 37°C, HR 82 bpm"),
                ("Exam", "Mild suprapubic tenderness. No CVA tenderness."),
                ("Labs", "UA: +LE, +nitrites"),
            ],
            "model_answer": {
                "subjective": "25F with 2-day history of dysuria and frequency. No fever or flank pain. (Focused symptoms.)",
                "objective": "Temp 37°C, mild suprapubic tenderness. UA: +LE, +nitrites. (Key exam and labs.)",
                "assessment": "Uncomplicated lower UTI. (Specific diagnosis.)",
                "plan": "Nitrofurantoin 100 mg BID for 5 days. Increase fluids. (Simple treatment plan.)",
                "pro_tip": "Example: \"25F with dysuria, UA positive. UTI confirmed. Starting nitrofurantoin.\""
            }
        },
        "appendicitis": {
            "title": "Emergency Medicine: Suspected Appendicitis",
            "case_details": [
                ("Patient", "20M with RLQ pain."),
                ("Chief Complaint", "\"My belly hurts, especially on the right.\""),
                ("HPI", "1 day of periumbilical pain migrating to RLQ and nausea. No diarrhea."),
                ("Vitals", "Temp 38°C, HR 100 bpm"),
                ("Exam", "Tenderness and guarding RLQ. Positive Rovsing sign."),
                ("Labs", "WBC 13,500/mm³"),
            ],
            "model_answer": {
                "subjective": "20M with 1-day history of RLQ pain and nausea. (Classic presentation.)",
                "objective": "Temp 38°C, RLQ tenderness and guarding. WBC 13.5k. (Key findings.)",
                "assessment": "Suspected acute appendicitis. (Direct diagnosis.)",
                "plan": "NPO, IV fluids, analgesia, surgical consult, CT abdomen. (Management steps.)",
                "pro_tip": "Example: \"20M with RLQ pain, guarding, WBC high. Likely appendicitis. Consulting surgery, prepping CT.\""
            }
        },
        "peds_rash": {
            "title": "Pediatrics: Fever and Rash",
            "case_details": [
                ("Patient", "5Y male with fever and rash."),
                ("Chief Complaint", "\"My child has had fever and spots for 2 days.\""),
                ("HPI", "Fever 39°C, red rash on face and trunk, runny nose, cough."),
                ("Immunizations", "Not up to date."),
                ("Exam", "Maculopapular rash and Koplik spots."),
            ],
            "model_answer": {
                "subjective": "5Y boy with 2 days of fever, cough, runny nose, and rash. (Clear summary.)",
                "objective": "Temp 39°C, maculopapular rash face and trunk, Koplik spots. (Key findings.)",
                "assessment": "Clinical measles. (Spot diagnosis.)",
                "plan": "Supportive care, Vitamin A, notify public health. (Management.)",
                "pro_tip": "Example: \"5Y with fever, rash, Koplik spots. Measles diagnosis. Supportive care, Vitamin A, and report.\""
            }
        },
        "depression": {
            "title": "Psychiatry: Depression Evaluation",
            "case_details": [
                ("Patient", "30F reporting low mood."),
                ("Chief Complaint", "\"I feel sad and tired all the time.\""),
                ("HPI", "2 months of low mood, poor sleep and appetite, difficulty concentrating. No suicidal ideation."),
                ("PMH", "None"),
                ("Vitals", "Normal"),
                ("Exam", "Flat affect."),
                ("Screening", "PHQ-9: 16 (moderate depression)"),
            ],
            "model_answer": {
                "subjective": "30F with 2 months of low mood, poor sleep and appetite, difficulty concentrating. No suicidality. (Classic depression.)",
                "objective": "Flat affect, PHQ-9 score 16. (Screening and exam.)",
                "assessment": "Moderate major depressive disorder. (Diagnosis.)",
                "plan": "Start SSRI (sertraline 50 mg daily), offer CBT referral, safety plan. (Treatment plan.)",
                "pro_tip": "Example: \"30F with moderate MDD. Starting sertraline and referring for CBT.\""
            }
        }
    }

    case_data = cases.get(case_type, cases['pneumonia'])

    if request.method == 'POST':
        subjective = request.form.get('subjective')
        objective = request.form.get('objective')
        assessment = request.form.get('assessment')
        plan = request.form.get('plan')

        return render_template('soap_note.html', case=case_data, show_answer=True)

    return render_template('soap_note.html', case=case_data, show_answer=False)


if __name__ == '__main__':
    app.run(debug=True)