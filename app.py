import streamlit as st
import pandas as pd
import plotly.express as px

# Page Setting
# Defining the page title, the icon and the layout
st.set_page_config(
    page_title="Key and Tonality Analysis of Spotify Tracks",
    page_icon="📊",
    layout="wide"
)

if "df" not in st.session_state:
    st.session_state.df = None
if "df_filtered" not in st.session_state:
    st.session_state.df_filtered = pd.DataFrame()

# Loading Data
@st.cache_data
def load_dataset(file_path):
    return pd.read_csv(file_path, compression="gzip", low_memory=False)

st.session_state.df = load_dataset("data/keys_spotify_data-25.csv.gz")

# Side Bar (Filters)
st.sidebar.header("🔍 Filter")

# Year Filter
available_years = sorted(st.session_state.df["year"].unique())
selected_years = st.sidebar.multiselect(
    "Year", available_years, default=available_years
)

# Genre Filter
available_genres = sorted(st.session_state.df["genre"].unique())
selected_genres = st.sidebar.multiselect(
    "Genre", available_genres, default=available_genres
)

# The main dataframe is filtered relative with the selections on the sidebar
st.session_state.df_filtered = st.session_state.df[
    (st.session_state.df["year"].isin(selected_years)) &
    (st.session_state.df["genre"].isin(selected_genres))
]

st.sidebar.markdown("---")
st.sidebar.subheader("🛈 Infos")
st.sidebar.markdown("**Base Dataset:** [Spotify 1M Tracks (Kaggle)](https://www.kaggle.com/datasets/amitanshjoshi/spotify-1million-tracks)")
st.sidebar.markdown("**Data License:** [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/)")
st.sidebar.markdown("**Project License:** [BSD-3-Clause](https://opensource.org/license/bsd-3-clause)")
st.sidebar.markdown("**Project Repository:** [GitHub](https://github.com/caiodotmm/keys-analysis-spotify)")

# Main Content
st.title("🎼 Key and Tonality Dashboard")
st.markdown("Explore the Keys and Tonalities analysis over 280K+ Spotify Tracks Dataset from 2000 to 2023. Use the filter in the left sidebar for sharp analysis!")

# KPIs
st.subheader("General Metrics")

if not st.session_state.df_filtered.empty:
    top_key = st.session_state.df_filtered["short_key_tonality"].value_counts().idxmax()
    tracks_in_top_key = (st.session_state.df_filtered["short_key_tonality"] == top_key).sum()
    top_key_mean_popularity = st.session_state.df_filtered[st.session_state.df_filtered["short_key_tonality"] == top_key]["popularity"].mean()
    top_key_median_popularity = st.session_state.df_filtered[st.session_state.df_filtered["short_key_tonality"] == top_key]["popularity"].median()
    tracks_number = st.session_state.df_filtered.shape[0]
else:
    top_key, tracks_in_top_key, top_key_mean_popularity, tracks_number = "", 0, 0, 0

col1, col2, col3, col4, col5= st.columns(5)

col1.metric("Top Key", top_key)
col2.metric("Tracks in top key", f"{tracks_in_top_key:,.0f}")
col3.metric("Top key mean popularity", f"{top_key_mean_popularity:,.2f}")
col4.metric("Top key median popularity", f"{top_key_median_popularity:,.2f}")
col5.metric("Tracks in Dataset", f"{tracks_number:,.0f}")

st.markdown("---")

# Graphical Analysis with Plotly
st.subheader("Graphs")

# Odered categories for the plotting
ordered_keys = [
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B"
]

ordered_relatives = [
    "C/Am",
    "C#/A#m",
    "D/Bm",
    "D#/Cm",
    "E/C#m",
    "F/Dm",
    "F#/D#m",
    "G/Em",
    "G#/Fm",
    "A/F#m",
    "A#/Gm",
    "B/G#m"
]

categorical_colors = [
    "#00E676",
    "#6495ED",
    "#E68600",
    "#E60300",
    "#7600E6",
    "#E60070",
    "#E600E3",
    "#00E3E6",
    "#FFD000",
    "#002FFF",
    "#AFFF00",
    "#00FFD0"
]

container_graph1 = st.container()

with container_graph1:
    if not st.session_state.df_filtered.empty:
        tracks_per_key = st.session_state.df_filtered.groupby(["key_chord_notation", "tonality"]).size().reset_index(name="tracks")
        tracks_per_key_graph = px.bar(
            tracks_per_key,
            x="key_chord_notation",
            y="tracks",
            color="tonality",
            title="Number of Tracks per Key",
            category_orders={"key_chord_notation": ordered_keys},
            color_discrete_sequence=categorical_colors,
            labels={"key_chord_notation": "Key", "tracks": "Tracks", "tonality": "Tonality"}
        )

        st.plotly_chart(tracks_per_key_graph)
    else:
        st.warning("No data provided.")

col_graph1, col_graph2, col_graph3 = st.columns(3)

