# create a function for pyramid
def pyramid(n):
    for i in range(1, n + 1):
        # create a variable to use for the symmetry of the pyramid
        j = n - i
        print((j * " ") + (i * "#"), end="")
        print("  ", end="")
        print(i * "#")


def main():
    while True:
        try:
            # get the input and convert it to int
            h = int(input("Height: "))
            if 9 > h > 0:
                pyramid(h)
                return
            else:
                print("You need to enter a positive integer")
        except ValueError:
            print("You need to enter a number")


main()
