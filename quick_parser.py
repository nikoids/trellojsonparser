
import json
from datetime import datetime

# Quick script to extract Done tasks from Trello JSON

file_path = 'trello_export.json'  # Change this to your file name

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("\n" + "="*80)
print("DONE TASKS FROM TRELLO")
print("="*80 + "\n")

count = 0
seen = set()

# Parse actions to find cards moved to Done
for action in data.get('actions', []):
    if action.get('type') == 'updateCard':
        list_after = action.get('data', {}).get('listAfter', {})

        if list_after.get('name') == 'Done':
            card = action.get('data', {}).get('card', {})
            card_id = card.get('id')

            if card_id and card_id not in seen:
                seen.add(card_id)
                count += 1

                # Format date
                date_str = action.get('date', '')
                try:
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    formatted_date = date_obj.strftime('%Y-%m-%d %H:%M')
                except:
                    formatted_date = date_str

                print(f"{count}. [{formatted_date}] {card.get('name')}")

print(f"\n{'='*80}")
print(f"Total: {count} tasks")
print("="*80)
