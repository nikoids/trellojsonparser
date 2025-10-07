The script parses the actions array in your Trello JSON, looking for updateCard actions where listAfter.name == "Done". For each task, it extracts:

Date: Formatted as YYYY-MM-DD HH:MM

Task Name: Full Azerbaijani/English text preserved

Card Link: Generated from shortLink for quick access

quick_parser.py (Simple Version)
Lightweight script that prints results directly to console. Just edit the filename in the script and run:

bash
python quick_parser.py

Complete script with CSV export functionality and detailed output. Run it with:

bash
python trello_parser.py trello_export.json
