#  Smart BMI & Obesity Risk Calculator

A simple yet powerful health tool built using **Python** and **Streamlit**, based on **CDC** and **WHO** guidelines — to help users estimate:
- Body Mass Index (BMI)
- Waist-to-Height Ratio (WHtR)
- Body Fat Percentage (optional)
- Obesity risk (based on ethnicity, age, and sex)

---

##  Try it Live!

👉 [Click to Use the App](https://bmi-calculator-el2g9y7qq8xegfv29ynkk7.streamlit.app/)


---

##  Features

✅ Ethnicity-based BMI classification (General vs. Asian)  
✅ Waist-to-Height Ratio using WHO thresholds  
✅ Optional Body Fat % estimation using BMI, age & sex  
✅ Visceral fat risk from waist circumference  
✅ Muscularity adjustment  
✅ Built with CDC-backed logic  
✅ User-friendly CLI & Streamlit frontend
![Screenshot 2025-07-09 142053](https://github.com/user-attachments/assets/487ec972-000f-46ea-b266-dc5e36912537)
![image](https://github.com/user-attachments/assets/55815b48-3469-4de8-88a1-49dd945f92e9)


---

## 🛠 Tech Stack

- `Python 3`
- `Streamlit`
- `matplotlib`

---

##  Installation

If you want to run locally:

```bash
git clone https://github.com/saikumar2608/bmi-calculator.git
cd bmi-calculator
pip install -r requirements.txt
streamlit run bmi_app.py
