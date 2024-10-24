from economy import get_player_money, set_player_money



# Define loan types
loans = {
    "small_loan": {"amount": 1000, "interest_rate": 0.05, "duration": 10},
    "medium_loan": {"amount": 5000, "interest_rate": 0.03, "duration": 20},
    "large_loan": {"amount": 10000, "interest_rate": 0.02, "duration": 30}
}



# Variables to track the active loan
current_loan = {
    "amount": 0,             # Principal loan amount
    "interest_rate": 0,       # Interest rate applied to the loan
    "remaining_cycles": 0,    # Number of repayment cycles remaining
    "total_loan_balance": 0   # Total remaining loan balance (principal + interest)
}



# Function to take a loan
def take_loan(loan_type):
    if current_loan["amount"] == 0:  # Only allow one active loan at a time
        loan = loans[loan_type]
        loan_amount = loan["amount"]
        interest_rate = loan["interest_rate"]
        duration = loan["duration"]

        # Add loan amount to player money
        set_player_money(get_player_money() + loan_amount)

        # Set loan repayment details
        current_loan["amount"] = loan_amount
        current_loan["interest_rate"] = interest_rate
        current_loan["remaining_cycles"] = duration
        # Total balance = principal + total interest over all cycles
        current_loan["total_loan_balance"] = loan_amount * (1 + interest_rate * duration)

    else:
        print("Loan already active. Repay existing loan before taking a new one.")



# Function to repay the loan each cycle
def repay_loan():
    if current_loan["amount"] > 0 and current_loan["remaining_cycles"] > 0:
        # Calculate payment per cycle based on total loan balance
        payment_per_cycle = current_loan["total_loan_balance"] / current_loan["remaining_cycles"]

        # Deduct loan payment from player money
        current_money = get_player_money()
        set_player_money(current_money - payment_per_cycle)

        # Update loan status
        current_loan["remaining_cycles"] -= 1
        current_loan["total_loan_balance"] -= payment_per_cycle

        if current_loan["remaining_cycles"] == 0:
            # Loan fully repaid, reset loan data
            print("Loan fully repaid!")
            reset_loan()
    else:
        print("No active loan or loan already fully repaid.")



# Function to reset the loan after it's fully repaid
def reset_loan():
    current_loan["amount"] = 0
    current_loan["interest_rate"] = 0
    current_loan["remaining_cycles"] = 0
    current_loan["total_loan_balance"] = 0



# Function to check if the player has an active loan
def has_active_loan():
    return current_loan["amount"] > 0



# Function to display loan status
def get_loan_status():
    if current_loan["amount"] > 0:
        return f"Loan: ${int(current_loan['total_loan_balance'])}, Interest: {current_loan['interest_rate']}%, Payments Left: {current_loan['remaining_cycles']}"
    return "No active loan."