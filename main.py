import re


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def tokenize(expression):
    pattern = r"\s*(\d+(?:\.\d+)?|[()+\-*/])"
    tokens = []
    position = 0

    while position < len(expression):
        match = re.match(pattern, expression[position:])

        if not match:
            raise ValueError("Invalid expression!")

        tokens.append(match.group(1))
        position += match.end()

    if not tokens:
        raise ValueError("Expression cannot be empty!")

    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def eat(self):
        token = self.current()
        self.position += 1
        return token

    def parse(self):
        root = self.expression()

        if self.current() is not None:
            raise ValueError("Invalid expression!")

        return root

    def expression(self):
        node = self.term()

        while self.current() in ("+", "-"):
            operator = self.eat()
            right = self.term()
            node = Node(operator, node, right)

        return node

    def term(self):
        node = self.factor()

        while self.current() in ("*", "/"):
            operator = self.eat()
            right = self.factor()
            node = Node(operator, node, right)

        return node

    def factor(self):
        token = self.current()

        if token == "+":
            self.eat()
            return self.factor()

        if token == "-":
            self.eat()
            return Node("-", Node("0"), self.factor())

        if token == "(":
            self.eat()
            node = self.expression()

            if self.current() != ")":
                raise ValueError("Missing closing bracket!")

            self.eat()
            return node

        if token is not None and re.fullmatch(
            r"\d+(?:\.\d+)?", token
        ):
            self.eat()
            return Node(token)

        raise ValueError("Expected a number!")


def build_tree(expression):
    tokens = tokenize(expression)
    parser = Parser(tokens)
    return parser.parse()


def evaluate(root):
    if root.left is None and root.right is None:
        return float(root.value)

    left = evaluate(root.left)
    right = evaluate(root.right)

    if root.value == "+":
        return left + right
    elif root.value == "-":
        return left - right
    elif root.value == "*":
        return left * right
    elif root.value == "/":
        if right == 0:
            raise ZeroDivisionError("Cannot divide by zero!")
        return left / right


def display_tree(root, level=0):
    if root is not None:
        display_tree(root.right, level + 1)
        print("    " * level + str(root.value))
        display_tree(root.left, level + 1)


def main():
    print("EXPRESSION TREE GENERATOR AND EVALUATOR")
    expression = input("Enter expression: ")

    try:
        root = build_tree(expression)
        result = evaluate(root)

        print("\nExpression Tree:")
        display_tree(root)

        if result.is_integer():
            result = int(result)

        print("\nResult:", result)

    except (ValueError, ZeroDivisionError) as error:
        print("Error:", error)


if __name__ == "__main__":
    main()