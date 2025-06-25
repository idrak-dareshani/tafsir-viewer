import json
import re
import os
import streamlit as st

# --- App Title ---
st.set_page_config(page_title="Tafsir Viewer", layout="wide")
st.title("📖 Qur'anic Tafsir Viewer")

# --- Load JSON from author/surah-structured folder ---
@st.cache_data
def load_all_tafsir_data():
    all_data = []
    base_folder = "data"
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

    # Select ayah(s)
    ayah_mode = st.sidebar.radio("Ayah Selection", ["Single Ayah", "Range"], index=0)
    if ayah_mode == "Single Ayah":
        selected_ayah = st.sidebar.selectbox("Select Ayah", available_ayahs)
        ayah_range = [selected_ayah]
    elif ayah_mode == "Range":
        start, end = st.sidebar.slider("Select Ayah Range", min_value=min(available_ayahs), max_value=max(available_ayahs), value=(min(available_ayahs), max(available_ayahs)))
        ayah_range = list(range(start, end + 1))

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
        st.markdown(f"### Surah {tafsir['surah_name_arabic']} ({tafsir['surah_name_english']}) - Ayah {tafsir['ayah_number']}")
        tafsir_text = tafsir['tafsir_text']
        if selected_lang != "None":
            st.markdown(f"<div style='text-align: justify; line-height: 2;'>We are working on the translation...</div>", unsafe_allow_html=True)
        elif selected_lang != "None":
            st.warning("Translation not available for this tafsir.")
        else:
            st.markdown(f"<div style='text-align: right; line-height: 2; font-size: 1.5em'>{tafsir_text}</div>", unsafe_allow_html=True)
        st.markdown("---")
else:
    st.info("Please select a Surah and Ayah(s) to view tafsir.")
