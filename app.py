import json
import re
import os
import streamlit as st
from translate import TafsirTranslator

base_folder = "data"
cache_folder = "cache"

# --- App Configuration ---
st.set_page_config(
    page_title="Tafsir Viewer", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📖"
)

# --- Custom CSS Styling ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Remove extra space above title */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
        min-height: 100vh;
    }
    
    /* Main Container */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Header Styling */
    .main-header {
        text-align: center;
        margin-bottom: 1rem;
        padding: 0.8rem;
        background: linear-gradient(135deg, #3a6073 0%, #16222a 100%);
        border-radius: 10px;
        color: white;
        box-shadow: 0 5px 15px rgba(79, 172, 254, 0.3);
    }
    
    .main-header h1 {
        font-family: 'Amiri', serif;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
        color: white;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.25);
    }
    
    /* Sidebar Styling */
    .stSidebar {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .stSidebar .stSelectbox label {
        color: white !important;
        font-weight: 500;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }
    
    .stSidebar .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        border: none;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 0.8rem;
    }
    
    .sidebar-header {
        color: white;
        text-align: center;
        padding: 0.8rem;
        margin-bottom: 0.8rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        backdrop-filter: blur(10px);
    }
    
    .sidebar-header h2 {
        font-size: 1.3rem;
        margin: 0;
    }
    
    /* Author Header */
    .author-heading {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        background: #f0f4ff;
        padding: 0.6rem 1rem;
        border-left: 4px solid #4facfe;
        border-radius: 6px;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);    
    }
  
    /* Surah and Ayah Info */
    .surah-ayah-info {
        font-family: 'Amiri', serif;
        font-size: 1.1rem;
        color: #fff;
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        padding: 0.6rem 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        text-align: center;
    }

    .scrollable-text {
        max-height: 60vh;
        overflow-y: auto;
        padding-right: 10px;
        direction: ltr;
    }
    
    /* Arabic Text Styling */
    .arabic-text {
        direction: rtl;
        font-family: 'Amiri', serif;
        font-size: 1.2rem;
        line-height: 1.8;
        text-align: justify;
        white-space: pre-line;
        padding: 1rem;
        background: linear-gradient(135deg, #f3eac2 0%, #e0c3fc 100%);
        border-radius: 8px;
        border-right: 4px solid #ff6b6b;
        box-shadow: 0 3px 10px rgba(255, 107, 107, 0.1);
        margin-bottom: 0.5rem;
    }
    
    /* Translated Text Styling */
    .translated-text {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        line-height: 1.6;
        text-align: justify;
        white-space: pre-line;
        padding: 1rem;
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        border-radius: 8px;
        border-left: 4px solid #4facfe;
        box-shadow: 0 3px 10px rgba(79, 172, 254, 0.1);
        margin-bottom: 0.5rem;
    }
    
    /* Info and Warning Messages */
    .stInfo {
        background: linear-gradient(135deg, #dbe6f6 0%, #c5796d 100%);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        border: none;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: #333;
        border-radius: 10px;
        padding: 1rem;
        border: none;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.5rem;
        }
        
        .arabic-text {
            font-size: 1.1rem;
            padding: 0.8rem;
            line-height: 1.7;
        }
        
        .translated-text {
            font-size: 0.95rem;
            padding: 0.8rem;
            line-height: 1.5;
        }
        
        .tafsir-header {
            font-size: 1.2rem;
        }
        
        .surah-ayah-info {
            font-size: 1.1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- App Title ---
st.markdown('<div class="main-header"><h1>📖 Quran Tafsir Viewer</h1></div>', unsafe_allow_html=True)

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
st.sidebar.markdown('<div class="sidebar-header"><h2>🔍 Filter Options</h2></div>', unsafe_allow_html=True)

authors = sorted(set(entry["author"] for entry in data))
author = st.sidebar.selectbox("📚 Select Author", authors)

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

surah_display = st.sidebar.selectbox("📖 Select Surah", ["-- Select Surah --"] + list(surah_dict.keys()))
selected_surah = surah_dict.get(surah_display, None)

ayah_range = []

if selected_surah:
    # Get ayahs for the selected surah
    available_ayahs = sorted([item["ayah_number"] for item in filtered_data if item["surah_number"] == selected_surah])
    selected_ayah = st.sidebar.selectbox("📝 Select Ayah", available_ayahs)
    ayah_range = [selected_ayah]

selected_lang = st.sidebar.selectbox("🌐 Translate Tafsir To", ["None"] + list(language_codes.keys()))

# --- Display Tafsir ---
if selected_surah and ayah_range:
    matching_tafsirs = [entry for entry in filtered_data if entry["surah_number"] == selected_surah and entry["ayah_number"] in ayah_range]

    if matching_tafsirs:
        
        for tafsir in matching_tafsirs:
            # Header with Surah and Ayah info
            st.markdown(f'''
            <div>
                <div class="author-heading">Tafsir by {tafsir['tafsir_author']}</div>
                <div class="surah-ayah-info">Surah {tafsir['surah_name_arabic']} ({tafsir['surah_name_english']}) - Ayah {tafsir['ayah_number']}</div>
            </div>
            ''', unsafe_allow_html=True)
        
            file_path = os.path.join(base_folder, author, f"{selected_surah}_{selected_ayah}.txt")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    tafsir_text = f.read()
                
                # data cleaning
                tafsir_text = tafsir_text.replace('الباحث القرآني', '')
                
                if selected_lang != "None":
                    cache_file_path = os.path.join(cache_folder, language_codes[selected_lang], author, f"{selected_surah}_{selected_ayah}.txt")
                    
                    if os.path.exists(cache_file_path):
                        with open(cache_file_path, 'r', encoding='utf-8') as f:
                            tafsir_text = f.read()
                    else:
                        # Show loading spinner
                        with st.spinner("Translating ayah... Please wait."):
                            translator = TafsirTranslator()
                            result = translator.translate_tafsir(tafsir_text, "ar", language_codes[selected_lang])
                            tafsir_text = result["translated_text"]

                            # Create directories and save translation
                            lang_dir = os.path.join(cache_folder, language_codes[selected_lang])
                            os.makedirs(lang_dir, exist_ok=True)
                            auth_dir = os.path.join(lang_dir, author)
                            os.makedirs(auth_dir, exist_ok=True)

                            with open(cache_file_path, 'w', encoding='utf-8') as f:
                                f.write(tafsir_text)

                # Display the tafsir text with appropriate styling
                if selected_lang != "None":
                    st.markdown(f'<div class="translated-text scrollable-text">{tafsir_text}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="arabic-text scrollable-text">{tafsir_text}</div>', unsafe_allow_html=True)

            except FileNotFoundError:
                st.error(f"Tafsir file not found: {file_path}")
            except Exception as e:
                st.error(f"Error reading tafsir: {str(e)}")
    else:
        st.warning("No tafsir entries found for the selected criteria.")

else:
    st.markdown('''
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white; margin: 1rem 0;">
        <h3 style="margin: 0 0 0.5rem 0;">Welcome to Quran Tafsir Viewer</h3>
        <p style="font-size: 1rem; opacity: 0.9; margin: 0;">Please select a Surah and Ayah from the sidebar to view tafsir.</p>
    </div>
    ''', unsafe_allow_html=True)