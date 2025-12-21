# test_pdf.py
from pdf_generator import generate_pdf

dummy_schedule = [
    {
        "stop_name": "Delhi",
        "arrival_time": 0.0,
        "departure_time": 0.0,
        "deadline_missed_hours": 0
    },
    {
        "stop_name": "Haldwani",
        "arrival_time": 4.2,
        "departure_time": 4.7,
        "deadline_missed_hours": 0
    },
    {
        "stop_name": "Jaipur",
        "arrival_time": 15.3,
        "departure_time": 15.8,
        "deadline_missed_hours": 2.3
    }
]

generate_pdf(
    summary_text="AI optimized the route prioritizing urgent deliveries.",
    schedule=dummy_schedule,
    map_image_path=None,   # abhi map skip
    output_path="test_report.pdf"
)

print("PDF Generated")
