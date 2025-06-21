import json
import re
import os
import streamlit as st
from openai import OpenAI
import time

# --- App Title ---
st.set_page_config(page_title="Tafsir Viewer", layout="wide")
st.title("📖 Qur'anic Tafsir Viewer")

# --- Load JSON from files in 'data' folder ---
@st.cache_data
def load_all_tafsir_data():
    all_data = []
    data_folder = "data"
    file_list = [f for f in os.listdir(data_folder) if f.endswith(".json")]
    for file in file_list:
        file_path = os.path.join(data_folder, file)
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                content = json.load(f)
                for entry in content:
                    entry["source_file"] = file  # track origin
                    all_data.append(entry)
            except Exception as e:
                st.warning(f"Error reading {file}: {e}")
    return all_data

data = load_all_tafsir_data()

# --- Sidebar Filters ---
st.sidebar.title("🔍 Filter Options")

# Extract authors from file names in 'data' folder
@st.cache_data
def extract_authors_from_files():
    data_folder = "data"
    return sorted({os.path.splitext(f)[0] for f in os.listdir(data_folder) if f.endswith(".json")})

authors = extract_authors_from_files()
author = st.sidebar.selectbox("Select Author", authors)

# Select translation language
language_codes = {
    "English": "en",
    "Urdu": "ur",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Indonesian": "id",
    "Bengali": "bn",
    "Turkish": "tr",
    "Malay": "ms",
    "Swahili": "sw",
}

# Filter data by selected author (filename prefix)
filtered_data = [entry for entry in data if entry.get("source_file", "").startswith(author)]

# Extract surah info
surahs = sorted(set((item["surah_number"], item["surah_name_arabic"], item["surah_name_english"]) for item in filtered_data))
surah_dict = {f"{num} - {name_ar} ({name_en})": num for num, name_ar, name_en in surahs}

surah_display = st.sidebar.selectbox("Select Surah", ["-- Select Surah --"] + list(surah_dict.keys()))
selected_surah = surah_dict.get(surah_display, None)

ayah_range = []

if selected_surah:
    # Get ayahs for the selected surah
    available_ayahs = sorted([item["ayah_number"] for item in filtered_data if item["surah_number"] == selected_surah])

    # Select ayah(s)
    ayah_mode = st.sidebar.radio("Ayah Selection", ["Single Ayah", "Range"], index=0)
    if ayah_mode == "Single Ayah":
        selected_ayah = st.sidebar.selectbox("Select Ayah", available_ayahs)
        ayah_range = [selected_ayah]
    elif ayah_mode == "Range":
        start, end = st.sidebar.slider("Select Ayah Range", min_value=min(available_ayahs), max_value=max(available_ayahs), value=(min(available_ayahs), max(available_ayahs)))
        ayah_range = list(range(start, end + 1))

selected_lang = st.sidebar.selectbox("Translate Tafsir To", ["None"] + list(language_codes.keys()))

# --- GPT-4o Translation using OpenAI ---
def translate_with_gpt4o(text, target_lang):
    prompt = (
        f"Translate the following Arabic tafsir text into {target_lang}. "
        f"Maintain religious tone, clarity, and formatting.\n\n{text}"
    )
    try:
        #api_key = os.getenv("OPENAI_API_KEY")
        api_key = st.secrets["OPENAI_API_KEY"]
        client = OpenAI(api_key=api_key)
        if not api_key:
            return "[Error: OpenAI API key not set in environment variables.]"
        
        response = client.responses.create(
            model="gpt-4o-mini",
            instructions="You are a translator and Islamic scholar. Translate the text while preserving its religious significance.",
            input=prompt,
            temperature=0.5
        )
        return response.output_text.strip()
    except Exception as e:
        return f"[Translation Error: {type(e).__name__}] {e}"

# --- Display Tafsir ---
st.markdown("---")
st.subheader(f"Tafsir by {author}")

if selected_surah and ayah_range:
    matching_tafsirs = [entry for entry in filtered_data if entry["surah_number"] == selected_surah and entry["ayah_number"] in ayah_range]

    if not matching_tafsirs:
        st.warning("No tafsir entries found for the selected criteria.")

    for tafsir in matching_tafsirs:
        st.markdown(f"### Surah {tafsir['surah_name_arabic']} ({tafsir['surah_name_english']}) - Ayah {tafsir['ayah_number']}")
        tafsir_text = tafsir['tafsir_text']
        if selected_lang != "None":
            translated_text = translate_with_gpt4o(tafsir_text, selected_lang)
            st.markdown(f"<div style='text-align: justify; line-height: 2;'>{translated_text}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: justify; line-height: 2;'>{tafsir_text}</div>", unsafe_allow_html=True)
        st.markdown("---")
else:
    st.info("Please select a Surah and Ayah(s) to view tafsir.")
