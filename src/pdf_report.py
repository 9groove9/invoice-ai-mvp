from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

from ai_big4_audit import AI_CONNECTED

from datetime import datetime
from pathlib import Path

def pdf_report(audit, ai_audit, mode):    
    BASE_DIR = Path(__file__).resolve().parent.parent
    REPORTS_DIR = BASE_DIR / 'reports'
    REPORTS_DIR.mkdir(exist_ok=True)  
    file_path = str(REPORTS_DIR / 'audit_report.pdf')

    pdf = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []
    
    if mode == 'ai':
        title_name = 'AI Invoice Audit Report (Big-4)'
    else:
        title_name = 'AI Invoice Audit Report (Rule-based)'
        
    elements.append(Paragraph(f'<b>{title_name}</b>', styles['Title']))
    elements.append(Spacer(1, 12))
    
    date = Paragraph(
        f'Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}',
        styles['Normal']
    )
    elements.append(date)
    elements.append(Spacer(1, 12))
    
    if mode == 'ai' and AI_CONNECTED:
        for item in ai_audit:
            ai_resp = Paragraph(item, styles['Normal'])
            elements.append(ai_resp)
            elements.append(Spacer(1, 12))
            elements.append(HRFlowable(width='100%', color='black', thickness=1))
            elements.append(Spacer(1, 8))
    else:
        for item in audit:
            issue_title = Paragraph(f'<b>Issue:</b> {item['issue']}', styles['Heading4'])
            elements.append(issue_title)
        
            detail = f'''
            <b>Severity:</b> {item['severity']}<br/>
            <b>Impact:</b> {item['impact']}<br/>
            <b>Action:</b> {item['action']}
            '''
            paragraph = Paragraph(detail, styles['Normal'])
            elements.append(paragraph)
            elements.append(Spacer(1, 12))
            elements.append(HRFlowable(width='100%', color='black', thickness=1))
            elements.append(Spacer(1, 8))
    
    pdf.build(elements)
    print(f'PDF report saved to: {file_path}')