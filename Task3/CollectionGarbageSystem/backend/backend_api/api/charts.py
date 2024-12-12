import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tempfile
from statistics import median, mode
from collections import defaultdict

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

def calculate_statistics_for_containers(waste_histories):
    material_stats = defaultdict(list)

    for history in waste_histories:
        material = history.container_id_filling.type_of_container_id.type_name_container
        volume = (history.sensor_value / 100) * history.container_id_filling.type_of_container_id.volume_container
        material_stats[material].append(volume)

    report_data = {}
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