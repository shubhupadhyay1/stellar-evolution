import streamlit as st


def plot_hr_diagram(data):
    fig = px.scatter(data, x='Temperature', y='Luminosity', color='Stage',
                     hover_data=['Mass', 'Age'], log_y=True,
                     title="Hertzsprung-Russell Diagram",
                     labels={'Temperature': 'Temperature (K)', 'Luminosity': 'Luminosity (relative to Sun)'})
    fig.update_traces(marker=dict(size=10))
    return fig

def plot_mass_luminosity_relation(data):
    fig = px.scatter(data, x='Mass', y='Luminosity', color='Stage',
                     title="Mass-Luminosity Relation",
                     labels={'Mass': 'Mass (in solar masses)', 'Luminosity': 'Luminosity (relative to Sun)'})
    fig.update_traces(marker=dict(size=8))
    return fig

def plot_metallicity_age_relation(data):
    fig = px.scatter(data, x='Age', y='Metallicity', color='Stage',
                     title="Metallicity vs. Age",
                     labels={'Age': 'Age (billion years)', 'Metallicity': 'Metallicity [Fe/H]'},
                     hover_data=['Mass', 'Temperature'])
    return fig

def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    b64 = base64.b64encode(object_to_download.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

st.set_page_config(page_title="Advanced Stellar Evolution Predictor", layout="wide")

# Sidebar configuration
st.sidebar.header('User Input Parameters')
mass = st.sidebar.slider("Mass (in solar masses)", 0.1, 50.0, 1.0)
temperature = st.sidebar.slider("Temperature (K)", 3000, 30000, 6000)
luminosity = st.sidebar.slider("Luminosity (relative to Sun)", 0.1, 10000.0, 1.0)
age = st.sidebar.slider("Age (in billion years)", 0.01, 10.0, 1.0)
metallicity = st.sidebar.slider("Metallicity [Fe/H]", -1.0, 1.0, 0.0)
rotation_rate = st.sidebar.slider("Rotation Rate (relative to solar)", 0.1, 10.0, 1.0)

# Main panel
st.title("Advanced Stellar Evolution Predictor")
st.write("Predict the evolutionary stage of a star based on astrophysical parameters.")

# Prediction logic
input_data = np.array([[mass, temperature, luminosity, age, metallicity, rotation_rate]])
scaled_input = scaler.transform(input_data)
scaled_input = scaled_input.reshape((scaled_input.shape[0], scaled_input.shape[1], 1))
prediction = model.predict(scaled_input)
predicted_stage = np.argmax(prediction)

st.subheader("Predicted Evolutionary Stage")
stage_dict = {0: 'Protostar', 1: 'Main Sequence', 2: 'Red Giant', 3: 'White Dwarf'}
st.write(f"The predicted evolutionary stage is: **{stage_dict[predicted_stage]}**")

# Hertzsprung-Russell Diagram
st.subheader("Hertzsprung-Russell Diagram")
hr_fig = plot_hr_diagram(stellar_data)
st.plotly_chart(hr_fig)

# Mass-Luminosity Relation
st.subheader("Mass-Luminosity Relation")
mass_luminosity_fig = plot_mass_luminosity_relation(stellar_data)
st.plotly_chart(mass_luminosity_fig)

# Metallicity vs. Age
st.subheader("Metallicity vs. Age")
metallicity_age_fig = plot_metallicity_age_relation(stellar_data)
st.plotly_chart(metallicity_age_fig)

# Notes
st.markdown("""
### Learn More About Stellar Evolution
- **Protostar**: The earliest stage of a star's life.
- **Main Sequence**: Stars spend most of their lives in this stable phase.
- **Red Giant**: A late phase where stars expand and cool.
- **White Dwarf**: The final stage for low to medium mass stars.

Explore the diagrams and relations to understand how different factors like mass, temperature, and age influence stellar evolution.
""")
