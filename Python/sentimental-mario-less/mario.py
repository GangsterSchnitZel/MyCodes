# Control if the input is in range

while True:
    try:
        n = int(input("Type in a Number between 1 and 8: "))
        if n > 0 and n < 9:
            break

    except ValueError:
        print("Type in a Number between 1 and 8: ")
# loop through lines
for i in range(n):
    for j in range(n-i-1):
        print("", end=" ")
    for k in range(i+1):
        print("#", end="")
    print()