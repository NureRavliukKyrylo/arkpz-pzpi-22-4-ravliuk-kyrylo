import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tempfile

def create_waste_trend_plot(dates, amounts):
    plt.figure(figsize=(6, 4))
    plt.plot(dates, amounts, marker='o', color='b', linestyle='-', label='Waste Amount')
    plt.xlabel('Date')
    plt.ylabel('Amount of Waste')
    plt.title('Waste Trends Over Time')
    plt.legend(loc="upper left")
    plt.grid(visible=True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        img_path = temp_file.name
        plt.savefig(img_path)
        plt.close()
    return img_path
