#   Learning lists
'''
sports = [Basketball]
print(sports)
print(type(sports))
print(len(sports))
#  List starts at zero
print(sports[0])
print(sports[-1])
print(sports[-2])
print(sports[0:3])
print(type(sports[3]))
#  instead of this:
#  print(type(sports[0]))
#  print(type(sports[1]))
#  print(type(sports[2]))
#  print(type(sports[3]))
#  This is faster:

for sport in sports:
    print(type(sport))
    print(sport)
'''
repeat = "yes"
sports = []
while repeat == "yes":
    new_sport = input("Enter your favourite sport: ")
    if new_sport:
        sports.append(new_sport)
        print("updated sports list: ", sports)
    else:
        print("No new sports added.")
        print("Sports List:", sports)

    for i, sport in enumerate(sports):  # Loop through the sports list with index
        print(f"Sport {i+1}: {sport}")  # print the index and sport, starting at one

    repeat = input("would you like to add another sport? (Yes/No): ").lower().strip()
print("Exiting the program.")  # When user exits program. "Exiting the program"


#END
