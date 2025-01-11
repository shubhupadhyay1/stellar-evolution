import numpy as np
import pandas as pd

# Set a random seed for reproducibility
np.random.seed(42)

# Function to generate synthetic stellar data based on astrophysical principles
def generate_stellar_data(n_samples=5000):
    """
    Generate synthetic stellar data.

    Parameters:
    n_samples (int): Number of synthetic star samples to generate.

    Returns:
    pd.DataFrame: DataFrame containing stellar data with features:
                  Mass, Temperature, Luminosity, Age, Metallicity, Rotation Rate, Stage
    """
    # Generate mass in solar masses (range: 0.1 to 50)
    masses = np.random.uniform(0.1, 50, n_samples)

    # Generate temperature in Kelvin (range: 3000 to 30000)
    temperatures = 7090 / (np.random.uniform(0.1, 2, n_samples) + 0.72)

    # Calculate luminosity using the mass-luminosity relation (L ≈ M^3.5)
    luminosities = masses ** 3.5

    # Generate age in billion years (range: 0.01 to 10)
    ages = np.random.uniform(0.01, 10, n_samples)

    # Generate metallicity [Fe/H] (range: -1 to +1)
    metallicities = np.random.uniform(-1, 1, n_samples)

    # Generate rotation rate relative to the Sun (range: 0.1 to 10)
    rotation_rates = np.random.uniform(0.1, 10, n_samples)

    # Classify stars into evolutionary stages based on age
    stages = np.digitize(ages, bins=[0.1, 2, 5, 9]) - 1
    stages = np.clip(stages, 0, 3)  # Clip stages to ensure they are between 0 and 3

    # Create a DataFrame with the generated data
    data = pd.DataFrame({
        'Mass': masses,
        'Temperature': temperatures,
        'Luminosity': luminosities,
        'Age': ages,
        'Metallicity': metallicities,
        'RotationRate': rotation_rates,
        'Stage': stages
    })

    return data

# Main execution block to generate and save the data
if __name__ == "__main__":
    print("Generating synthetic stellar data...")
    stellar_data = generate_stellar_data()
    print("Data generation complete. Here is a preview:")
    print(stellar_data.head())

    # Save the generated data to a CSV file
    output_path = "data/synthetic_stellar_data.csv"
    stellar_data.to_csv(output_path, index=False)
    print(f"Synthetic stellar data saved to {output_path}")