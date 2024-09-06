import os

#  File path for saving
file_path = 'sports01.txt'

def read_sports(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    return []

#def equals define and runs function with called word_or_words
def write_sports(file_path,sports_list):
    with open('sports01.txt', 'w') as file:
        for sport in sports_list:
            file.write(f"{sport}\n")
#  repeats
repeat = "yes"
#  sports = []
while repeat == "yes":

    sports = read_sports(file_path)

    #  User input time
    new_sport = input("Enter your favourite sport: ").capitalize().strip()

    if new_sport:
        if new_sport in sports:
                    print(f"{new_sport} is already in the list.")
    #                del sports[sports.index(new_sport)]
        else:
            sports.append(new_sport)
            print("Updated sports list:", sports)
    else:
        print(f"No new sports added.")

    write_sports(file_path, sports)

    print("Sports list:")
    for i, sport in enumerate(sports):  # Loop through the sports list with index
        print(f"Sport {i+1}: {sport}")

    repeat = input("would you like to add another sport? (Yes/No): ").lower().strip()
print("Exiting the program.")  # When user exits program. "Exiting the program"
#END
