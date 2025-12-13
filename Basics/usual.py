'''
Basic syntax to work with python programming language
'''
def loop1():
    numbers = [1, 3, 4, 6, 7, 9, 10]
    #Iterate over list
    for num in numbers:
        if num % 2 == 0:
            print(f"{num} is even")
        else:
            print(f"{num} is odd")

# loop1()

def loop2():
    # Iterate from 0 to a given number(excludes the number)
    for i in range(5):
        print(f"I am number {i}")
    # Iterate from a given number to another given number(excludes the last one)
    for j in range(3,10):
        print(f"Hey, this is {j}")

# loop2()

def test_if_else():
    # Example 1
    fruits = ['mango', 'apple', 'orange', 'banana', 'pineapple', 'papaya']
    size = len(fruits)
    if size > 0 and size < 3:
        print(f"We have {size} fruits available")
    elif size > 2 and size <= 5:
        print('we have more than 2 but less than 6 fruits')
    else:
        print('We have more than 5 fruits')

    # Example 2
    age = 20
    has_id = True

    if age >= 18 and has_id:
        print("Entry allowed")
    else:
        print("Entry denied")

    # Example 3
    is_admin = False
    is_editor = False

    if is_admin or is_editor:
        print("Access granted")
    else:
        print("Access denied")

    # Example 4
    is_logged_in = True

    if not is_logged_in:
        print("Please log in first")
    else:
        print("You are logged in")

    #Example 5
    age = 2
    has_id = True
    is_vip = True

    if (age >= 18 and has_id) or is_vip:
        print("Entry allowed")
    else:
        print("You are not allowed")


test_if_else()
