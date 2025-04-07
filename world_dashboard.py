import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Maailman maat - Dashboard", layout="wide")
st.title("🌍 Maailman maat - väestö ja tilastot")

df = pd.read_csv("world_population.csv")


with st.expander("Näytä raakadata"):
    st.dataframe(df)

required_columns = ['Continent', 'Country/Territory', 'Density (per km²)', 'Area (km²)']
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"Puuttuvat sarakkeet: {', '.join(missing_columns)}")
else:
 
    regions = st.multiselect("Valitse maanosat", df['Continent'].unique(), default=df['Continent'].unique())
    filtered = df[df['Continent'].isin(regions)]

    col1, col2, col3 = st.columns(3)
    col1.metric("🌐 Maat", len(df))
    col2.metric("📏 Keskimääräinen tiheys", round(df['Density (per km²)'].mean(), 2))


    st.subheader("🔝 Top 10 maat pinta-alan mukaan")
    top_area = filtered.sort_values(by="Area (km²)", ascending=False).head(10)
    fig1, ax1 = plt.subplots()
    ax1.barh(top_area['Country/Territory'], top_area['Area (km²)'], color='blue')
    ax1.invert_yaxis()
    st.pyplot(fig1)

    st.subheader("📊 Pinta-ala vs Tiheys")
    fig2, ax2 = plt.subplots()
    ax2.scatter(filtered['Area (km²)'], filtered['Density (per km²)'], alpha=0.6)
    ax2.set_xlabel("Pinta-ala (km²)")
    ax2.set_ylabel("Tiheys (as/km²)")
    st.pyplot(fig2)

    st.subheader("🔎 Etsi maa")
    search = st.text_input("Kirjoita maan nimi").capitalize()
    if search:
        result = df[df['Country/Territory'].str.contains(search, case=False)]
        if not result.empty:
            st.dataframe(result)
        else:
            st.warning("Maata ei löytynyt.")
