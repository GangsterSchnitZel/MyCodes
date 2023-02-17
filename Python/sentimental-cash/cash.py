from cs50 import get_float, get_int

# get dollar input from the user
while True:
    try:
        dollars = get_float("Change owed: ")
        if dollars > 0:
            break
    except ValueError:
        print("Type in a positive value")

# calculate quarters (25¢)
quarters = 0
while dollars >= 0.25:
    quarters += 1
    dollars -= 0.25
# calculate dimes (10¢)
dimes = 0
while dollars >= 0.10:
    dimes += 1
    dollars -= 0.10
# calculate nickels (5¢)
nickels = 0
while dollars >= 0.049:
    nickels += 1
    dollars -= 0.05
# calculate pennies (1¢)
pennies = 0
while dollars >= 0.009:
    pennies += 1
    dollars -= 0.01
# print
print(quarters+dimes+nickels+pennies)

