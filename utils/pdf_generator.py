# from reportlab.platypus import (
#     SimpleDocTemplate,
#     Paragraph,
#     Table,
#     TableStyle,
#     Image,
#     Spacer
# )
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib import colors


# def generate_pdf(summary_text, schedule, map_image_path, output_path):
#     doc = SimpleDocTemplate(output_path)
#     styles = getSampleStyleSheet()
#     elements = []

#     # Title
#     elements.append(Paragraph("<b>Logistics Route Optimization Report</b>", styles["Title"]))
#     elements.append(Spacer(1, 12))

#     # Summary
#     elements.append(Paragraph("<b>AI Generated Summary</b>", styles["Heading2"]))
#     elements.append(Paragraph(summary_text, styles["Normal"]))
#     elements.append(Spacer(1, 12))

#     # Table
#     table_data = [["Stop", "Arrival", "Departure", "Deadline Missed (hrs)"]]
#     for s in schedule:
#         table_data.append([
#             s["stop_name"],
#             round(s["arrival_time"], 2),
#             round(s["departure_time"], 2),
#             round(s.get("deadline_missed_hours", 0), 2)
#         ])

#     table = Table(table_data)
#     table.setStyle(TableStyle([
#         ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
#         ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
#         ("ALIGN", (0, 0), (-1, -1), "CENTER"),
#         ("GRID", (0, 0), (-1, -1), 1, colors.black),
#         ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
#     ]))

#     elements.append(table)
#     elements.append(Spacer(1, 12))

#     # Map image
#     if map_image_path:
#         elements.append(Paragraph("<b>Route Map</b>", styles["Heading2"]))
#         elements.append(Image(map_image_path, width=400, height=300))

#     doc.build(elements)
# utils/pdf_generator.py
import io
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generate_pdf_bytes(report: dict) -> bytes:
    """
    report: {
      "title": "string" (optional),
      "summary": "string",
      "schedule": [ {stop_name, arrival_time, departure_time, deadline_missed_hours?, lat?, lon?}, ... ],
      "map_image_bytes": optional bytes (PNG/JPG)
    }
    Returns: PDF bytes
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    title = report.get("title", "Logistics Route Optimization Report")
    elements.append(Paragraph(f"<b>{title}</b>", styles["Title"]))
    elements.append(Spacer(1, 8))

    # Summary
    # elements.append(Paragraph("<b>Executive Summary</b>", styles["Heading2"]))
    elements.append(Paragraph("Executive Summary", styles["Heading2"]))

    # summary_text = report.get("summary", "No summary provided.")
    # elements.append(Paragraph(summary_text, styles["Normal"]))
    summary_text = report.get("summary", "No summary provided.")
    summary_text = summary_text.replace("\n", "<br/>")
    elements.append(Paragraph(summary_text, styles["Normal"]))

    elements.append(Spacer(1, 12))

    # Table (Schedule)
    schedule = report.get("schedule", [])
    table_data = [["Stop", "Arrival (h)", "Departure (h)", "Deadline Missed (h)"]]
    for s in schedule:
        stop = s.get("stop_name", s.get("stop_id", ""))
        arr = s.get("arrival_time", 0.0)
        dep = s.get("departure_time", 0.0)
        miss = s.get("deadline_missed_hours", s.get("deadline_missed_hrs", 0.0))
        try:
            table_data.append([str(stop), f"{float(arr):.2f}", f"{float(dep):.2f}", f"{float(miss):.2f}"])
        except Exception:
            table_data.append([str(stop), str(arr), str(dep), str(miss)])

    table = Table(table_data, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Map image (optional)
    map_bytes = report.get("map_image_bytes")
    if map_bytes:
        # elements.append(Paragraph("<b>Route Map</b>", styles["Heading2"]))
        elements.append(Paragraph("Route Map", styles["Heading2"]))

        img_buf = io.BytesIO(map_bytes)
        # keep width/height flexible; adjust as needed
        elements.append(Image(img_buf, width=400, height=300))
        elements.append(Spacer(1, 8))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
