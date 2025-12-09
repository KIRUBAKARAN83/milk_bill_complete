from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
from io import BytesIO

def generate_bill_pdf(customer, entries, total_ml, total_litres, total_amount, price_per_litre, year=None, month=None):
    """
    Generate PDF bill for customer
    Returns BytesIO object with PDF content
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#007bff'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#333333'),
        spaceAfter=6,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#333333'),
        spaceAfter=3,
    )
    
    # Build PDF content
    elements = []
    
    # Title (without emoji for PDF compatibility)
    title = Paragraph("MILK BILLING INVOICE", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Period info
    if year and month:
        period_text = f"Month: {month:02d}/{year}"
    else:
        period_text = "Full Bill"
    period = Paragraph(f"<b>{period_text}</b> | Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}", normal_style)
    elements.append(period)
    elements.append(Spacer(1, 0.2*inch))
    
    # Customer Details
    elements.append(Paragraph("<b>Customer Details</b>", heading_style))
    
    # Safe get customer data
    cust_name = customer.name if customer.name else "N/A"
    cust_phone = customer.phone if customer.phone else "N/A"
    cust_whatsapp = customer.whatsapp_number if hasattr(customer, 'whatsapp_number') and customer.whatsapp_number else "N/A"
    
    cust_data = [
        ['Name:', cust_name],
        ['Phone:', cust_phone],
        ['WhatsApp:', cust_whatsapp],
    ]
    cust_table = Table(cust_data, colWidths=[1.5*inch, 3.5*inch])
    cust_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(cust_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Milk Entries Table
    elements.append(Paragraph("<b>Milk Entries</b>", heading_style))
    
    table_data = [['Date', 'Qty (ml)', 'Litres', 'Price/L (Rs)', 'Amount (Rs)']]
    
    if entries.exists():
        for entry in entries:
            table_data.append([
                entry.date.strftime('%d-%m-%Y'),
                str(entry.quantity_ml),
                f"{float(entry.litres):.3f}",
                f"Rs {price_per_litre}",
                f"Rs {float(entry.amount):.2f}"
            ])
    else:
        table_data.append(['No entries found', '', '', '', ''])
    
    # Add totals row
    table_data.append([
        'TOTAL',
        str(total_ml),
        f"{float(total_litres):.2f}",
        f"Rs {price_per_litre}",
        f"Rs {float(total_amount):.2f}"
    ])
    
    # Create table with styling
    entries_table = Table(table_data, colWidths=[1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
    entries_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f4f8')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f9f9f9')]),
    ]))
    elements.append(entries_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Summary
    summary_data = [
        ['Total Quantity:', f"{total_ml} ml"],
        ['Total Litres:', f"{float(total_litres)} L"],
        ['Rate per Litre:', f"Rs {price_per_litre}"],
        ['TOTAL AMOUNT:', f"Rs {float(total_amount):.2f}"],
    ]
    summary_table = Table(summary_data, colWidths=[2.5*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -2), 10),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#28a745')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Footer
    footer = Paragraph("<i>Thank you for your business! For queries, contact us.</i>", 
                      ParagraphStyle('footer', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER))
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer