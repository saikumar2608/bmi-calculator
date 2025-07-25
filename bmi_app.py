import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- BMI thresholds by region ---
BMI_THRESHOLDS = {
    'General (WHO)': [(0, 18.5, 'Underweight', '🟡'), (18.5, 24.9, 'Normal', '🟢'), (25, 29.9, 'Overweight', '🟡'), (30, 100, 'Obese', '🔴')],
    'Asian (India/China)': [(0, 18.5, 'Underweight', '🟡'), (18.5, 22.9, 'Normal', '🟢'), (23, 24.9, 'Overweight', '🟡'), (25, 100, 'Obese', '🔴')],
    'Pacific Islander': [(0, 18.5, 'Underweight', '🟡'), (18.5, 26.9, 'Normal', '🟢'), (27, 31.9, 'Overweight', '🟡'), (32, 100, 'Obese', '🔴')],
    'Custom': [(0, 18.5, 'Underweight', '🟡'), (18.5, 24.9, 'Normal', '🟢'), (25, 29.9, 'Overweight', '🟡'), (30, 100, 'Obese', '🔴')]
}

# --- Input UI ---
st.title("BMI Calculator - RiskGuard Edition")

weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=70.0)
height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
region = st.selectbox("Ethnicity / Region", list(BMI_THRESHOLDS.keys()))

# --- Calculate BMI ---
height_m = height_cm / 100
bmi = round(weight / (height_m ** 2), 1)

# --- Interpretation ---
category = "Unknown"
emoji = ""
for low, high, label, icon in BMI_THRESHOLDS[region]:
    if low <= bmi <= high:
        category = label
        emoji = icon
        break

# --- Suggested normal weight range ---
normal_low = 18.5 * (height_m ** 2)
normal_high = 24.9 * (height_m ** 2)

# --- Display Results ---
st.metric("Your BMI", f"{bmi}", help="Body Mass Index")
st.write(f"**Interpretation ({region})**: {emoji} {category}")
st.write(f"Suggested normal weight range: **{normal_low:.1f} kg - {normal_high:.1f} kg**")

# --- Visual ---
fig, ax = plt.subplots(figsize=(6, 1.5))

# Draw colored background bars
for low, high, label, icon in BMI_THRESHOLDS[region]:
    ax.barh(0, high - low, left=low, height=0.5,
            color='green' if label == 'Normal' else 'orange' if label == 'Overweight' else 'red' if label == 'Obese' else 'gray', alpha=0.4)

# Mark user's BMI
ax.axvline(bmi, color='black', linestyle='--')
ax.text(bmi, 0.6, f'Your BMI: {bmi}', ha='center', fontsize=10, weight='bold')

# Clean up chart
ax.set_xlim(10, 45)
ax.set_yticks([])
ax.set_xticks(np.arange(10, 46, 5))
ax.set_title("BMI Category Visualization")

st.pyplot(fig)
