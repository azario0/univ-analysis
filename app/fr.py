import streamlit as st
import pandas as pd
import altair as alt

# Configuration de la page
st.set_page_config(page_title="Filtre de données universitaires", layout="wide")

# Mise en cache du chargement des données
@st.cache_resource
def load_data():
    return pd.read_csv('topuniversities.csv')

df = load_data()

# Configuration de la barre latérale pour les filtres
st.sidebar.title('Filtres')
filter_by = st.sidebar.selectbox('Filtrer par:', ['Ville', 'Nom de l\'Université'])

# Initialisation de filtered_df
filtered_df = df  # Par défaut, tout le jeu de données

# Appliquer le filtre en fonction du choix de l'utilisateur
if filter_by == 'Ville':
    selected_city = st.sidebar.selectbox('Sélectionnez une ville:', df['City'].unique())
    filtered_df = df[df['City'] == selected_city]
elif filter_by == 'Nom de l\'Université':
    selected_university = st.sidebar.selectbox('Sélectionnez un nom d\'université:', df['University Name'].unique())
    filtered_df = df[df['University Name'] == selected_university]

# Titre principal de la page
st.title('Explorateur de données universitaires')

# Affichage des critères de filtre
st.write(f'Filtré par **{filter_by}**: **{selected_city if filter_by == "Ville" else selected_university}**')

# Vérifier si les données filtrées ne sont pas vides
if not filtered_df.empty:
    # Affichage du DataFrame dans une colonne
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # DataFrame stylé
        styled_df = filtered_df.style.highlight_max(axis=0)
        st.dataframe(styled_df)
    
    with col2:
        # Créer un graphique interactif
        chart_data = filtered_df[['University Name', 'Overall Score', 'Citations per Paper']]
        chart = alt.Chart(chart_data).mark_bar().encode(
            x='University Name',
            y='Overall Score',
            color='Citations per Paper'
        ).interactive()
        st.altair_chart(chart, use_container_width=True)
    
    # Bouton de téléchargement
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Télécharger les données filtrées au format CSV",
        data=csv,
        file_name='donnees_universitaires_filtrées.csv',
        mime='text/csv',
    )
else:
    st.warning('Aucune donnée ne correspond au filtre sélectionné.')