class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def is_operator(ch):
    return ch in "+-*/"


def precedence(op):
    if op in "+-":
        return 1
    if op in "*/":
        return 2
    return 0


# Convert infix expression to postfix
def infix_to_postfix(expression):
    result = []
    stack = []

    for ch in expression:
        if ch.isdigit():
            result.append(ch)

        elif ch == '(':
            stack.append(ch)

        elif ch == ')':
            while stack and stack[-1] != '(':
                result.append(stack.pop())
            stack.pop()

        elif is_operator(ch):
            while (stack and stack[-1] != '(' and
                   precedence(stack[-1]) >= precedence(ch)):
                result.append(stack.pop())
            stack.append(ch)

    while stack:
        result.append(stack.pop())

    return result


# Construct Expression Tree
def construct_tree(postfix):
    stack = []

    for ch in postfix:
        if ch.isdigit():
            stack.append(Node(ch))

        elif is_operator(ch):
            right = stack.pop()
            left = stack.pop()

            node = Node(ch)
            node.left = left
            node.right = right

            stack.append(node)

    return stack[-1]


# Recursive evaluation
def evaluate(root):
    if root is None:
        return 0

    # Leaf node
    if root.left is None and root.right is None:
        return int(root.value)

    left_value = evaluate(root.left)
    right_value = evaluate(root.right)

    if root.value == '+':
        return left_value + right_value
    elif root.value == '-':
        return left_value - right_value
    elif root.value == '*':
        return left_value * right_value
    elif root.value == '/':
        return left_value / right_value


# Traversals
def inorder(root):
    if root:
        inorder(root.left)
        print(root.value, end=" ")
        inorder(root.right)


def preorder(root):
    if root:
        print(root.value, end=" ")
        preorder(root.left)
        preorder(root.right)


def postorder(root):
    if root:
        postorder(root.left)
        postorder(root.right)
        print(root.value, end=" ")


# Main program
expression = input("Enter arithmetic expression: ")

postfix = infix_to_postfix(expression)
root = construct_tree(postfix)

print("\nExpression Tree Traversals:")
print("Inorder   :", end=" ")
inorder(root)

print("\nPreorder  :", end=" ")
preorder(root)

print("\nPostorder :", end=" ")
postorder(root)

print("\n\nResult =", evaluate(root))