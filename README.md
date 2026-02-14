# Key and Tonality Analysis

**Interactive dashboard analyzing 1M+ Spotify tracks** using Python, Pandas, Plotly and Streamlit for Data Science practice.

---

## Explore the Data
**Explore the data in your way!** Filter by year, genre and discover insights from Spotify tracks.

**[Try the Live App](https://keys-analysis-spotify.streamlit.app/)**

---

## Data
**Base Dataset:** [Spotify 1M Tracks (Kaggle)](https://www.kaggle.com/datasets/amitanshjoshi/spotify-1million-tracks)  
**License:** [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/)

This project uses a **modified derivative** of the original dataset. Download it directly from [data](data/).

**Note:** There are four different dataset sizes in [data](data/): 100% (Full Dataset), 75%, 50% and 25% (Default).

---

## Tech Stack
```
- Python 3.14+
- Streamlit 1.54.0
- Plotly 6.5.2
- Pandas 2.3.3
```

---

## Quick Start

1. With Docker
```bash
# Clone the repo
git clone https://github.com/caiodotmm/keys-analysis-spotify.git
cd keys-analysis-spotify

# Build the image
docker build -f app.Dockerfile -t keys-analysis-spotify .
# Run the container
docker run -p 8501:8501 keys-analysis-spotify
```
- If you want the high dataset availability version
```bash
# Build the image
docker build -f app_dataset_selection.Dockerfile -t keys-analysis-spotify-dataset-selection .
# Run the container
docker run -p 8502:8502 keys-analysis-spotify
```

2. With Python venv
```bash
# Clone the repo
git clone https://github.com/caiodotmm/keys-analysis-spotify.git
cd keys-analysis-spotify

# Create the virtual enviroment and activate it
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

- If you want the high dataset availability version
```bash
streamlit run app_dataset_selection.py
```
---

## Licensing

[BSD-3-Clause](https://opensource.org/license/bsd-3-clause) [LICENSE](LICENSE)
[ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/)  [DATABASE-LICENSE](DATABASE-LICENSE)

**Note:** This is a Derivative Database. See [DATABASE-LICENSE](DATABASE-LICENSE) for Share-Alike requirements.

---

<div align="center">
  
© 2026 [caiodotmm](https://github.com/caiodotmm)

</div>

---
