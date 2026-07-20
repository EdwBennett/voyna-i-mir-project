# demo_ty.py

def greet_user(name: str) -> str:
    """Returns a personalized greeting message."""
    return f"Hello, {name}!"


def calculate_total(price: float, quantity: int) -> float:
    """Calculates the total cost based on price and quantity."""
    return price * quantity


# --- TEST CASES (Ty will verify these types) ---

# 1. Correct Usage: Ty passes these cleanly
user_greeting = greet_user("Alice")
total_cost = calculate_total(19.99, 3)
print(user_greeting)
print(f"Total: ${total_cost:.2f}")


# 2. Type Errors: Uncomment these lines to see Ty catch errors in VS Code
bad_greeting = greet_user(123)          # Ty Error: Argument 1 expects 'str', got 'int'
bad_total = calculate_total("19.99", 3) # Ty Error: Argument 1 expects 'float', got 'str'
