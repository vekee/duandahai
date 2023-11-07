import pandas as pd


df_before = pd.DataFrame(
    [
        ("Tokyo", "101", "2021", "10000"),
        ("Tokyo", "101", "2022", "12000"),
        ("Tokyo", "101", "2023", "11000"),
        ("Osaka", "201", "2021", "9000"),
        ("Osaka", "201", "2022", "8000"),
        ("Osaka", "201", "2023", "9000"),
        ("Nagoya", "301", "2021", "4000"),
        ("Nagoya", "301", "2022", "3000"),
        ("Nagoya", "301", "2023", "3500")
    ],
    columns= ("BranchName", "BranchCode", "year", "profit")
)

df_after = df_before.pivot(
    index=["BranchName", "BranchCode"],
    columns=["year"],
    values="profit"
)
print(df_after.reset_index())
