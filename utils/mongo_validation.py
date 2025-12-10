from datetime import datetime

def validate_allergy(allergen, severity, date_added):
    if not allergen or not allergen.strip():
        raise ValueError('Allergen is required')
    
    valid_severities = ['Mild', 'Moderate', 'Severe']
    if not severity or severity not in valid_severities:
        raise ValueError('Invalid severity selection')
    
    if not date_added:
        raise ValueError('Date added is required')
    
    try:
        datetime.strptime(date_added, '%Y-%m-%d')
    except ValueError:
        raise ValueError('Invalid date format')
    
    return True

def validate_assessment(hypertension, ever_married, work_type, residence_type, 
                       avg_glucose_level, bmi, smoking_status, stroke):
    if hypertension not in ['0', '1']:
        raise ValueError('Hypertension must be 0 or 1')
    
    if ever_married not in ['No', 'Yes']:
        raise ValueError('Ever married must be No or Yes')
    
    valid_work_types = ['Children', 'Govt_job', 'Never_worked', 'Private', 'Self-employed']
    if work_type not in valid_work_types:
        raise ValueError('Invalid work type')
    
    if residence_type not in ['Rural', 'Urban']:
        raise ValueError('Residence type must be Rural or Urban')
    
    try:
        glucose = float(avg_glucose_level)
        if glucose < 0 or glucose > 300:
            raise ValueError('Average glucose level must be between 0 and 300')
    except ValueError:
        raise ValueError('Invalid glucose level')
    
    try:
        bmi_val = float(bmi)
        if bmi_val < 10 or bmi_val > 100:
            raise ValueError('BMI must be between 10 and 100')
    except ValueError:
        raise ValueError('Invalid BMI')
    
    valid_smoking = ['Formerly smoked', 'Never smoked', 'Smokes', 'Unknown']
    if smoking_status not in valid_smoking:
        raise ValueError('Invalid smoking status')
    
    if stroke not in ['0', '1']:
        raise ValueError('Stroke must be 0 or 1')
    
    return True