with col_graph1:
    if not st.session_state.df_filtered.empty:
        tracks_mean_popularity_per_key = st.session_state.df_filtered.groupby(["key_chord_notation", "tonality"])["popularity"].mean().reset_index()

        tracks_mean_popularity_per_key_graph = px.bar(
            tracks_mean_popularity_per_key,
            x="key_chord_notation",
            y="popularity",
            color="tonality",
            title="Mean Popularity per Key",
            category_orders={"key_chord_notation": ordered_keys},
            color_discrete_sequence=categorical_colors,
            labels={"key_chord_notation": "Key", "popularity": "Popularity", "tonality": "Tonality"}
        )

        st.plotly_chart(tracks_mean_popularity_per_key_graph)
    else:
        st.warning("No data provided.")

with col_graph2:
    if not st.session_state.df_filtered.empty:
        tracks_mean_instrumentalness = st.session_state.df_filtered.groupby(["key_chord_notation", "tonality"])["instrumentalness"].mean().reset_index()

        tracks_mean_instrumentalness_graph = px.bar(
            tracks_mean_instrumentalness,
            x="key_chord_notation",
            y="instrumentalness",
            color="tonality",
            title="Mean Instrumentalness per Key",
            category_orders={"key_chord_notation": ordered_keys},
            color_discrete_sequence=categorical_colors,
            labels={"key_chord_notation": "Key", "instrumentalness": "Instrumentalness", "tonality": "Tonality"}
        )

        st.plotly_chart(tracks_mean_instrumentalness_graph)
    else:
        st.warning("No data provided.")

with col_graph3:
    if not st.session_state.df_filtered.empty:
        tracks_mean_valence = st.session_state.df_filtered.groupby(["key_chord_notation", "tonality"])["valence"].mean().reset_index()

        tracks_mean_valence_graph = px.bar(
            tracks_mean_valence,
            x="key_chord_notation",
            y="valence",
            color="tonality",
            title="Mean Valence per Key",
            category_orders={"key_chord_notation": ordered_keys},
            color_discrete_sequence=categorical_colors,
            labels={"key_chord_notation": "Key", "valence": "Valence", "tonality": "Tonality"}
        )

        st.plotly_chart(tracks_mean_valence_graph)
    else:
        st.warning("No data provided.")

container_graph2 = st.container()

with container_graph2:
    if not st.session_state.df_filtered.empty:
        key_relative_per_year = st.session_state.df_filtered.groupby(["key_relative_notation", "year"]).size().reset_index(name="tracks")

        key_relative_per_year_graph = px.line(
            key_relative_per_year,
            x="year",
            y="tracks",
            color="key_relative_notation",
            markers=True,
            title="Keys evolution over time",
            category_orders={"key_relative_notation": ordered_relatives},
            color_discrete_sequence=categorical_colors,
            labels={"key_relative_notation": "Key with Relative", "tracks": "Tracks", "year": "Year"}
        )

        st.plotly_chart(key_relative_per_year_graph)
    else:
        st.warning("No data provided.")

container_graph3 = st.container()

with container_graph3:
    if not st.session_state.df_filtered.empty:
        tracks_per_genre_and_key = st.session_state.df_filtered.groupby(["genre","key_relative_notation"]).size().reset_index(name="tracks")

        tracks_per_genre_and_key_graph = px.scatter(
            tracks_per_genre_and_key,
            x="genre",
            y="tracks",
            size="tracks",
            color="key_relative_notation",
            title="Tracks per key in each Genre",
            category_orders={"key_relative_notation": ordered_relatives},
            color_discrete_sequence=categorical_colors,
            labels={"key_relative_notation": "Key with Relative", "tracks": "Tracks", "genre": "Genre"}
        )

        st.plotly_chart(tracks_per_genre_and_key_graph)
    else:
        st.warning("No data provided.")

container_graph4 = st.container()

with container_graph4:
    if not st.session_state.df_filtered.empty:
        mean_popularity_per_genre_and_key = st.session_state.df_filtered.groupby(["genre","key_relative_notation"])["popularity"].mean().reset_index()

        mean_popularity_per_genre_and_key_graph = px.scatter(
            mean_popularity_per_genre_and_key,
            x="genre",
            y="popularity",
            size="popularity",
            color="key_relative_notation",
            title="Mean Popularity per key in each Genre",
            category_orders={"key_relative_notation": ordered_relatives},
            color_discrete_sequence=categorical_colors,
            labels={"key_relative_notation": "Key with Relative", "popularity": "Popularity", "genre": "Genre"}
        )

        st.plotly_chart(mean_popularity_per_genre_and_key_graph)
    else:
        st.warning("No data provided.")

st.markdown("---")

# Dataframe
st.subheader("Detailed Data")
st.markdown("Top 10,000 most popular tracks in the filtered dataset.")
st.session_state.df_sorted_popularity = st.session_state.df_filtered.sort_values(by="popularity", ascending=False)
st.dataframe(st.session_state.df_sorted_popularity.head(10000))
