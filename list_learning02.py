import os

#  File path for saving
file_path = 'sports02.txt'
#   Sports List
sports = []

#   Checks if file exists and reads the existing sports list
if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        sports = [line.strip() for line in file.readlines()]
#  repeats
repeat = "yes"
#   While
while repeat == "yes":

    #  User input time
    new_sport = input("Enter your favourite sport: ").capitalize().strip()

    if new_sport:
        if new_sport in sports:
                    print(f"{new_sport} is already in the list.")
        else:
            sports.append(new_sport)
            print("Updated sports list:", sports)
    else:
        print(f"No new sports added.")


    with open('sports01.txt', 'w') as file:
            for sport in sports:
                file.write(f"{sport}\n")

    print("Sports list:")
    for i, sport in enumerate(sports):  # Loop through the sports list with index
        print(f"Sport {i+1}: {sport}")

    repeat = input("would you like to add another sport? (Yes/No): ").lower().strip()
    if repeat != "yes":
        break
print("Exiting the program.")  # When user exits program. "Exiting the program"
#END
