# -------------VISUAL SEARCH TASK------------- #
# This project is inspired by the work of Ulric Neisser,
# often referred to as the father of cognitive psychology.
# In his paper (1964) on visual search, Neisser explored how people
# perceive and process visual information,as well as how they organize
# and interpret it. As a small programming project, I recreated
# a simplified version of one of his visual search tasks.
# If you would like to learn more about the original study, you can
# access the paper here:
# https://doi.org/10.1038/scientificamerican0664-94
# So, how quickly can your brain find a specific letter among a bunch
# of distractions? Let's find out!
# Disclaimer: This project is intended for educational and entertainment
# purposes only. It is not a scientific assessment of attention,
# perception, or cognitive ability.
# -------------------------------------------- #
print('\033c')

import random
import string
import time
import os
import sys
import matplotlib.pyplot as plt

RED = "\033[31m"
RESET = "\033[0m"
START_BOLD = "\033[1m"
TARGET_LETTER = "K"
DISPLAY_WIDTH = 26


# Creating a string of alphabet letters without the letter "K" (used in trial 1,2,3,4).
alphabets = string.ascii_uppercase
no_k_string = "".join([letter for letter in alphabets if letter != "K"])

# Creating a string of letters + digits, then romoving "K" (used in trial 5,6).
alphabets_digits = string.ascii_uppercase + string.digits
no_k_string_digits = "".join([letter for letter in alphabets_digits if letter != "K"])

# Creating a string of letters + digits + punctuations, then romoving "K" (used in trial 7,8).
punctuations = "+=*@!#%?&+=*@!#%?&"  # didn't use string.punctuation as I wanted specfic punctuations.
string_digits_punctuations = string.ascii_uppercase + string.digits + punctuations
no_k_string_digits_punctuations = "".join(
    [letter for letter in string_digits_punctuations if letter != "K"]
)

# This generates a list of random non-target items and target item.
# Parameters:
# items_pool (str) = collection  of characters (e.g. letters, digits,
#   punctuations) that random.choices() pulls from to generate random items.
# num_items (int) = numbers of distractor items to generate. The target
#   item is added afterward, so the final list lenght is num_items + 1.
#   E.g., for a list of 4 items total (including the target), set num_items = 3
# item_length (int) = numbers of characters used to generate an item.
# target_letter (str) = target letter that will be added
#  in the generated item.


def create_search_list(items_pool, num_items, item_length, target_letter):
    my_list = []
    # Create random items that are not the target item.
    for i in range(num_items):
        random_items_no_k = "".join(random.choices(items_pool, k=item_length))
        my_list.append(random_items_no_k)
    # Create target item.
    target_item = "".join(random.choices(items_pool, k=item_length - 1)) + target_letter
    # make sure that "target letter" appears at any position of the string.
    target_item = "".join(random.sample(target_item, len(target_item)))

    my_list.append(target_item)
    random.shuffle(my_list)
    return my_list, target_item


# user input. Also, make sure the input is valid.
def get_valid_answer(target_item):
    expected_answer_length = len(target_item)
    while True:
        user_answer = (
            input(f"Enter the full item containing {TARGET_LETTER}: ").strip().upper()
        )
        if len(user_answer) == expected_answer_length:
            return user_answer
        else:
            print(
                f"{RED}!!!!Your answer MUST contain {expected_answer_length} characters.{RESET}"
            )
            print("")


def run_trial(item_pool, num_items, item_length):
    trial_list, target_item = create_search_list(
        item_pool, num_items, item_length, TARGET_LETTER
    )

    print("----------------------------")
    for item in trial_list:
        print(f"{item:^{DISPLAY_WIDTH}}")
    print("----------------------------")

    # user input
    start_time = time.perf_counter()
    user_answer = get_valid_answer(target_item)
    end_time = time.perf_counter()
    rt = (end_time - start_time)  # total reaction time (how long it took the user to answer).

    if user_answer == target_item:
        print("Correct")
        print("")
        is_correct = True
    else:
        print(f"Sorry, the answer is {RED}{target_item}{RESET}.")
        is_correct = False
        print("")

    return rt, is_correct


