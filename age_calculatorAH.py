import os
repeat = "yes"
while repeat == "yes":

    #  input
    name = input("Enter your name? ").strip()
    birth_year = int(input("Enter your birth year: ").strip())
    age = 2024 - birth_year
    #  ideal place for negative number if else
    is_thisyear = input("Have you had your birthday yet this year? (Yes/No): ").lower().strip()
    if is_thisyear == "no":
        age = age - 1

#  If negative tell user
    if age == age < 0:
        print("Sorry, you entered a year that has not passed yet.")
    else:
        print(f"Hi, {name}, you are {age} years old")
    # Should be Hi, name, you are age years old.

    #  repeat func
    repeat = input("would you like to run the program again (Yes/No): ").lower().strip()
    os.system('cls')
#  if repeat == "no": thank the user and exit program
print("Thank you for using the age calculator!")
#  Should be "Thank you for using the age calculator"
