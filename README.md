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
├── .gitignore
├── app.py
├── requirements.txt
├── README.md
└── data/
    ├── alaloosi/
    │   ├── 1.json
    │   ├── 1.csv
    │   ├── 100.json
    │   ├── 100.csv
    │   └── ... (more JSON/CSV files per surah/ayah)
    ├── alrazi/
    ├── ibn-aashoor/
    ├── ibn-katheer/
    ├── iraab-daas/
    ├── qurtubi/
    └── tabari/
```

- **app.py**: Main Streamlit application.
- **data/**: Folder containing tafsir data, organized by author subfolders. Each subfolder contains JSON and/or CSV files per surah or ayah.
- **.gitignore**: Git ignore rules.
- **requirements.txt**: Python dependencies.
- **README.md**: Project documentation.

## Getting Started

1. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

2. **Place your tafsir JSON/CSV files** in the appropriate subfolders under `data/` (e.g., `data/alaloosi/1.json`).

3. **Run the app:**

    ```sh
    streamlit run app.py
    ```

4. **Open the app** in your browser at [http://localhost:8501](http://localhost:8501).

## Data Format

Each JSON file in `data/<author>/` should be a list of entries, where each entry contains at least:

- `surah_number`
- `surah_name_arabic`
- `surah_name_english`
- `ayah_number`
- `text`
- (optionally) `language`, `translation`, etc.

CSV files should have equivalent columns.

## Dependencies

See [requirements.txt](requirements.txt) for the full list. Key packages:

- `streamlit`

## License

This project is licensed under the GNU General Public License (GPL).