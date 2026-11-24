import json
import os
from datetime import datetime

DATA_FILE = "deadlines.json"
REPORT_FILE = "DEADLINE_CHECKLIST.md"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def calculate_urgency(deadline_str):
    deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
    today = datetime.now()
    days_left = (deadline - today).days

    if days_left < 0:
        return days_left, "EXPIRED"
    elif days_left <= 14:
        return days_left, "CRITICAL (Submit ASAP)"
    elif days_left <= 45:
        return days_left, "HIGH PRIORITY (Prepare Docs)"
    else:
        return days_left, "ON TRACK"

def add_opportunity():
    title = input("Enter University / Conference Name (e.g., KAUST MS/PhD): ").strip()
    category = input("Category (Scholarship / Conference / Journal): ").strip().capitalize()
    deadline = input("Enter Deadline (YYYY-MM-DD, e.g., 2027-01-03): ").strip()

    try:
        datetime.strptime(deadline, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format! Use YYYY-MM-DD.\n")
        return

    tasks = input("Required Docs (comma-separated, e.g., SOP, IELTS, 3 LORs): ").strip()

    data = load_data()
    data.append({
        "title": title,
        "category": category,
        "deadline": deadline,
        "tasks": [t.strip() for t in tasks.split(",") if t.strip()]
    })
    save_data(data)
    print(f"'{title}' added to your radar!\n")

def view_radar():
    data = load_data()
    if not data:
        print("No deadlines tracked yet.\n")
        return

    print("\n" + "=" * 60)
    print("ACADEMIC & SCHOLARSHIP DEADLINE RADAR")
    print("=" * 60)
    for idx, item in enumerate(data, 1):
        days_left, status = calculate_urgency(item["deadline"])
        print(f"{idx}. {item['title']} [{item['category']}]")
        print(f"   Deadline: {item['deadline']} | Days Left: {max(days_left, 0)} | Status: {status}")
        print(f"   Checklist: {', '.join(item['tasks'])}")
        print("-" * 60)
    print()

def export_markdown():
    data = load_data()
    if not data:
        print("Nothing to export.\n")
        return

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("# Academic & Scholarship Application Tracker\n\n")
        f.write(f"*Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
        for item in data:
            days_left, status = calculate_urgency(item["deadline"])
            f.write(f"## {item['title']} ({item['category']})\n")
            f.write(f"- **Deadline:** `{item['deadline']}` ({max(days_left, 0)} days remaining)\n")
            f.write(f"- **Urgency Status:** **{status}**\n")
            f.write("- **Action Items:**\n")
            for task in item["tasks"]:
                f.write(f"  - [ ] {task}\n")
            f.write("\n")

    print(f"Markdown checklist exported successfully to '{REPORT_FILE}'!\n")

def main():
    while True:
        print("1. Add Deadline | 2. View Radar | 3. Export Markdown Report | 4. Exit")
        choice = input("Select an option: ").strip()
        if choice == "1":
            add_opportunity()
        elif choice == "2":
            view_radar()
        elif choice == "3":
            export_markdown()
        elif choice == "4":
            print("Exiting Radar. Good luck with your applications!")
            break
        else:
            print("Invalid choice!\n")

if __name__ == "__main__":
    main()
