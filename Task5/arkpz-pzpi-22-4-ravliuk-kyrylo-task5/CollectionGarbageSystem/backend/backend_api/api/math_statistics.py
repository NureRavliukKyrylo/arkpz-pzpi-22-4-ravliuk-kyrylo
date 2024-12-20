from statistics import mode
from collections import defaultdict
from datetime import timedelta
import numpy as np

# Function to perform polynomial regression and predict future waste data trends
def polynomial_regression_forecast(dates, amounts, future_days, degree=2):
    
    # Calculate the number of days since the first date for each data point
    days = [(date - dates[0]).days for date in dates]

     # Fit polynomial regression to the data
    coefficients = np.polyfit(days, amounts, degree)
    poly = np.poly1d(coefficients)

    # Predict future waste amounts for the next 'future_days' days
    future_predictions = []
    for i in range(1, future_days + 1):
        future_day = days[-1] + i
        predicted_amount = poly(future_day)
        future_predictions.append((dates[-1] + timedelta(days=i), predicted_amount))

    return future_predictions

# Function to calculate statistics for containers based on waste history data
def calculate_statistics_for_containers(waste_histories):
    material_stats = defaultdict(list)

    for history in waste_histories:
        material = history.container_id_filling.type_of_container_id.type_name_container
        volume = (history.sensor_value / 100) * history.container_id_filling.type_of_container_id.volume_container
        material_stats[material].append(volume)

    report_data = {}

    # Calculate statistics (average, mode, min, and max) for each material
    for material, volumes in material_stats.items():
        avg = round(sum(volumes) / len(volumes), 2)
        try:
            mode_val = round(mode(volumes), 2)
        except:
            mode_val = "No mode"

        min_val = round(min(volumes), 2)
        max_val = round(max(volumes), 2)

        report_data[material] = {
            "average": avg,
            "mode": mode_val,
            "min": min_val,
            "max": max_val
        }

    return report_data