import streamlit as st
from gtts import gTTS
import base64
import tempfile

# ✅ Conversion History
if "history" not in st.session_state:
    st.session_state.history = []

# ✅ *Google Text-to-Speech Function*
def speak(text):
    tts = gTTS(text=text, lang='en')

    # ✅ Temporary file create kar ke voice save karein
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_path = temp_audio.name
        tts.save(temp_path)
    
    # ✅ MP3 file ko base64 mein encode karein
    with open(temp_path, "rb") as audio_file:
        audio_base64 = base64.b64encode(audio_file.read()).decode()

    # ✅ Audio player show karein (Manual Play)
    audio_html = f"""
        <audio controls>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# ✅ *Streamlit Page Configuration*
st.set_page_config(page_title="Smart Unit Converter", layout="wide")

# ✅ *Fixed Sidebar Color & Animated UI*
st.markdown("""
    <style>
        body { background: linear-gradient(to right, #a1c4fd, #c2e9fb); color: black; }
        .main-title { font-size: 42px; font-weight: bold; color: #FF5733; text-align: center; text-shadow: 2px 2px 5px rgba(0,0,0,0.3); }
        .stButton>button { background: linear-gradient(to right, #ff5733, #ff8d33); color: white; font-size: 18px; padding: 10px; border-radius: 10px; transition: 0.3s; }
        .stButton>button:hover { background: linear-gradient(to right, #ffbd33, #ffdb4d); transform: scale(1.05); }
        .stSidebar { background: linear-gradient(to bottom, #f5f5f5, #e0e0e0); padding: 20px; border-radius: 10px; box-shadow: 3px 3px 10px rgba(0,0,0,0.2); }
        .history-box { background: rgba(255, 255, 255, 0.8); padding: 10px; border-radius: 8px; color: black; }
    </style>
    """, unsafe_allow_html=True)

# ✅ *Title*
st.markdown('<h1 class="main-title">🌟 Smart Unit Converter</h1>', unsafe_allow_html=True)

# ✅ *Conversion Functions*

# Length Conversion Function
def convert_length(value, from_unit, to_unit):
    factors = {"Meters": 1, "Kilometers": 0.001, "Miles": 0.000621371, "Feet": 3.28084}
    return value * factors[to_unit] / factors[from_unit]

# Weight Conversion Function
def convert_weight(value, from_unit, to_unit):
    factors = {"Kilograms": 1, "Grams": 1000, "Pounds": 2.20462, "Ounces": 35.274}
    return value * factors[to_unit] / factors[from_unit]

# Temperature Conversion Function
def convert_temperature(value, from_unit, to_unit):
    if from_unit == "Celsius" and to_unit == "Fahrenheit":
        return (value * 9/5) + 32
    elif from_unit == "Fahrenheit" and to_unit == "Celsius":
        return (value - 32) * 5/9
    return value  

# ✅ *Sidebar Menu*
unit_type = st.sidebar.radio("Choose Conversion Type", ["Length", "Weight", "Temperature"])
st.sidebar.markdown("---")

# ✅ *Length Conversion*
if unit_type == "Length":
    st.subheader("📏 Length Converter")
    from_unit = st.selectbox("From", ["Meters", "Kilometers", "Miles", "Feet"])
    to_unit = st.selectbox("To", ["Meters", "Kilometers", "Miles", "Feet"])
    value = st.number_input("Enter value", min_value=0.0, format="%.2f")

    if st.button("Convert"):
        result = convert_length(value, from_unit, to_unit)
        st.session_state.history.append(f"{value} {from_unit} = {result:.2f} {to_unit}")
        st.success(f"{value} {from_unit} is equal to {result:.2f} {to_unit}")
        speak(f"{value} {from_unit} is equal to {result:.2f} {to_unit}")

# ✅ *Weight Conversion*
elif unit_type == "Weight":
    st.subheader("⚖️ Weight Converter")
    from_unit = st.selectbox("From", ["Kilograms", "Grams", "Pounds", "Ounces"])
    to_unit = st.selectbox("To", ["Kilograms", "Grams", "Pounds", "Ounces"])
    value = st.number_input("Enter value", min_value=0.0, format="%.2f")

    if st.button("Convert"):
        result = convert_weight(value, from_unit, to_unit)
        st.session_state.history.append(f"{value} {from_unit} = {result:.2f} {to_unit}")
        st.success(f"{value} {from_unit} is equal to {result:.2f} {to_unit}")
        speak(f"{value} {from_unit} is equal to {result:.2f} {to_unit}")

# ✅ *Temperature Conversion*
elif unit_type == "Temperature":
    st.subheader("🌡️ Temperature Converter")
    from_unit = st.selectbox("From", ["Celsius", "Fahrenheit"])
    to_unit = st.selectbox("To", ["Celsius", "Fahrenheit"])
    value = st.number_input("Enter value", min_value=-273.15, format="%.2f")  # Below absolute zero not allowed

    if st.button("Convert"):
        result = convert_temperature(value, from_unit, to_unit)
        st.session_state.history.append(f"{value} {from_unit} = {result:.2f} {to_unit}")
        st.success(f"{value} {from_unit} is equal to {result:.2f} {to_unit}")
        speak(f"{value} {from_unit} is equal to {result:.2f} {to_unit}")

# ✅ *Sidebar Pe History Show Karein*
st.sidebar.subheader("📜 Conversion History")

# ✅ Last 5 Entries Dikhao (Agar History Empty Nahi Hai)
if st.session_state.history:
    for entry in st.session_state.history[-5:]:  # ✅ Last 5 conversions dikhao
        st.sidebar.markdown(f"<div class='history-box'>{entry}</div>", unsafe_allow_html=True)
else:
    st.sidebar.write("No history available.")