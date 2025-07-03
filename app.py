import json
import re
import os
import streamlit as st
from translate import TafsirTranslator

base_folder = "data"
cache_folder = "cache"

# --- App Title ---
st.set_page_config(page_title="Tafsir Viewer", layout="wide")
st.title("📖 Quran Tafsir Viewer")

# --- Load JSON from author/surah-structured folder ---
@st.cache_data
def load_all_tafsir_data():
    all_data = []
    for author_folder in os.listdir(base_folder):
        author_path = os.path.join(base_folder, author_folder)
        if os.path.isdir(author_path):
            for filename in os.listdir(author_path):
                if filename.endswith(".json"):
                    file_path = os.path.join(author_path, filename)
                    with open(file_path, "r", encoding="utf-8") as f:
                        try:
                            content = json.load(f)
                            for entry in content:
                                entry["source_file"] = filename
                                entry["author"] = author_folder
                                all_data.append(entry)
                        except Exception as e:
                            st.warning(f"Error reading {file_path}: {e}")
    return all_data

data = load_all_tafsir_data()

# --- Sidebar Filters ---
st.sidebar.title("🔍 Filter Options")

authors = sorted(set(entry["author"] for entry in data))
author = st.sidebar.selectbox("Select Author", authors)

# Select translation language
language_codes = {
    "Bengali": "bn",
    "English": "en",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Indonesian": "id",
    "Malay": "ms",
    "Spanish": "es",
    "Swahili": "sw",
    "Turkish": "tr",
    "Urdu": "ur"
}

# Filter data by selected author
filtered_data = [entry for entry in data if entry.get("author") == author]

# Extract surah info
surahs = sorted(set((item["surah_number"], item["surah_name_arabic"], item["surah_name_english"]) for item in filtered_data))
surah_dict = {f"{num} - {name_ar} ({name_en})": num for num, name_ar, name_en in surahs}

surah_display = st.sidebar.selectbox("Select Surah", ["-- Select Surah --"] + list(surah_dict.keys()))
selected_surah = surah_dict.get(surah_display, None)

ayah_range = []

if selected_surah:
    # Get ayahs for the selected surah
    available_ayahs = sorted([item["ayah_number"] for item in filtered_data if item["surah_number"] == selected_surah])

    selected_ayah = st.sidebar.selectbox("Select Ayah", available_ayahs)
    ayah_range = [selected_ayah]

    # # Select ayah(s)
    # ayah_mode = st.sidebar.radio("Ayah Selection", ["Single Ayah", "Range"], index=0)
    # if ayah_mode == "Single Ayah":
    # elif ayah_mode == "Range":
    #     start, end = st.sidebar.slider("Select Ayah Range", min_value=min(available_ayahs), max_value=max(available_ayahs), value=(min(available_ayahs), max(available_ayahs)))
    #     ayah_range = list(range(start, end + 1))

selected_lang = st.sidebar.selectbox("Translate Tafsir To", ["None"] + list(language_codes.keys()))

# --- Display Tafsir ---
st.markdown("---")
if selected_surah and ayah_range:
    matching_tafsirs = [entry for entry in filtered_data if entry["surah_number"] == selected_surah and entry["ayah_number"] in ayah_range]

    if matching_tafsirs and "tafsir_author" in matching_tafsirs[0]:
        st.subheader(f"Tafsir by {matching_tafsirs[0]['tafsir_author']}")
    else:
        st.subheader(f"Tafsir by {author}")

    if not matching_tafsirs:
        st.warning("No tafsir entries found for the selected criteria.")

    for tafsir in matching_tafsirs:
        # Header with Surah and Ayah info
        
        st.markdown(f"### Surah {tafsir['surah_name_arabic']} ({tafsir['surah_name_english']}) - Ayah {tafsir['ayah_number']}")
    
        file_path = os.path.join(base_folder, author, f"{selected_surah}_{selected_ayah}.txt")
        with open(file_path, 'r', encoding='utf-8') as f:
            tafsir_text = f.read()
        if selected_lang != "None":
            file_path = os.path.join(cache_folder, language_codes[selected_lang], author, f"{selected_surah}_{selected_ayah}.txt")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    tafsir_text = f.read()
            else:
                translator = TafsirTranslator()
                result = translator.translate_tafsir(tafsir_text, "ar", language_codes[selected_lang])
                tafsir_text = result["translated_text"]

                # create language directory (if not exists)
                lang_dir = os.path.join(cache_folder, language_codes[selected_lang])
                os.makedirs(lang_dir, exist_ok=True)

                # create author directory (if not exists)
                auth_dir = os.path.join(lang_dir, author)
                os.makedirs(auth_dir, exist_ok=True)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(tafsir_text)

        if selected_lang != "None":
            st.markdown(f"<div style='text-align: justify; line-height: 2; white-space: pre-line;'>{tafsir_text}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='direction: rtl; font-size: 1.15rem; text-align: justify; line-height: 2; white-space: pre-line;'>{tafsir_text}</div>", unsafe_allow_html=True)

else:
    st.info("Please select a Surah and Ayah(s) to view tafsir.")
