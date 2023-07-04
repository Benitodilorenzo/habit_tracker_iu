import json
import datetime
from datetime import timedelta
import random

class Habit:
    def __init__(self, name, period):
        """
        Initialize a Habit object with a name and period (daily or weekly).
        Also sets the creation time to the current time and initializes an empty list of completions.
        """
        self.name = name
        self.period = period
        self.creation_time = str(datetime.datetime.now())
        self.completions = []

    def start_date(self):
        """
        Return the start date of the habit, which is the date of the first completion.
        If there are no completions, return None.
        """
        if self.completions:
            return min(completion.date() for completion in self.completions)
        else:
            return None

    def track_streaks(self):
        """
        Track the streaks of habit completion based on the habit's period (daily or weekly).
        If the period is neither daily nor weekly, raise a ValueError.
        """
        if self.period == 'daily':
            return self._track_daily_streaks()
        elif self.period == 'weekly':
            return self._track_weekly_streaks()
        else:
            raise ValueError(f'Unknown habit period: {self.period}')

    def _track_daily_streaks(self):
        """
        Track the daily streaks of habit completion.
        A new streak starts when there is a day without habit completion.
        If there are no completions, return an empty list.
        """
        if not self.completions:
            return []

        # Sort completion dates
        dates = sorted(self.completions)

        streaks = []
        current_streak = [dates[0]]

        for i in range(1, len(dates)):
            previous_date = dates[i - 1]
            current_date = dates[i]
            if (current_date - previous_date).days <= 1:
                current_streak.append(current_date)
            else:
                streaks.append(current_streak)
                current_streak = [current_date]

        streaks.append(current_streak)
        return streaks




    def _track_weekly_streaks(self):
        """
        Track the weekly streaks of habit completion.
        A new streak starts when there is a week without habit completion.
        If there are no completions, return an empty list.
        """
        if not self.completions:
            return []

        # Sort completions in ascending order
        self.completions.sort()

        streaks = []
        current_streak = [self.completions[0]]

        for i in range(1, len(self.completions)):
            previous_date = self.completions[i - 1]
            current_date = self.completions[i]
            if (current_date - previous_date).days <= 7:
                current_streak.append(current_date)
            else:
                streaks.append(current_streak)
                current_streak = [current_date]

        streaks.append(current_streak)
        return streaks




    def calculate_streak_duration(self, streak):
        """
        Calculate the duration of a given streak in days.
        If the streak is empty, return 0.
        """
        if not streak:
            return 0
        streak_start = streak[0]
        streak_end = streak[-1]
        return (streak_end - streak_start).days + 1

    def calculate_average_streak_duration(self):
        """
        Calculate the average duration of all streaks in days.
        If there are no streaks, return 0.
        """
        streaks = self.track_streaks()
        total_streak_duration = sum(self.calculate_streak_duration(streak) for streak in streaks)
        total_streaks = len(streaks)
        return total_streak_duration / total_streaks if total_streaks > 0 else 0

    def find_longest_streak(self):
        """
        Find the longest streak and return its duration in days.
        If there are no streaks, return 0.
        """
        streaks = self.track_streaks()
        longest_streak = max(streaks, key=self.calculate_streak_duration, default=[])
        return self.calculate_streak_duration(longest_streak)

    def find_shortest_streak(self):
        """
        Find the shortest streak and return its duration in days.
        If there are no streaks, return 0.
        """
        streaks = self.track_streaks()
        shortest_streak = min(streaks, key=self.calculate_streak_duration, default=[])
        return self.calculate_streak_duration(shortest_streak)








    def complete(self):
        """
        Mark the habit as completed for the current day.
        If the habit has already been completed for the current day, print a message and do nothing.
        """
        now = datetime.datetime.now()
        if any(now.date() == completion.date() for completion in self.completions):
            print("Habit already completed for today.")
        else:
            self.completions.append(now)  # storing datetime object directly

    def generate_example_data(self):
        """
        Generate example completion data for the habit.

        If the habit's period is 'daily', generate up to 28 days of completion data.
        If the habit's period is 'weekly', generate up to 4 weeks of completion data.
        For each day or week, randomly decide whether to add a completion.
        The completion dates are relative to a fixed reference date.

        This method is useful for testing and demonstration purposes.
        """
        reference_date = datetime.date(2023, 5, 1)  # Choose a fixed reference date

        if self.period == 'daily':
            for i in range(28):
                if random.choice([True, False]):  # Randomly decide whether to add a completion
                    completion_date = reference_date + datetime.timedelta(days=i)
                    self.completions.append(completion_date)
        elif self.period == 'weekly':
            for i in range(4):
                if random.choice([True, False]):  # Randomly decide whether to add a completion
                    completion_date = reference_date + datetime.timedelta(weeks=i)
                    self.completions.append(completion_date)







    def get_streak(self):
        """
        Calculate and return the longest streak of consecutive completions.
        A streak is considered broken if the gap between two consecutive completions is more than one day for daily habits, or more than one week for weekly habits.
        """
        dates = [completion for completion in self.completions]

        dates.sort()
        streak = 0
        max_streak = 0
        gap = datetime.timedelta(days=1 if self.period == 'daily' else 7) 
        for i in range(1, len(dates)):
            if dates[i] - dates[i-1] <= gap:
                streak += 1
            else:
                max_streak = max(max_streak, streak)
                streak = 0
        max_streak = max(max_streak, streak)
        return max_streak

    def to_dict(self):
        """
        Convert the habit to a dictionary.
        This can be useful for serialization, for example when saving the habit to a file.
        """
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        """
        Create a Habit object from a dictionary.
        This is a class method, meaning it's called on the class itself, not on an instance of the class.
        It's a common pattern for alternative constructors.
        """
        habit = cls(data['name'], data['period'])
        habit.completions = [datetime.datetime.strptime(completion, "%Y-%m-%d").date() for completion in data['completions']]  # Converting strings to date objects
        return habit



