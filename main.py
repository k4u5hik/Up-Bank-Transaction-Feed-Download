import requests
import csv
import json

# Replace with your API token
api_token = 'YOUR-API-TOKEN-HERE'
headers = {
    'Authorization': f'Bearer {api_token}',
}

# Step 1: Get the list of accounts
accounts_url = 'https://api.up.com.au/api/v1/accounts'
response = requests.get(accounts_url, headers=headers)
accounts = response.json()['data']

# Step 2: Retrieve transactions for each account
transactions = []
for account in accounts:
    account_id = account['id']
    transactions_url = f'https://api.up.com.au/api/v1/accounts/{account_id}/transactions'
    while transactions_url:
        response = requests.get(transactions_url, headers=headers)
        data = response.json()
        transactions.extend(data['data'])
        transactions_url = data['links']['next']

# Step 3: Export transactions to CSV
csv_file = 'transactions.csv'
csv_columns = ['id', 'status', 'rawText', 'description', 'message', 'amount', 'currencyCode', 'createdAt', 'settledAt']

with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=csv_columns)
    writer.writeheader()
    for transaction in transactions:
        transaction_data = transaction['attributes']
        row = {
            'id': transaction['id'],
            'status': transaction_data['status'],
            'rawText': transaction_data.get('rawText', ''),
            'description': transaction_data['description'],
            'message': transaction_data.get('message', ''),
            'amount': transaction_data['amount']['value'],
            'currencyCode': transaction_data['amount']['currencyCode'],
            'createdAt': transaction_data['createdAt'],
            'settledAt': transaction_data.get('settledAt', '')
        }
        writer.writerow(row)

print(f'Transactions have been exported to {csv_file}')
