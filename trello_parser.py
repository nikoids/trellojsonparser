
import json
from datetime import datetime
from collections import defaultdict

def parse_trello_done_tasks(json_file_path):
    """
    Parse Trello JSON export and extract tasks from Done list

    Args:
        json_file_path: Path to the Trello JSON export file

    Returns:
        List of tuples (date, task_name, card_id)
    """
    # Load JSON file
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    done_tasks = []
    seen_cards = set()  # To avoid duplicates

    # Method 1: Check actions for cards moved to Done
    if 'actions' in data:
        for action in data['actions']:
            # Look for updateCard actions where card was moved to Done list
            if action.get('type') == 'updateCard':
                action_data = action.get('data', {})
                list_after = action_data.get('listAfter', {})

                # Check if moved to Done list
                if list_after.get('name') == 'Done':
                    card = action_data.get('card', {})
                    card_id = card.get('id')
                    card_name = card.get('name')
                    date_str = action.get('date')

                    if card_id and card_id not in seen_cards:
                        seen_cards.add(card_id)
                        # Parse date
                        if date_str:
                            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                            formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            formatted_date = 'N/A'

                        done_tasks.append({
                            'date': formatted_date,
                            'task_name': card_name,
                            'card_id': card_id,
                            'short_link': card.get('shortLink', '')
                        })

    # Method 2: Check lists directly for cards in Done list
    if 'lists' in data:
        done_list = None
        for lst in data['lists']:
            if lst.get('name') == 'Done':
                done_list = lst
                break

        if done_list and 'cards' in data:
            done_list_id = done_list.get('id')
            for card in data['cards']:
                if card.get('idList') == done_list_id:
                    card_id = card.get('id')
                    if card_id not in seen_cards:
                        seen_cards.add(card_id)
                        # Use dateLastActivity as the date
                        date_str = card.get('dateLastActivity') or card.get('due')
                        if date_str:
                            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                            formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            formatted_date = 'N/A'

                        done_tasks.append({
                            'date': formatted_date,
                            'task_name': card.get('name'),
                            'card_id': card_id,
                            'short_link': card.get('shortLink', '')
                        })

    # Sort by date (most recent first)
    done_tasks.sort(key=lambda x: x['date'], reverse=True)

    return done_tasks

def print_done_tasks(done_tasks):
    """Print done tasks in a formatted way"""
    if not done_tasks:
        print("No tasks found in Done list")
        return

    print(f"\n{'='*80}")
    print(f"Total Done Tasks: {len(done_tasks)}")
    print(f"{'='*80}\n")

    for i, task in enumerate(done_tasks, 1):
        print(f"{i}. Date: {task['date']}")
        print(f"   Task: {task['task_name']}")
        print(f"   Link: https://trello.com/c/{task['short_link']}")
        print()

def export_to_csv(done_tasks, output_file='trello_done_tasks.csv'):
    """Export done tasks to CSV file"""
    import csv

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Task Name', 'Card ID', 'Link'])

        for task in done_tasks:
            writer.writerow([
                task['date'],
                task['task_name'],
                task['card_id'],
                f"https://trello.com/c/{task['short_link']}"
            ])

    print(f"Exported to {output_file}")

# Usage example:
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python trello_parser.py <path_to_json_file>")
        print("Example: python trello_parser.py trello_export.json")
        sys.exit(1)

    json_file = sys.argv[1]

    # Parse tasks
    done_tasks = parse_trello_done_tasks(json_file)

    # Print to console
    print_done_tasks(done_tasks)

    # Export to CSV
    export_to_csv(done_tasks)
