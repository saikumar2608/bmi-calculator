import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="BMI Calculator - RiskGuard Edition", layout="centered")
st.title("BMI Calculator - RiskGuard Edition")

# --- Weight input ---
weight_unit = st.radio("Select weight unit:", ["kg", "lbs"], horizontal=True)
if weight_unit == "kg":
    weight = st.number_input("Weight", 30.0, 250.0, 70.0, step=0.5)
else:
    weight_lbs = st.number_input("Weight", 66.0, 550.0, 154.3, step=1.0)
    weight = weight_lbs * 0.453592

# --- Height input ---
height_unit = st.radio("Select height unit:", ["cm", "feet+inches"], horizontal=True)
if height_unit == "cm":
    height = st.number_input("Height", 100.0, 250.0, 170.0, step=0.5)
else:
    feet = st.number_input("Feet", 3, 8, 5)
    inches = st.number_input("Inches", 0, 11, 7)
    height = ((feet * 12) + inches) * 2.54

# --- Optional Inputs ---
with st.expander("Optional Measurements"):
    waist = st.number_input("Waist Circumference (cm)", min_value=0.0, step=0.1)
    hip = st.number_input("Hip Circumference (cm)", min_value=0.0, step=0.1)
    whr = waist / hip if waist > 0 and hip > 0 else None
    gym_mode = st.checkbox("I have an athletic or muscular build")

# --- Region selector ---
region = st.selectbox("Ethnicity / Region", [
    "General (WHO)",
    "Asian (India/China)",
    "Pacific Islander",
    "Custom"
])

# --- BMI Calculation ---
bmi = weight / ((height / 100) ** 2)

# --- Region-wise interpretation ---
def interpret_bmi(bmi, region):
    if region == "General (WHO)":
        if bmi < 18.5:
            return "Underweight", "🟡"
        elif bmi < 25:
            return "Normal", "🟢"
        elif bmi < 30:
            return "Overweight", "🟡"
        else:
            return "Obese", "🔴"
    elif region == "Asian (India/China)":
        if bmi < 18.5:
            return "Underweight", "🟡"
        elif bmi < 23:
            return "Normal", "🟢"
        elif bmi < 27.5:
            return "Overweight", "🟡"
        else:
            return "Obese", "🔴"
    elif region == "Pacific Islander":
        if bmi < 26:
            return "Underweight", "🟡"
        elif bmi < 32:
            return "Normal", "🟢"
        else:
            return "Obese", "🔴"
    else:
        return "Custom Range", "🔵"

category, emoji = interpret_bmi(bmi, region)

# --- Ideal weight range ---
if region == "General (WHO)":
    low_bmi, high_bmi = 18.5, 24.9
elif region == "Asian (India/China)":
    low_bmi, high_bmi = 18.5, 22.9
elif region == "Pacific Islander":
    low_bmi, high_bmi = 26.0, 32.0
else:
    low_bmi, high_bmi = 18.5, 24.9  # default fallback

min_weight = round(low_bmi * ((height / 100) ** 2), 1)
max_weight = round(high_bmi * ((height / 100) ** 2), 1)

# --- Output display ---
st.metric("Your BMI", f"{bmi:.1f}")
interpretation = f"**Interpretation ({region})**: {emoji} {category}"

if gym_mode and bmi >= 25 and (whr is None or whr < 0.9) and (waist < 102 if waist > 0 else True):
    interpretation += "\n\n🧘 You mentioned having a muscular build. Your elevated BMI may be due to increased muscle mass, not excess fat."
elif bmi < 25 and ((waist >= 102) or (whr is not None and whr >= 0.9)):
    interpretation += "\n\n⚠️ Your BMI is in the normal range, but your waist or waist-to-hip ratio indicates increased abdominal fat."
elif bmi >= 25 and ((waist >= 102) or (whr is not None and whr >= 0.9)):
    interpretation += "\n\n🔴 You are overweight and also show signs of central obesity. This combination increases health risk."

st.markdown(interpretation)
st.markdown(f"Suggested normal weight range: **{min_weight} kg - {max_weight} kg**")
if whr:
    st.markdown(f"Waist-to-Hip Ratio: **{whr:.2f}**")

# --- Bar Visualization ---
def bmi_chart(bmi):
    fig, ax = plt.subplots(figsize=(7, 1.5))
    ax.barh(0, 40, color='white')

    # Colored zones
    ax.barh(0, low_bmi, color='lightblue')
    ax.barh(0, high_bmi - low_bmi, left=low_bmi, color='lightgreen')
    ax.barh(0, 40 - high_bmi, left=high_bmi, color='lightcoral')

    ax.axvline(bmi, color='black', linestyle='--', label=f'Your BMI: {bmi:.1f}')
    ax.set_xlim(10, 40)
    ax.set_yticks([])
    ax.set_xlabel('BMI')
    ax.legend()
    st.pyplot(fig)

bmi_chart(bmi)

# --- References and Disclaimer ---
with st.expander("References & Medical Disclaimer"):
    st.markdown("""
    **Sources:**
    - World Health Organization (WHO): [Waist Circumference and Waist-Hip Ratio Report (2008)](https://www.who.int/publications/i/item/9789241501491)
    - WHO BMI Classification: [Obesity and Overweight](https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight)
    - ICMR-NIN Dietary Guidelines for Indians: [PDF](https://www.nin.res.in/downloads/DietaryGuidelinesforIndians-Finaldraft.pdf)

    ⚠️ **Disclaimer**  
    This calculator provides general health risk estimation based on BMI and waist metrics.  
    It is not a substitute for clinical diagnosis. Please consult a healthcare provider for medical evaluation.
    """)
