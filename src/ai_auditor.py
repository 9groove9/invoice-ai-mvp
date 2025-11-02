# AI auditor
from ai_big4_audit import explain_issue
from ai_big4_audit import AI_CONNECTED
def generate_audit_report(issues, mode):
    audit = []

    for issue in issues:

        if 'duplicate' in issue.lower():
            audit.append({
                'issue': 'Duplicate Order ID Found',
                'severity': 'CRITICAL',
                'impact': 'Possible double-billing or duplicate liability.',
                'action': 'Verify ERP / WMS logs and request invoice correction.'
            })

        elif 'missing' in issue.lower():
            audit.append({
                'issue': 'Missing or Invalid Values',
                'severity': 'HIGH',
                'impact': 'Invoice cannot be validated or booked correctly.',
                'action': 'Request corrected invoice with complete fields.'
            })

        elif 'qty' in issue.lower():
            audit.append({
                'issue': 'Zero or Negative Quantity Detected',
                'severity': 'CRITICAL',
                'impact': 'Indicates returns or invoice data error.',
                'action': 'Check warehouse return records and confirm entry.'
            })

        elif 'price' in issue.lower():
            audit.append({
                'issue': 'Zero or Negative Price Detected',
                'severity': 'HIGH',
                'impact': 'May cause incorrect revenue / AP posting.',
                'action': 'Validate pricing with product catalog / ERP.'
            })

        else:
            audit.append({
                'issue': issue,
                'severity': 'MEDIUM',
                'impact': 'Data inconsistency.',
                'action': 'Review manually.'
            })
    if mode == 'ai' and AI_CONNECTED:
        print('OpenAI connected successfully')
    else:
        print('Rule-based AI response')
    print('\n==== AI AUDIT ANALYSIS (Big-4) ====\n')
    ai_audit=[]
    for item in audit:
        explanation = explain_issue(item['issue'],item['severity'], item['impact'], item['action'], mode)
        ai_audit.append(explanation['pdf'])
        print(explanation['plain'])
        print('-' * 60)


    return {'ai': ai_audit, 'rule_based': audit}