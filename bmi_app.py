import streamlit as st

# --- BMI calculator ---
def calculate_bmi(height_cm, weight_kg):
    """
    Calculates Body Mass Index (BMI).

    Parameters:
    height_cm (float): Height in centimeters
    weight_kg (float): Weight in kilograms

    Returns:
    float: BMI rounded to 1 decimal place
    """
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)

def classify_bmi(bmi, ethnicity):
    """
    Classifies BMI into health categories based on ethnicity.

    Parameters:
    bmi (float): Body Mass Index
    ethnicity (str): 'General' or 'Asian'

    Returns:
    str: BMI category
    """
    if ethnicity.lower() == 'asian':
        if bmi < 18.5:
            return 'Underweight'
        elif bmi < 23:
            return 'Normal'
        elif bmi < 27.5:
            return 'Overweight'
        else:
            return 'Obese'
    else:
        if bmi < 18.5:
            return 'Underweight'
        elif bmi < 25:
            return 'Normal'
        elif bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'

def calculate_whtr(waist_cm, height_cm):
    """
    Calculates Waist-to-Height Ratio (WHtR).

    Parameters:
    waist_cm (float): Waist circumference in cm
    height_cm (float): Height in cm

    Returns:
    float: WHtR ratio rounded to 2 decimals
    """
    return round(waist_cm / height_cm, 2)

def assess_waist_only_risk(waist_cm, sex):
    """
    Assesses obesity risk using waist circumference alone.

    Parameters:
    waist_cm (float): Waist in cm
    sex (str): 'Male' or 'Female'

    Returns:
    str: Risk interpretation
    """
    if sex.lower() == 'male' and waist_cm > 102:
        return "High risk: Waist above 102 cm for males"
    elif sex.lower() == 'female' and waist_cm > 88:
        return "High risk: Waist above 88 cm for females"
    else:
        return "Waist circumference is within healthy range"

def estimate_body_fat(bmi, age, sex, is_muscular=False):
    """
    Estimates body fat % using BMI, age, and sex.

    Parameters:
    bmi (float): Body Mass Index
    age (int): Age of user
    sex (str): 'Male' or 'Female'
    is_muscular (bool): Whether user is muscular

    Returns:
    float: Estimated body fat %
    """
    sex_factor = 1 if sex.lower() == 'male' else 0
    body_fat = 1.20 * bmi + 0.23 * age - 10.8 * sex_factor - 5.4
    if is_muscular:
        body_fat = max(0, round(body_fat - 5, 1))
    return round(body_fat, 1)

# --- Streamlit UI ---
st.title(" Smart BMI & Obesity Risk Calculator")

st.markdown("This app calculates your BMI, body fat %, and waist-to-height ratio using medically validated formulas. Based on [CDC](https://www.cdc.gov/) and [WHO](https://www.who.int/) guidelines.")

# Height
height_option = st.radio(" How would you like to enter your height?", ['Feet', 'Centimeters', 'I don’t know'])
height_cm = None
if height_option == 'Feet':
    feet = st.number_input("Enter height in feet (e.g., 5.3)", min_value=1.0, step=0.1)
    height_cm = round(feet * 30.48, 1)
elif height_option == 'Centimeters':
    height_cm = st.number_input("Enter height in cm", min_value=50.0, step=0.1)

# Waist
waist_cm = None
if st.checkbox("Do you know your waist circumference?"):
    waist_cm = st.number_input("Enter your waist in cm", min_value=20.0, step=0.1)

# Weight
weight = st.number_input("Enter your weight", min_value=10.0, step=0.1)
weight_unit = st.selectbox("Weight Unit", ['kg', 'lbs'])
if weight_unit == 'lbs':
    weight = round(weight * 0.453592, 1)

# Ethnicity & sex
ethnicity = st.selectbox("Ethnicity", ['General', 'Asian'])
sex = st.selectbox("Biological Sex", ['Male', 'Female'])

# Show results
if st.button("Calculate My Health Metrics"):
    if height_cm:
        bmi = calculate_bmi(height_cm, weight)
        category = classify_bmi(bmi, ethnicity)
        st.success(f" Your BMI is: {bmi} — {category}")

        if waist_cm:
            whtr = calculate_whtr(waist_cm, height_cm)
            st.info(f" Waist-to-Height Ratio (WHtR): {whtr}")

    elif waist_cm:
        risk = assess_waist_only_risk(waist_cm, sex)
        st.warning(f" {risk}")

# Optional Body Fat %
if height_cm and st.checkbox("Estimate my Body Fat %"):
    age = st.number_input("Enter your age", min_value=10, max_value=100)
    is_muscular = st.checkbox("Are you muscular or athletic?")
    bmi = calculate_bmi(height_cm, weight)
    bf = estimate_body_fat(bmi, age, sex, is_muscular)
    st.success(f" Estimated Body Fat %: {bf}%")
