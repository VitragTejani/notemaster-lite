from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/simulate', methods=['GET', 'POST'])
def simulate():
    case_type = request.args.get('case', 'pneumonia')  # default to pneumonia if nothing selected

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
                "subjective": "65M with 3-day history of fever and productive cough. Denies chest pain or SOB.",
                "objective": "Temp 38.5°C, HR 95 bpm, BP 130/80, RR 20. Crackles RLL. WBC 14k. CXR shows RLL infiltrate.",
                "assessment": "Community-acquired pneumonia, likely RLL.",
                "plan": "IV ceftriaxone and azithromycin. Monitor vitals, encourage fluids, repeat CXR in 48h.",
                "pro_tip": "Example: '65M with 3-day productive cough, febrile, crackles RLL, CXR infiltrate. CAP likely.'"
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
                "subjective": "58F here for routine hypertension follow-up. Asymptomatic, taking meds daily.",
                "objective": "BP 150/95, HR 80 bpm. Normal cardio-pulmonary exam. Recent labs normal.",
                "assessment": "Sub-optimally controlled hypertension.",
                "plan": "Increase amlodipine to 10 mg daily. Counsel on low-salt diet, recheck BP in 2 weeks.",
                "pro_tip": "Example: '58F here for hypertension follow-up, BP still 150/95 despite meds. Increasing amlodipine.'"
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
                "subjective": "25F with 2-day history of dysuria and frequency. No fever or flank pain.",
                "objective": "Temp 37°C, mild suprapubic tenderness. UA: +LE, +nitrites.",
                "assessment": "Uncomplicated lower UTI.",
                "plan": "Nitrofurantoin 100 mg BID for 5 days. Increase fluids.",
                "pro_tip": "Example: '25F with dysuria, UA positive. UTI confirmed. Starting nitrofurantoin.'"
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
                "subjective": "20M with 1-day history of RLQ pain and nausea.",
                "objective": "Temp 38°C, RLQ tenderness and guarding. WBC 13.5k.",
                "assessment": "Suspected acute appendicitis.",
                "plan": "NPO, IV fluids, analgesia, surgical consult, CT abdomen.",
                "pro_tip": "Example: '20M with RLQ pain, guarding, WBC high. Likely appendicitis. Consulting surgery.'"
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
                "subjective": "5Y boy with 2 days of fever, cough, runny nose, and rash.",
                "objective": "Temp 39°C, maculopapular rash face and trunk, Koplik spots.",
                "assessment": "Clinical measles.",
                "plan": "Supportive care, Vitamin A, notify public health.",
                "pro_tip": "Example: '5Y with fever, rash, Koplik spots. Measles diagnosis. Supportive care, Vitamin A.'"
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
                "subjective": "30F with 2 months of low mood, poor sleep and appetite, difficulty concentrating. No suicidality.",
                "objective": "Flat affect, PHQ-9 score 16.",
                "assessment": "Moderate major depressive disorder.",
                "plan": "Start SSRI (sertraline 50 mg daily), offer CBT referral, safety plan.",
                "pro_tip": "Example: '30F with moderate MDD. Starting sertraline and referring for CBT.'"
            }
        },

        # ... add new cases below
        "diabetes_followup": {
        "title": "Internal Medicine: Diabetes Mellitus Follow-Up",
        "case_details": [
            ("Patient", "60F attending diabetes follow-up."),
            ("Chief Complaint", "\"Here for my sugar check.\""),
            ("HPI", "Diabetes for 10 years, controlled on metformin. No current symptoms."),
            ("PMH", "Diabetes, Hypertension"),
            ("Medications", "Metformin 1000 mg BID, Lisinopril 20 mg"),
            ("Vitals", "BP 130/80, HR 76 bpm"),
            ("Labs", "HbA1c: 7.8% last month"),
            ("Exam", "Normal foot exam, no retinopathy."),
        ],
        "model_answer": {
            "subjective": "60F with T2DM follow-up, asymptomatic, adherent to meds.",
            "objective": "BP 130/80, HbA1c 7.8%. Normal foot and retina exams.",
            "assessment": "T2DM, moderately controlled.",
            "plan": "Reinforce diet, increase metformin if tolerated, plan HbA1c in 3 months.",
            "pro_tip": "Example: \"60F with T2DM, HbA1c 7.8%. Reinforcing lifestyle, adjusting metformin.\""
        }
    },

    "low_back_pain": {
        "title": "Family Medicine: Acute Low Back Pain",
        "case_details": [
            ("Patient", "40M with 5-day low back pain."),
            ("Chief Complaint", "\"I hurt my back lifting boxes.\""),
            ("HPI", "Onset after lifting heavy object. No radiating pain, no weakness."),
            ("PMH", "None"),
            ("Vitals", "Normal"),
            ("Exam", "Tender lumbar paraspinal muscles, no neurological deficits."),
        ],
        "model_answer": {
            "subjective": "40M with 5 days of low back pain after lifting. No red flags.",
            "objective": "Tender lumbar paraspinals. No neuro deficits.",
            "assessment": "Mechanical low back pain.",
            "plan": "NSAIDs, heat therapy, advise gentle activity. No imaging needed now.",
            "pro_tip": "Example: \"40M with acute back pain, no red flags. Mechanical LBP. NSAIDs + activity advice.\""
        }
    },

    "hyperlipidemia": {
        "title": "Family Medicine: Hyperlipidemia Management",
        "case_details": [
            ("Patient", "55M during annual physical."),
            ("Chief Complaint", "\"No complaints, just my yearly check.\""),
            ("HPI", "Asymptomatic."),
            ("PMH", "Hypertension"),
            ("Vitals", "BP 128/78"),
            ("Labs", "LDL 165 mg/dL"),
            ("Exam", "Unremarkable."),
        ],
        "model_answer": {
            "subjective": "55M asymptomatic at annual physical.",
            "objective": "BP 128/78. LDL 165 mg/dL.",
            "assessment": "Primary hyperlipidemia.",
            "plan": "Start atorvastatin 20 mg daily. Lifestyle counseling.",
            "pro_tip": "Example: \"55M with LDL 165. Starting atorvastatin + diet advice.\""
        }
    },

    "uri": {
        "title": "Family Medicine: Upper Respiratory Infection",
        "case_details": [
            ("Patient", "28F with sore throat and runny nose."),
            ("Chief Complaint", "\"I’ve had a sore throat and stuffy nose for 3 days.\""),
            ("HPI", "No fever, no shortness of breath. Occasional cough."),
            ("PMH", "None"),
            ("Vitals", "Temp 37.2°C, HR 80 bpm"),
            ("Exam", "Mildly erythematous throat, clear lungs."),
        ],
        "model_answer": {
            "subjective": "28F with 3-day sore throat, nasal congestion. No fever or SOB.",
            "objective": "Temp 37.2°C, mild pharyngeal erythema, clear lungs.",
            "assessment": "Viral URI.",
            "plan": "Supportive care: fluids, rest, OTC symptom relief.",
            "pro_tip": "Example: \"28F with viral URI, no red flags. Supportive care advised.\""
        }
    },

    "otitis_media": {
        "title": "Pediatrics: Acute Otitis Media",
        "case_details": [
            ("Patient", "3Y girl with ear pain."),
            ("Chief Complaint", "\"She’s tugging at her ear and crying.\""),
            ("HPI", "2 days of ear pain, fever 38.2°C."),
            ("Vitals", "Temp 38.2°C"),
            ("Exam", "Bulging, erythematous right tympanic membrane."),
        ],
        "model_answer": {
            "subjective": "3Y girl with 2-day ear pain and fever.",
            "objective": "Temp 38.2°C, bulging red TM (right).",
            "assessment": "Acute otitis media (right ear).",
            "plan": "Amoxicillin 80–90 mg/kg/day divided BID x10 days. Symptom relief.",
            "pro_tip": "Example: \"3Y with AOM. Starting amoxicillin + pain relief.\""
        }
    },

    "well_child_2yo": {
        "title": "Pediatrics: Well-Child Check (2-Year-Old)",
        "case_details": [
            ("Patient", "2Y boy for routine check-up."),
            ("Chief Complaint", "\"He’s doing fine.\""),
            ("HPI", "No concerns, meeting milestones."),
            ("Vitals", "Weight and height at 50th percentile."),
            ("Exam", "Normal physical exam."),
            ("Immunizations", "Due for Hep A and MMR dose 2."),
        ],
        "model_answer": {
            "subjective": "2Y boy here for routine well-child visit. No parental concerns.",
            "objective": "Normal growth and development. Vitals WNL.",
            "assessment": "Healthy 2Y old, up-to-date on milestones.",
            "plan": "Administer Hep A and MMR vaccines. Anticipatory guidance.",
            "pro_tip": "Example: \"2Y well-child, normal exam. Gave vaccines, advised parents.\""
        }
    }
}

    case_data = cases.get(case_type, cases['pneumonia'])

    if request.method == 'POST':
        subjective = request.form.get('subjective')
        objective = request.form.get('objective')
        assessment = request.form.get('assessment')
        plan = request.form.get('plan')

        user_answer = {
            "subjective": subjective,
            "objective": objective,
            "assessment": assessment,
            "plan": plan
        }

        return render_template('soap_note.html', case=case_data, show_answer=True, user_answer=user_answer)

    return render_template('soap_note.html', case=case_data, show_answer=False)


if __name__ == '__main__':
    app.run(debug=True)
