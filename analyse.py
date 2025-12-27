# analyse.py
import questionary
import pandas as pd
from db import get_tracker_data, get_db, display_table, get_all_counters


def calculate_count(db, name):
    '''
    Return aggregated metrics for a given habit.

    This function reads all tracker entries for the specified habit and
    computes two values:
    - the maximum runstreak ever achieved (historical maximum)
    - the current number of attempts, taken from the latest tracker entry

    Note:
        The 'attempts' field is stored as an accumulated counter in the
        tracker, therefore it must NOT be summed across rows.

    Args:
        db: Database instance.
        name (str): Name of the habit.

    Returns:
        tuple[int, int]: (max_runstreak, current_attempts)
    '''
    rows = get_tracker_data(db, name)
    # print(rows)
    if not rows:
        return 0, 0

    # Returns: max_runstreak and total_attempts of a given Habit
    max_runstreak = max(r['runstreak'] for r in rows)
    total_attempts = int(rows[-1]['attempts'])

    return max_runstreak, total_attempts

def longest_runstreak_task(db):
    '''
    Return the habit with the highest historical runstreak.

    For each habit, the maximum runstreak ever achieved is evaluated.
    The habit with the highest such value is returned.

    Args:
        db: Database instance.

    Returns:
        tuple[str | None, int]: (habit_name, max_runstreak)
        If no habits have tracker data, habit_name is None.
    '''

    counters = get_all_counters(db)
    best_task = None
    best_runstreak = 0

    for name in counters:
        rows = get_tracker_data(db, name)
        if not rows:
            continue
        max_rs = max(r['runstreak'] for r in rows)
        if max_rs > best_runstreak:
            best_runstreak = max_rs
            best_task = name

    return best_task, best_runstreak


def ranking_accomplished(db):
    '''
    Return a ranking of habits by their maximum historical runstreak.

    Each habit is evaluated based on the highest runstreak value it has
    ever reached. The resulting list is ordered in descending order.

    Args:
        db: Database instance.

    Returns:
        list[tuple[str, int]]: List of (habit_name, max_runstreak),
        ordered descending.
    '''

    counters = get_all_counters(db)
    ranking = []

    for name in counters:
        rows = get_tracker_data(db, name)
        if not rows:
            continue
        max_rs = max(r['runstreak'] for r in rows)
        ranking.append((name, max_rs))

    ranking.sort(key=lambda x: x[1], reverse=True)
    return ranking


def worst_habits(db):
    '''
    Return a ranking of habits by number of failed attempts.

    The attempts value is taken from the latest tracker entry of each habit,
    as attempts are stored as an accumulated counter.

    Habits with a higher number of attempts are considered worse and are
    ranked first.

    Args:
        db: Database instance.

    Returns:
        list[tuple[str, int]]: List of (habit_name, current_attempts),
        ordered descending.
    '''
    
    counters = get_all_counters(db)
    ranking = []

    for name in counters:
        rows = get_tracker_data(db, name)
        if not rows:
            continue
        last = rows[-1]
        att = int(last['attempts'])
        ranking.append((name, att))

    ranking.sort(key=lambda x: x[1], reverse=True)
    return ranking

def analyse_menu(db):
    '''
    Display the analysis submenu and handle user interaction.

    This menu allows the user to:
    - analyse a single habit
    - identify the habit with the longest historical runstreak
    - display a ranking by runstreak
    - display the worst habits based on number of attempts

    Args:
        db: Database instance
    '''
    
    # Open or create the database
    db_instance = get_db()
    # Prepare the Task data in a intuitive Table for the user
    db_display = display_table(db_instance)
    dt = pd.DataFrame(db_display)
    
    stop = False

    while not stop:
        choice = questionary.select(
            "Analysis options:",
            choices=[
                "Analyse one habit",
                "Longest runstreak habit",
                "Ranking by runstreak",
                "Worst habits (most attempts)",
                "Back"
            ]
        ).ask()

        if choice == "Analyse one habit":
            print(f'Habits that can be analysed \n\n{dt}\n\n')
            name = questionary.text("What's the name of your counter?").ask()
            accoplished_data = get_tracker_data(db, name)
            last = accoplished_data[-1]
            print(
                f"\n{name}:\n"
                f"Max runstreak: {last['runstreak']}\n"
                f"Total attempts: {last['attempts']}\n"
            )

        elif choice == "Longest runstreak habit":
            task, runstreak = longest_runstreak_task(db)
            print(f"\nBest habit: {task} with runstreak {runstreak}\n")

        elif choice == "Ranking by runstreak":
            ranking = ranking_accomplished(db)
            print("\nRanking by runstreak:")
            for name, rs in ranking:
                print(f"- {name}: {rs}")
            print()

        elif choice == "Worst habits (most attempts)":
            ranking = worst_habits(db)
            print("\nWorst habits:")
            for name, att in ranking:
                print(f"- {name}: {att} attempts")
            print()

        else:
            stop = True