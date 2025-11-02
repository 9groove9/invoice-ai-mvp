import argparse

from parse_invoice import load_invoice
from validation import validate_invoice
from ai_auditor import generate_audit_report
from exel_report import exel_report
from pdf_report import pdf_report
def main():
    parser = argparse.ArgumentParser(description='AI invoice audite system')
    parser.add_argument('--file', type=str, required=True, help='invoice exel filename')
    parser.add_argument('--mode', type=str, choices=['ai', 'rule_based'], 
                        default='auto', help='Switch between ai and rule-based pdf report')
    args = parser.parse_args()
    MODE = args.mode
    try:
        df = load_invoice(args.file)
    except Exception as e:
        print(f'Faild to load file: {e}')
    
    print(f'Loaded file: {args.file}')
    
    issues = validate_invoice(df)

    if not issues:
        print('No issues found - invoice looks clean!')
        return

    audit = generate_audit_report(issues, MODE)
    
    exel_report(audit['rule_based'])
    pdf_report(audit['rule_based'], audit['ai'], MODE)

    print('\n\nAll reports generated successfully')

if __name__ == '__main__':
    main()