class HabitTracker:
    def __init__(self):
        """
        Initialize a HabitTracker object with an empty list of habits.
        """
        self.habits = []

    PREDEFINED_HABITS = [
        "Exercise",
        "Exercise (with example data)",
        "Meditation",
        "Meditation (with example data)",
        "Reading",
        "Reading (with example data)",
        "Coding",
        "Coding (with example data)",
        "Sleeping Early",
        "Sleeping Early (with example data)"
    ]

    def add_habit(self):
        """
        Interactively add a habit to the tracker.
        The user can select a habit from a predefined list or enter a custom habit.
        The user also needs to specify the habit period (daily or weekly).
        If a habit with example data is choosen, then example data gets created, using the 'generate_example_data' method
        """
        print("Select a habit from the list or enter a custom habit:")
        for i, habit in enumerate(self.PREDEFINED_HABITS, start=1):
            print(f"{i}. {habit}")
        print(f"{len(self.PREDEFINED_HABITS) + 1}. Custom Habit")

        choice = input("Enter choice: ")
        if not choice.isdigit() or not 1 <= int(choice) <= len(self.PREDEFINED_HABITS) + 1:
            print("Invalid choice. Please try again.")
            return
        if int(choice) == len(self.PREDEFINED_HABITS) + 1:
            name = input("Enter custom habit name: ")
        else:
            name = self.PREDEFINED_HABITS[int(choice) - 1]

        period = input("Enter habit period (daily or weekly): ")
        if period not in ['daily', 'weekly']:
            print("Invalid period. Please enter 'daily' or 'weekly'.")
            return

        new_habit = Habit(name, period)
        if "(with example data)" in name:
            new_habit.generate_example_data()
        self.habits.append(new_habit)

        

    def add_custom_habit(self, habit):
        """
        Add a custom habit to the tracker.
        The habit should be an instance of the Habit class.
        """
        self.habits.append(habit)

    def remove_habit(self, name):
        """
        Remove a habit from the tracker by its name.
        If the habit is not found, do nothing.
        """
        self.habits = [habit for habit in self.habits if habit.name != name]

    def get_habit(self, name):
        """
        Get a habit from the tracker by its name.
        If the habit is not found, return None.
        """
        for habit in self.habits:
            if habit.name == name:
                return habit
        return None

    def list_habits(self):
        """
        Return a list of the names of all habits in the tracker.
        """
        return [habit.name for habit in self.habits]

    def habits_by_periodicity(self):
        """
        Print the names of all habits in the tracker, grouped by their periodicity (daily or weekly).
        """
        daily_habits = []
        weekly_habits = []

        for habit in self.habits:
            if habit.period == 'daily':
                daily_habits.append(habit.name)
            elif habit.period == 'weekly':
                weekly_habits.append(habit.name)

        print("Habits by Periodicity:")
        print(f"Daily Habits: {', '.join(daily_habits)}")
        print(f"Weekly Habits: {', '.join(weekly_habits)}")
        print()

    def longest_run_streak(self):
        """
        Return the name of the habit with the longest run streak.
        """
        return max(self.habits, key=lambda habit: habit.get_streak()).name





    def view_streaks(self):
        """
        Print the streaks for all habits in the tracker.
        For each habit, this includes the start and end date of each streak, the number of days in the streak,
        the average streak length, the longest streak, and the shortest streak.
        """

        print("Streaks for all habits:")
        for habit in self.habits:
            print(f"Habit: {habit.name} (Periodicity: {habit.period})")
            streaks = habit.track_streaks()
            if streaks:
                total_days = 0
                for streak in streaks:
                    start_date = streak[0].strftime("%Y-%m-%d")
                    end_date = streak[-1].strftime("%Y-%m-%d")
                    streak_days = (streak[-1] - streak[0]).days + 1
                    print(f"- {start_date} - {end_date} ({streak_days} {'day' if streak_days == 1 else 'days'})")
                    total_days += streak_days

                average_streak_length = habit.calculate_average_streak_duration()
                longest_streak = habit.find_longest_streak()
                shortest_streak = habit.find_shortest_streak()

                print(f"  Average streak length: {average_streak_length:.2f} {'day' if average_streak_length == 1 else 'days'}")
                print(f"  Longest streak: {longest_streak} {'day' if longest_streak == 1 else 'days'}")
                print(f"  Shortest streak: {shortest_streak} {'day' if shortest_streak == 1 else 'days'}")
                # print("  "+ self.longest_run_streak())

            else:
                print("No streaks found.")
        print()
 


    def find_struggling_habit(self):
        """
        Find and print the habit with the lowest and highest average streak length.
        If there are no habits or all habits have no completions, print a message indicating that no struggling or best habits were found.
        """

        lowest_average_streak = float('inf')
        highest_average_streak = float('-inf')
        struggling_habit = None
        best_habit = None
        for habit in self.habits:
            if len(habit.completions) > 0:
                streaks = habit.track_streaks()
                total_streaks = len(streaks)
                total_days = sum((streak[-1] - streak[0]).days + 1 for streak in streaks)
                if total_streaks > 0:
                    average_streak_length = total_days / total_streaks
                    if average_streak_length < lowest_average_streak:
                        lowest_average_streak = average_streak_length
                        struggling_habit = habit.name
                    if average_streak_length > highest_average_streak:
                        highest_average_streak = average_streak_length
                        best_habit = habit.name
        if struggling_habit:
            print(f"The habit you struggle with the most is: {struggling_habit}")
            print(f"Average streak length: {lowest_average_streak:.2f} days")
        else:
            print("No struggling habits found.")
        if best_habit:
            print(f"The habit you are best at is: {best_habit}")
            print(f"Average streak length: {highest_average_streak:.2f} days")
        else:
            print("No best habits found.")



    def load_from_file(self, filename):
        """
        Load habits from a JSON file.
        If the file does not exist, create it and initialize it with an empty list.
        """

        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                for habit_data in data:
                    habit = Habit.from_dict(habit_data)  # Use from_dict to convert
                    self.habits.append(habit)
        except FileNotFoundError:
            with open(filename, 'w') as file:  # This will create the file
                json.dump([], file)  # Initialize with an empty list


    def save_to_file(self, filename):
        """
        Save habits to a JSON file.
        """

        data = []
        for habit in self.habits:
            habit_data = {
                'name': habit.name,
                'period': habit.period,
                'creation_time': str(habit.creation_time),
                'completions': [str(completion) for completion in habit.completions]
            }
            data.append(habit_data)
        with open(filename, 'w') as file:
            json.dump(data, file)


def main():
    """
    The main function of the program.
    It creates a HabitTracker, loads habits from a file, and then enters a loop where the user can interactively manage their habits.
    When the user chooses to exit, the habits are saved to a file.
    """
    tracker = HabitTracker()
    tracker.load_from_file('habits.json')

    while True:
        print("1. Add Habit")
        print("2. Remove Habit")
        print("3. Complete Habit")
        print("4. List Habits by Periodicity")
        print("5. View Streaks")
        print("6. Find Struggling Habit")  # New option
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            tracker.add_habit()
        elif choice == '2':
            name = input("Enter habit name: ")
            tracker.remove_habit(name)
        elif choice == '3':
            name = input("Enter habit name: ")
            tracker.get_habit(name).complete()
        elif choice == '4':
            print(tracker.habits_by_periodicity())
        # elif choice == '6':
        #     print(tracker.longest_run_streak())

        elif choice == '5':
            tracker.view_streaks()
        elif choice == '6':
            tracker.find_struggling_habit()  # New option
        elif choice == '7':                                                                                                                                                                   
            tracker.save_to_file('habits.json')
            break

if __name__ == "__main__":
    main()
