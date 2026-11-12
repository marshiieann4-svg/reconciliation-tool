import pandas as pd

# Load data
bank = pd.read_csv("bank_statement.csv")
invoices = pd.read_csv("invoices.csv")

# Clean amount to number
bank["Amount"] = bank["Amount"].astype(float)
invoices["Amount"] = invoices["Amount"].astype(float)

matched = []
unmatched_bank = []
duplicate_payments = []

# Check for duplicates in bank statement
seen_refs = {}
for _, row in bank.iterrows():
    ref = row["Reference"]
    if ref in seen_refs:
        duplicate_payments.append(row)
    else:
        seen_refs[ref] = True

# Match bank to invoices
for _, b in bank.iterrows():
    match = invoices[(invoices["Reference"] == b["Reference"]) & (invoices["Amount"] == b["Amount"])]
    if not match.empty:
        matched.append(b)
    else:
        # Check for partial payment
        partial = invoices[invoices["Reference"] == b["Reference"]]
        if not partial.empty:
            print(f"PARTIAL: {b['Reference']} - Paid R{b['Amount']} of R{partial.iloc[0]['Amount']}")
        else:
            unmatched_bank.append(b)

print(f"\nMatched: {len(matched)}")
print(f"Unmatched bank transactions: {len(unmatched_bank)}")
print(f"Duplicate payments: {len(duplicate_payments)}")

# Unpaid invoices
matched_refs = [m["Reference"] for m in matched]
unpaid = invoices[~invoices["Reference"].isin(matched_refs)]
print(f"Unpaid invoices: {len(unpaid)}")
print(unpaid)