def continue_or_quit_prompt():
    while True:
        enter = (
            input(
                "Press the Enter key if you want to continue the task OR type 'quit' to stop: "
            )
            .strip()
            .lower()
        )
        if enter == "":
            break
        elif enter == "quit":
            print("Thank you for your time. Have a wonderful day!")
            sys.exit()  # end the task.
    os.system("cls||clear")  # clear the terminal before moving to next trial.


def main():
    reactions_time = []
    incorrect_answers = 0
    correct_answers = 0

    # introduction
    print(f"{START_BOLD}THE LETTER K - Visual Search Task {RESET}")
    print("------------------------------------------------------------")
    print("Welcome!")
    print("")
    print(
        f"- In this task, your goal is to find the item that contains the letter{START_BOLD} K {RESET}."
    )
    print(
        "- A list of random items will appear on the screen. Find the target item as quickly as possible."
    )
    print(
        "- Important Note: Type the full item, not just the letter K, or your answer will not be accepted."
    )
    print(
        "- There will be 8 trials. Each trial will be presented only once, and the difficulty will increase with each trial."
    )
    print(
        "- At the end of the task, you will receive your results along with a small graph showing your reaction time for each trial."
    )
    print("")
    print("Have Fun!")
    print("------------------------------------------------------------")
    input("Press ENTER to start: ")
    os.system("cls||clear")

    trials = [
        [no_k_string, 3, 4],  # trial 1
        [no_k_string, 5, 4],  # trial 2
        [no_k_string, 5, 6],  # trial 3
        [no_k_string, 7, 6],  # trial 4
        [no_k_string_digits, 7, 6],  # trial 5
        [no_k_string_digits, 9, 6],  # trial 6
        [no_k_string_digits_punctuations, 9, 6],  # trial 7
        [no_k_string_digits_punctuations, 11, 6],  # trial 8
    ]

    for trial_number, trial in enumerate(trials, start=1):
        # unpacking list. For e.g., for the 1st loop, trial = [no_k_string, 3, 4].
        # no_k_string goes to item_pool, 3 goes to num_items, 4 to item_length and so on.
        item_pool, num_items, item_length = trial

        # skip the prompt before trial 1
        # show it again before each remaining trial.
        if trial_number > 1:
            continue_or_quit_prompt()

        rt, is_correct = run_trial(item_pool, num_items, item_length)
        reactions_time.append(rt)

        if is_correct:
            correct_answers += 1
        else:
            incorrect_answers += 1

    os.system("cls||clear")  # clear the terminal before the final results.

    # results
    average_reaction_time = sum(reactions_time) / len(reactions_time)
    avg = f"Average Reaction Time: {average_reaction_time:.1f} Seconds"  # 1f means 1 digit after the decimal.
    print("===========================================================")
    print("RESULTS:")
    print(f"Number of Correct Answers:{correct_answers}")
    print(f"Number of Incorrect Answers:{incorrect_answers}")
    print(f"Your Average Time: {average_reaction_time:.1f} Seconds")
    print("===========================================================")
    print("Task Completed!\nThank you for your Time and have a wonderful day.")

    # display graph of reaction time per trials
    trial_numbers = [1 + x for x in range(len(reactions_time))]
    fig, ax = plt.subplots(figsize=(5, 2), layout="constrained")  # figsize = (width, height) in inches.
    ax.plot(trial_numbers, reactions_time, c="blue", marker="o", label=avg)
    ax.set_title("Reaction Time Per Trial", fontsize=15)
    ax.set_xlabel("Trial Number")
    ax.set_ylabel("Reaction Time in Seconds")
    ax.text(
        1.02, 0.5, avg, fontsize=10, verticalalignment="center", transform=ax.transAxes
    )
    plt.show()


if __name__ == "__main__":
    main()
