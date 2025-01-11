import numpy as np
from keras.models import Model, load_model
from keras.layers import LSTM, Dense, Dropout, Input
from keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import pandas as pd

# Load and preprocess data
def load_and_preprocess_data(file_path):
    """
    Load synthetic stellar data and preprocess it for model training.

    Parameters:
    file_path (str): Path to the CSV file containing stellar data.

    Returns:
    tuple: Scaled training and testing data (X_train, X_test, y_train, y_test)
    """
    # Load data
    data = pd.read_csv(file_path)

    # Features and target
    features = ['Mass', 'Temperature', 'Luminosity', 'Age', 'Metallicity', 'RotationRate']
    target = 'Stage'

    X = data[features].values
    y = data[target].values

    # Scale features
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Reshape data for LSTM input (samples, timesteps, features)
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

    return X_train, X_test, y_train, y_test, scaler

# Build the LSTM model
def build_lstm_model(input_shape):
    """
    Build and compile an LSTM model for stellar evolution prediction.

    Parameters:
    input_shape (tuple): Shape of the input data (timesteps, features).

    Returns:
    keras.models.Model: Compiled LSTM model
    """
    input_layer = Input(shape=input_shape)
    x = LSTM(64, return_sequences=True)(input_layer)
    x = Dropout(0.2)(x)
    x = LSTM(32, return_sequences=False)(x)
    x = Dense(32, activation='relu')(x)
    output_layer = Dense(4, activation='softmax')(x)

    model = Model(inputs=input_layer, outputs=output_layer)
    model.compile(optimizer=Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    return model

# Main execution block
if __name__ == "__main__":
    # Load and preprocess data
    file_path = "../data/synthetic_stellar_data.csv"
    X_train, X_test, y_train, y_test, scaler = load_and_preprocess_data(file_path)

    # Build model
    input_shape = (X_train.shape[1], 1)
    model = build_lstm_model(input_shape)

    # Train model
    print("Training the LSTM model...")
    history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=20, batch_size=32)

    # Save the trained model
    model.save("../models/stellar_evolution_model.h5")
    print("Model training complete. Model saved to ../models/stellar_evolution_model.h5")