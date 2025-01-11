import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import argparse

# Load the model and scaler
def load_model_and_scaler(model_path, scaler_path):
    """
    Load the trained model and the scaler used during training.

    Parameters:
    model_path (str): Path to the trained model file.
    scaler_path (str): Path to the saved scaler.

    Returns:
    tuple: Loaded model and scaler
    """
    model = load_model(model_path)
    scaler = pd.read_pickle(scaler_path)
    return model, scaler

# Predict the evolutionary stage of a star
def predict_star_stage(model, scaler, input_features):
    """
    Predict the evolutionary stage of a star given its features.

    Parameters:
    model (keras.models.Model): Trained LSTM model.
    scaler (sklearn.preprocessing.MinMaxScaler): Scaler used for feature normalization.
    input_features (list): List of input features [Mass, Temperature, Luminosity, Age, Metallicity, RotationRate].

    Returns:
    str: Predicted evolutionary stage.
    """
    # Convert input features to numpy array and reshape for prediction
    input_array = np.array(input_features).reshape(1, -1)

    # Scale the input features
    scaled_input = scaler.transform(input_array)
    scaled_input = scaled_input.reshape((scaled_input.shape[0], scaled_input.shape[1], 1))

    # Make prediction
    prediction = model.predict(scaled_input)
    predicted_stage = np.argmax(prediction)

    # Map numerical stage to descriptive stage
    stage_dict = {0: 'Protostar', 1: 'Main Sequence', 2: 'Red Giant', 3: 'White Dwarf'}
    return stage_dict[predicted_stage]

# Main execution block
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict the evolutionary stage of a star.")
    parser.add_argument('--mass', type=float, required=True, help="Mass of the star in solar masses")
    parser.add_argument('--temperature', type=float, required=True, help="Temperature of the star in Kelvin")
    parser.add_argument('--luminosity', type=float, required=True, help="Luminosity of the star relative to the Sun")
    parser.add_argument('--age', type=float, required=True, help="Age of the star in billion years")
    parser.add_argument('--metallicity', type=float, required=True, help="Metallicity [Fe/H] of the star")
    parser.add_argument('--rotation_rate', type=float, required=True, help="Rotation rate relative to the Sun")

    args = parser.parse_args()

    # Load model and scaler
    model_path = "../models/stellar_evolution_model.h5"
    scaler_path = "../models/scaler.pkl"
    model, scaler = load_model_and_scaler(model_path, scaler_path)

    # Prepare input features
    input_features = [
        args.mass,
        args.temperature,
        args.luminosity,
        args.age,
        args.metallicity,
        args.rotation_rate
    ]

    # Predict stage
    predicted_stage = predict_star_stage(model, scaler, input_features)
    print(f"The predicted evolutionary stage of the star is: {predicted_stage}")