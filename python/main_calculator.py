from calculator_operations import add, subtract, multiply, divide


def main():
    valid_operators = {"+", "-", "/", "*"}

    print(
        "Please provide an operand with an operator and finally an operand to calculate\n"
        f"Valid operators are {[x for x in valid_operators]}"
    )

    while True:
        user_input = input("What do you want to calculate?\n>").strip()

        if len(user_input.split()) != 3:
            print("Not a valid expression")
            continue

        left, operator, right = user_input.split()

        if not left.isdigit() and not right.isdigit():
            print(f"Expression {user_input} has incorrect operands.")
            continue

        if operator not in valid_operators:
            print(f"The operator {operator} is invalid.")
            continue

        if "+" in user_input:
            print(
                f"The answer for the expression {user_input} is {add(int(left), int(right))}"
            )
        if "-" in user_input:
            print(
                f"The answer for the expression {user_input} is {subtract(int(left), int(right))}"
            )
        if "*" in user_input:
            print(
                f"The answer for the expression {user_input} is {multiply(int(left), int(right))}"
            )
        if "/" in user_input:
            print(
                f"The answer for the expression {user_input} is {divide(int(left), int(right))}"
            )

        go_again = input("Do you want to calculate again?(y , n)\n>").strip().lower()

        if go_again in {"y", "n"}:
            if go_again == "y":
                continue
            else:
                break
        else:
            print("invalid input")
            continue


if __name__ == "__main__":
    main()
