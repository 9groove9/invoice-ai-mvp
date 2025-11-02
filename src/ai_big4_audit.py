'''
Big-4 style reasoning module.
If no OpenAI key — returns clean fallback text.
'''

import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
AI_CONNECTED = True

SYSTEM_PROMPT = '''
You are a senior financial auditor from a Big-4 firm (Deloitte / EY / PwC / KPMG).
Tone: formal, concise, precise. Business and finance language.
Format responses as:

Issue:
Reason:
Risk:
Recommendation:

Keep each section 1–2 sentences.
'''


def _client():
    key = os.getenv('OPENAI_API_KEY')
    if not key:
        return None
    try:
        return OpenAI(api_key=key)
    except:
        return None


def explain_issue(issue, severity, impact, action, mode):

    client = _client()
    plain = (
            f'Issue: {issue}\n'
            f'Reason: Likely data entry or vendor processing error.\n'
            f'Severity: {severity}\n'
            f'Risk: {impact}\n'
            f'Recommendation: {action}\n'
    )
    pdf = (
            f'<b>Issue</b>: {issue}<br/>'
            f'<b>Reason</b>: Likely data entry or vendor processing error.<br/>'
            f'<b>Severity</b>: {severity}<br/>'
            f'<b>Risk</b>: {impact}<br/>'
            f'<b>Recommendation</b>: {action}<b/>'
        )
    if client is None or mode=='rule_based':        
        # fallback – clean professional template
        global AI_CONNECTED
        AI_CONNECTED = False
        return {'plain': plain, 'pdf': pdf}

    prompt = f"""
    Issue found: {issue}
    Impact: {impact}
    Recommended corrective action: {action}
    Generate auditor commentary.
    """
    try:
        resp = client.chat.completions.create(
            model='gpt-4.1-mini',
            messages=[
                {'role':'system','content':SYSTEM_PROMPT},
                {'role':'user','content':prompt},
            ],
            temperature=0.2
        )
        text = resp.choices[0].message.content.strip()


        pdf_text = (
            text
            .replace('Issue:', '<b>Issue:</b>')
            .replace('Reason:', '<b>Reason:</b>')
            .replace('Severity:', '<b>Severity:</b>')
            .replace('Risk:', '<b>Risk:</b>')
            .replace('Recommendation:', '<b>Recommendation:</b>')
            .replace('\n', '<br/>')
        )
        return {'plain': text, 'pdf': pdf_text}
    except:
        return {'plain': plain, 'pdf': pdf}
