import sqlite3
from datetime import date
import matplotlib.pyplot as plt

# Function to create the database and table
def create_db():
    conn = sqlite3.connect('habit_tracker.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS habits
                 (id INTEGER PRIMARY KEY, habit_name TEXT, date TEXT, completed INTEGER)''')
    conn.commit()
    conn.close()

# Function to add a habit
def add_habit(habit_name):
    conn = sqlite3.connect('habit_tracker.db')
    c = conn.cursor()
    today = date.today().strftime("%Y-%m-%d")
    c.execute("INSERT INTO habits (habit_name, date, completed) VALUES (?, ?, ?)",
              (habit_name, today, 0))  # Default completed as 0 (not done)
    conn.commit()
    conn.close()
    print(f"Habit '{habit_name}' added for today.")

# Function to mark a habit as completed
def mark_habit_completed(habit_name, completed=True):
    today = date.today().strftime("%Y-%m-%d")
    conn = sqlite3.connect('habit_tracker.db')
    c = conn.cursor()
    c.execute("UPDATE habits SET completed = ? WHERE habit_name = ? AND date = ?",
              (int(completed), habit_name, today))
   
    if c.rowcount == 0:  # If no rows were updated
        print(f"No habit found for '{habit_name}' today. Add it first!")
    else:
        status = "completed" if completed else "not completed"
        print(f"Habit '{habit_name}' marked as {status} for today.")
   
    conn.commit()
    conn.close()

# Function to plot habit progress
def plot_habit_progress(habit_name):
    conn = sqlite3.connect('habit_tracker.db')
    c = conn.cursor()
    c.execute("SELECT date, completed FROM habits WHERE habit_name = ?", (habit_name,))
    data = c.fetchall()
    conn.close()
   
    if not data:
        print(f"No data found for habit '{habit_name}'.")
        return
   
    dates = [d[0] for d in data]
    completions = [d[1] for d in data]
   
    plt.figure(figsize=(10, 6))
    plt.plot(dates, completions, marker='o', linestyle='-', color='b')
    plt.title(f"Progress for '{habit_name}'")
    plt.xlabel('Date')
    plt.ylabel('Completed (1 = Yes, 0 = No)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Function to display the menu
def show_menu():
    print("\nHabit Tracker Menu:")
    print("1. Add Habit")
    print("2. Mark Habit Completed")
    print("3. View Habit Progress")
    print("4. Exit")

# Main function to run the program
def main():
    create_db()
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()
       
        if choice == "1":
            habit_name = input("Enter habit name: ").strip()
            add_habit(habit_name)
        elif choice == "2":
            habit_name = input("Enter habit name: ").strip()
            mark_completed = input("Did you complete the habit today? (y/n): ").strip().lower()
            mark_habit_completed(habit_name, completed=(mark_completed == 'y'))
        elif choice == "3":
            habit_name = input("Enter habit name to view progress: ").strip()
            plot_habit_progress(habit_name)
        elif choice == "4":
            print("Exiting... Have a great day!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()