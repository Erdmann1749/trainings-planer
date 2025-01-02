def ask_for_input():
    # function asks for user input
    name = input("Name des Trainers: ")
    time = input("Zeit der Trainingsstunde: ")
    day = input("Tag der Trainingsstunde: ")
    return f"{name} gibt am {day} um {time} Uhr eine Trainingsstunde."

if __name__ == "__main__":
    print(ask_for_input())
