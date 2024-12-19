import matplotlib
# Set matplotlib to use a non-interactive backend (useful for running in server environments)
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tempfile

# Function to create a waste trend plot over time, with optional forecast predictions
def create_waste_trend_plot(dates, amounts, predictions=None):
    plt.figure(figsize=(6, 4))
    plt.plot(dates, amounts, marker='o', color='b', linestyle='-', label='Waste Amount')

    if predictions:
        pred_dates, pred_amounts = zip(*predictions)
        plt.plot(pred_dates, pred_amounts, marker='x', color='r', linestyle='--', label='Forecast')

    plt.xlabel('Date')
    plt.ylabel('Amount of Waste')
    plt.title('Waste Trends Over Time')
    plt.legend(loc="upper right")
    plt.grid(visible=True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        img_path = temp_file.name
        plt.savefig(img_path)
        plt.close()
    return img_path

# Function to create a bar chart for container waste volume statistics (average and mode)
def create_statistics_chart_for_containers(report_data):
    materials = list(report_data.keys())
    averages = [stats["average"] for stats in report_data.values()]
    modes = [
        stats["mode"] if stats["mode"] != "No mode" else 0  
        for stats in report_data.values()
    ]

    plt.figure(figsize=(10, 6))
    x = range(len(materials))
    plt.bar(x, averages, width=0.4, label="Average", align='center', color="skyblue")
    plt.bar([i + 0.4 for i in x], modes, width=0.4, label="Mode", align='center', color="orange")

    plt.xticks([i + 0.2 for i in x], materials, rotation=45, ha="right")
    plt.title("Waste Volume Statistics")
    plt.ylabel("Volume (liters)")
    plt.xlabel("Material Type")
    plt.legend()
    plt.tight_layout()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        plt.savefig(temp_file, format="png")
        temp_file_path = temp_file.name
        plt.close()

    return temp_file_path