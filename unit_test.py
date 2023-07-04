import unittest
from datetime import datetime, timedelta


from habit_tracker import Habit, HabitTracker

class TestHabit(unittest.TestCase):
    def setUp(self):
        self.habit = Habit('Test Habit', 'daily')

    def test_complete(self):
        self.habit.complete()
        self.assertEqual(len(self.habit.completions), 1)

    def test_track_streaks(self):
        self.habit.generate_example_data()
        streaks = self.habit.track_streaks()
        self.assertTrue(len(streaks) > 0)  # Expect at least one streak

    def test_calculate_streak_duration(self):
        self.habit.generate_example_data()
        streak = self.habit.completions
        duration = self.habit.calculate_streak_duration(streak)
        self.assertGreaterEqual(duration, 1)  # Expect a streak duration of at least 1 day



    def test_calculate_average_streak_duration(self):
        self.habit.completions = [datetime.now() - timedelta(days=i) for i in range(6)]
        average_duration = self.habit.calculate_average_streak_duration()
        self.assertEqual(average_duration, 5)

    def test_find_longest_streak(self):
        self.habit.completions = [datetime.now() - timedelta(days=i) for i in range(6)]
        longest_streak = self.habit.find_longest_streak()
        self.assertEqual(longest_streak, 5)

    def test_find_shortest_streak(self):
        self.habit.completions = [datetime.now() - timedelta(days=i) for i in range(6)]
        shortest_streak = self.habit.find_shortest_streak()
        self.assertEqual(shortest_streak, 5)


class TestHabitTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = HabitTracker()

    def test_add_custom_habit(self):
        habit = Habit('Test Habit', 'daily')
        self.tracker.add_custom_habit(habit)
        self.assertEqual(len(self.tracker.habits), 1)

    def test_remove_habit(self):
        habit = Habit('Test Habit', 'daily')
        self.tracker.add_custom_habit(habit)
        self.tracker.remove_habit('Test Habit')
        self.assertEqual(len(self.tracker.habits), 0)

    def test_get_habit(self):
        habit = Habit('Test Habit', 'daily')
        self.tracker.add_custom_habit(habit)
        retrieved_habit = self.tracker.get_habit('Test Habit')
        self.assertEqual(retrieved_habit, habit)

    def test_list_habits(self):
        habit = Habit('Test Habit', 'daily')
        self.tracker.add_custom_habit(habit)
        habit_list = self.tracker.list_habits()
        self.assertEqual(habit_list, ['Test Habit'])

if __name__ == '__main__':
    unittest.main()
