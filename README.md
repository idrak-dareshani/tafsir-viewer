# Qur'anic Tafsir Viewer

A Streamlit web application for browsing and filtering Qur'anic tafsir (exegesis) from multiple authors and languages.

## Features

- Browse tafsir entries from multiple authors.
- Filter by author, surah, ayah, and translation language.
- Loads tafsir data from JSON files in the `data/` directory.
- User-friendly sidebar for filtering options.

## Project Structure

```
.
├── .env
├── app.py
├── requirements.txt
└── data/
    ├── alaloosi.json
    ├── alrazi.json
    └── ibn-katheer.json
```

- **app.py**: Main Streamlit application.
- **data/**: Folder containing tafsir data in JSON format, one file per author.
- **.env**: Environment variables (e.g., API keys).
- **requirements.txt**: Python dependencies.

## Getting Started

1. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

2. **Add your `.env` file** (if needed for API keys).

3. **Place your tafsir JSON files** in the `data/` directory.

4. **Run the app:**

    ```sh
    streamlit run app.py
    ```

5. **Open the app** in your browser at [http://localhost:8501](http://localhost:8501).

## Data Format

Each JSON file in `data/` should be a list of entries, where each entry contains at least:

- `surah_number`
- `surah_name_arabic`
- `surah_name_english`
- `ayah_number`
- `text`
- (optionally) `language`, `translation`, etc.

## Dependencies

See [requirements.txt](requirements.txt) for the full list. Key packages:

- `streamlit`
- `openai`

## License

MIT License (add your license here).
