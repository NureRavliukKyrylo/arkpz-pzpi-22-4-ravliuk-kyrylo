from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from collections import defaultdict
from django.http import HttpResponse
import os
from .charts import create_waste_trend_plot,create_statistics_chart_for_containers
from .math_statistics import calculate_statistics_for_containers, polynomial_regression_forecast

# This function generates PDF reports for waste history, including trends and statistics.
def generate_waste_report_pdf(waste_histories, start_date, end_date, future_days=7):
    if not waste_histories:
        return HttpResponse("No waste history data provided.", content_type="text/plain")

    station_data = defaultdict(float)
    waste_by_date = defaultdict(float)

    for history in waste_histories:
        station_name = history.station_id.station_of_containers_name if history.station_id else "N/A"
        station_data[station_name] += history.amount
        recycling_date = history.recycling_date.date()
        waste_by_date[recycling_date] += history.amount

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="waste_history_report.pdf"'

    pdf_canvas = canvas.Canvas(response, pagesize=letter)

    pdf_canvas.setFont("Times-Bold", 25)

    pdf_canvas.drawString(200, 750, "Waste History Report")
    pdf_canvas.setFont("Times-Bold", 18)
    pdf_canvas.drawString(50, 700, f"Period: {start_date} to {end_date}")

    y = 660
    pdf_canvas.drawString(50, y, "Station Name")
    pdf_canvas.drawString(200, y, "Total Amount")
    y -= 20

    for station_name, total_amount in sorted(station_data.items(), key=lambda x: -x[1]):
        pdf_canvas.drawString(50, y, str(station_name))
        pdf_canvas.drawString(200, y, f"{total_amount:.2f}")
        y -= 20
        if y < 50:
            pdf_canvas.showPage()
            pdf_canvas.setFont("Times-Bold", 12)
            y = 750  

    if y < 70:
        pdf_canvas.showPage()
        pdf_canvas.setFont("Times-Bold", 12)
        y = 750  

    pdf_canvas.drawString(50, y - 30, f"Total Stations: {len(station_data)}")
    pdf_canvas.drawString(50, y - 50, f"Total Waste Amount: {sum(station_data.values()):.2f}")
    y -= 40

    dates = sorted(waste_by_date.keys())
    amounts = [waste_by_date[date] for date in dates]
    predictions = polynomial_regression_forecast(dates, amounts, future_days)

    img_path = create_waste_trend_plot(dates, amounts, predictions)

    if y < 350:
        pdf_canvas.showPage()
        pdf_canvas.setFont("Times-Bold", 12)
        y = 750  

    pdf_canvas.drawImage(img_path, 50, y - 350, width=450, height=300)
    os.remove(img_path)

    pdf_canvas.save()
    return response

# Function to generate PDF report for container-specific waste statistics
def generate_waste_report_for_containers_pdf(waste_histories, start_date, end_date):
    if not waste_histories:
        return HttpResponse("No waste history data provided.", content_type="text/plain")

    report_data = calculate_statistics_for_containers(waste_histories)

    chart_img_path = create_statistics_chart_for_containers(report_data)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="waste_history_report.pdf"'

    pdf_canvas = canvas.Canvas(response, pagesize=letter)
    pdf_canvas.setFont("Times-Bold", 25)
    pdf_canvas.drawString(180, 750, "Statistics Type Containers")
    pdf_canvas.setFont("Times-Bold", 14)
    pdf_canvas.drawString(50, 700, f"Period: {start_date} to {end_date}")

    y = 660
    pdf_canvas.drawString(50, y, "Material Type")
    pdf_canvas.drawString(150, y, "Average Volume (liters)")
    pdf_canvas.drawString(310, y, "Mode Volume (liters)")
    pdf_canvas.drawString(455, y, "Min")
    pdf_canvas.drawString(530, y, "Max")
    y -= 20

    for material, stats in sorted(report_data.items(), key=lambda x: -x[1]['average']):
        pdf_canvas.drawString(50, y, str(material))
        pdf_canvas.drawString(150, y, f"{stats['average']} liters")
        pdf_canvas.drawString(310, y, f"{stats['mode']} liters")
        pdf_canvas.drawString(455, y, f"{stats['min']} liters")
        pdf_canvas.drawString(530, y, f"{stats['max']} liters")
        y -= 20
        if y < 50:
            pdf_canvas.showPage()
            pdf_canvas.setFont("Times-Bold", 12)
            y = 750  

    if y < 70:
        pdf_canvas.showPage()
        pdf_canvas.setFont("Times-Bold", 12)
        y = 750  

    pdf_canvas.drawString(50, y - 30, f"Total Materials: {len(report_data)}")
    y -= 40

    pdf_canvas.drawImage(chart_img_path, 50, y - 350, width=500, height=300)
    os.remove(chart_img_path)

    pdf_canvas.save()
    return response

