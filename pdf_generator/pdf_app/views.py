from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.templatetags.static import static
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table, TableStyle

def GeneratePdf(request):
    # Get the HTML template
    template = get_template('pdf_template.html')
    context = {'data': 'Hello, World!'}  # Example data for the template

    # Render the template with the context
    html = template.render(context)

    # Create a PDF object and specify the paper size (e.g., letter)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="output.pdf"'
    p = canvas.Canvas(response, pagesize=letter)

    # Draw the letterhead with blue background color and an icon
    p.setFillColor(colors.HexColor('#0066CC'))
    p.rect(0, 750, 612, 100, fill=1)
    icon_path = 'https://cdn-icons-png.flaticon.com/128/4300/4300059.png'  # Update with the actual path to your icon
    p.drawImage(ImageReader(icon_path), 20, 760, width=60, height=60, mask='auto')

    # Draw the table with boilerplate data
    data = [['Column 1', 'Column 2', 'Column 3', 'Column 4', 'Column 5'],
            ['Data 1', 'Data 2', 'Data 3', 'Data 4', 'Data 5'],
            ['Data 6', 'Data 7', 'Data 8', 'Data 9', 'Data 10']]
    table = Table(data, colWidths=[100, 100, 100, 100, 100])
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E6F2FF')),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('FONTSIZE', (0, 0), (-1, 0), 14),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige)]))
    table.wrapOn(p, 0, 0)
    table.drawOn(p, 30, 650)

    p.showPage()
    p.save()

    return response
