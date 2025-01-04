# a function to check Luhn's algorithm
def sum_check(n):
    p1 = ""
    p2 = 0
    if len(n) % 2 == 0:
        for i in range((len(n) - 1), -1, -1):
            if i % 2 == 0:
                p1 += str(int(n[i]) * 2)
            elif i == 0:
                p1 += str(int(n[i]) * 2)
            else:
                p2 += int(n[i])
    else:
        for i in range((len(n) - 1), -1, -1):
            if i % 2 == 0:
                p2 += int(n[i])
            elif i == 0:
                p2 += int(n[i])
            else:
                p1 += str(int(n[i]) * 2)
    sum1 = 0
    for i in range(len(p1)):
        sum1 += int(p1[i])
    total = sum1 + p2
    Luhn_value = str(total)
    # return the string format of Luhn's value
    return Luhn_value


# a function to check all the conditions for a credit card
def complete_check(n):
    M_DIGIT = 16
    M_START = [51, 52, 53, 54, 55]
    A_DIGIT = 15
    A_START = [34, 37]
    V_DIGIT = [13, 16]
    V_START = 4
    str_total = sum_check(n)

    if len(n) == M_DIGIT and int(n[0] + n[1]) in M_START and str_total[-1] == "0":
        print("MASTERCARD")
    elif len(n) == A_DIGIT and int(n[0] + n[1]) in A_START and str_total[-1] == "0":
        print("AMEX")
    elif len(n) in V_DIGIT and int(n[0]) == V_START and str_total[-1] == "0":
        print("VISA")
    else:
        print("INVALID")


def main():
    card_n = input("Number: ")
    complete_check(card_n)


main()
