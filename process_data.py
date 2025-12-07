import pandas as pd
from pathlib import Path

def main():
    # Folder containing the CSV files
    data_dir = Path("data")

    # List your CSV files here
    files = [
        "daily_sales_data_0.csv",
        "daily_sales_data_1.csv",
        "daily_sales_data_2.csv",
    ]

    all_dfs = []

    for file_name in files:
        file_path = data_dir / file_name
        print(f"Processing {file_path}...")

        df = pd.read_csv(file_path)

        # 1. Keep only Pink Morsels
        # Check exact wording in your CSV if needed (e.g. 'pink morsel' / 'Pink Morsel')
        df = df[df["product"] == "pink morsel"]

        # 2. Create 'sales' = quantity * price
        df["sales"] = df["quantity"] * df["price"]

        # 3. Keep only the required columns: Sales, Date, Region
        # Rename to match exact requirement formatting
        df_formatted = df[["sales", "date", "region"]].rename(
            columns={
                "sales": "Sales",
                "date": "Date",
                "region": "Region",
            }
        )

        all_dfs.append(df_formatted)

    # 4. Combine all three files into one DataFrame
    final_df = pd.concat(all_dfs, ignore_index=True)

    # 5. Save formatted output file
    output_path = data_dir / "pink_morsel_sales.csv"
    final_df.to_csv(output_path, index=False)
    print(f"Saved processed data to {output_path}")

if __name__ == "__main__":
    main()
