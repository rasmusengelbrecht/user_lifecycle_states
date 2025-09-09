"""Generate synthetic user and transaction data and load into DuckDB."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import duckdb
import os

def generate_data():
    """Generate synthetic users and transactions data."""
    
    # Set random seed for reproducibility
    random.seed(42)
    np.random.seed(42)

    # Parameters
    n_users = 1000
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 12, 31)
    months = pd.date_range(start=start_date, end=end_date, freq='MS')

    # Generate users
    user_ids = [f"user_{i}" for i in range(1, n_users + 1)]
    user_created_dates = np.random.choice(pd.date_range(start=start_date, end=end_date, freq='D'), size=n_users)

    users = pd.DataFrame({
        "user_id": user_ids,
        "created_at": user_created_dates
    })

    # Define behavior probabilities for generating transactions
    behaviors = ["never_activated", "retained", "churned", "sporadic", "resurrected"]
    probabilities = [0.1, 0.4, 0.2, 0.2, 0.1]

    user_behaviors = np.random.choice(behaviors, size=n_users, p=probabilities)

    # Generate transactions based on behavior
    transactions = []
    transaction_id_counter = 1

    for i, row in users.iterrows():
        user_id = row["user_id"]
        signup_date = row["created_at"]
        behavior = user_behaviors[i]
        
        eligible_months = [m for m in months if m >= signup_date.replace(day=1)]
        
        if behavior == "never_activated":
            continue
        
        elif behavior == "retained":
            for m in eligible_months:
                tx_date = m + timedelta(days=np.random.randint(0, 28))
                # Ensure transaction date is after signup date
                if tx_date >= signup_date:
                    transactions.append((f"tx_{transaction_id_counter}", user_id, tx_date))
                    transaction_id_counter += 1
        
        elif behavior == "churned":
            churn_month = np.random.choice(eligible_months) if eligible_months else None
            if churn_month:
                for m in eligible_months:
                    if m <= churn_month:
                        tx_date = m + timedelta(days=np.random.randint(0, 28))
                        # Ensure transaction date is after signup date
                        if tx_date >= signup_date:
                            transactions.append((f"tx_{transaction_id_counter}", user_id, tx_date))
                            transaction_id_counter += 1
        
        elif behavior == "sporadic":
            for m in eligible_months:
                if np.random.rand() < 0.5:
                    tx_date = m + timedelta(days=np.random.randint(0, 28))
                    # Ensure transaction date is after signup date
                    if tx_date >= signup_date:
                        transactions.append((f"tx_{transaction_id_counter}", user_id, tx_date))
                        transaction_id_counter += 1
        
        elif behavior == "resurrected":
            if len(eligible_months) > 4:
                active1 = eligible_months[:2]
                dormant = eligible_months[2:5]
                active2 = eligible_months[5:]
                for m in active1 + active2:
                    tx_date = m + timedelta(days=np.random.randint(0, 28))
                    # Ensure transaction date is after signup date
                    if tx_date >= signup_date:
                        transactions.append((f"tx_{transaction_id_counter}", user_id, tx_date))
                        transaction_id_counter += 1

    # Create transaction DataFrame
    transactions_df = pd.DataFrame(transactions, columns=["transaction_id", "user_id", "created_at"])
    
    return users, transactions_df


def load_to_duckdb(users_df, transactions_df, db_path="data.duckdb"):
    """Load dataframes into DuckDB database."""
    
    print("🔄 Loading data into DuckDB...")
    
    # Connect to DuckDB
    conn = duckdb.connect(db_path)
    
    # Create raw schema
    conn.execute("CREATE SCHEMA IF NOT EXISTS raw_data")
    
    # Drop tables if they exist
    conn.execute("DROP TABLE IF EXISTS raw_data.users")
    conn.execute("DROP TABLE IF EXISTS raw_data.transactions")
    
    # Create and populate users table
    conn.execute("""
        CREATE TABLE raw_data.users AS 
        SELECT * FROM users_df
    """)
    
    # Create and populate transactions table
    conn.execute("""
        CREATE TABLE raw_data.transactions AS 
        SELECT * FROM transactions_df
    """)
    
    # Show summary
    user_count = conn.execute("SELECT COUNT(*) FROM raw_data.users").fetchone()[0]
    transaction_count = conn.execute("SELECT COUNT(*) FROM raw_data.transactions").fetchone()[0]
    
    print(f"✅ Loaded {user_count:,} users and {transaction_count:,} transactions")
    
    conn.close()


def run_data_generation():
    """Main function to generate and load data."""
    
    print("🚀 Starting data generation...")
    
    # Generate data
    users_df, transactions_df = generate_data()
    
    # Ensure database directory exists
    os.makedirs("../dbt_project", exist_ok=True)
    db_path = "../dbt_project/data.duckdb"
    
    # Load to DuckDB
    load_to_duckdb(users_df, transactions_df, db_path)
    
    print("✅ Data generation completed successfully!")


if __name__ == "__main__":
    run_data_generation()