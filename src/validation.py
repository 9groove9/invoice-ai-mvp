import pandas as pd

def validate_invoice(df):    
    issues = []
    
    numeric_col = ['qty', 'price', 'shipping_cost']
    for col in numeric_col:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    if df['order_id'].duplicated().any():
        issues.append(f'Order_id have {df['order_id'].duplicated().sum()} duplicate(s)')
        
    important_cols = ['order_id', 'qty', 'sku', 'price', 'shipping_cost'] 
    if df[important_cols].isna().any().any():
        issues.append('Missing or invalid values in required fields')
    
    if (df['qty'] <= 0).any():
        issues.append('Non-positive qty found')
    if (df['price'] <= 0).any():
        issues.append('Non-positive price found')
    if (df['shipping_cost'] <= 0).any():
        issues.append('Non-positive shipping cost found')
    
    return issues