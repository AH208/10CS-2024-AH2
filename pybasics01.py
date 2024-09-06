#  do not delete and code, no marks if no comments in code


'''
name = "Fred"  # this variable contains a string 'str' which is (text)
age = 15  # this variable contains an integer 'int' which is a whole number
salary = 1000.50  # this variable contains a float 'float' which is a decimal number
is_student = True  # this variable contains a boolean 'bool' which is a true or false statement
'''

#  input variables for the user
name = input("Enter your name? ")
age = int(input("Enter your age? "))
salary = float(input("Enter your salary? "))
is_student = input("Are you a student? (True/False): ")

print(type(name))  # prints a string and name
print(type(age))  # prints an integer and age
print(type(salary))  # prints a float and salary
print(type(is_student))  # prints a boolean and yes/no student
print("Name: ", name)
if is_student == True:
    student = "Yes"
else:
    student = "No"
# Following is an f-string
print(f"{name}, is {age} years old, and earns ${salary} per month. Is he a student: {is_student}")
# Fred is 15 years old, and earns $1000.50 per month.
print(f"{name}, is {age} years old, and earns ${salary} per month. Is he a student: {student}")
