import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# TASK 2: EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================

# ------------------------------------------------------------
# 1. LOAD THE DATASET
# ------------------------------------------------------------

file_path = "outputs/quotes_dataset.csv"

if not os.path.exists(file_path):
    raise FileNotFoundError(
        f"Dataset file '{file_path}' not found. "
        "Please run 'python web_scraper.py' first to generate the dataset."
    )

df = pd.read_csv(file_path)

print("=" * 60)
print("TASK 2: EXPLORATORY DATA ANALYSIS")
print("=" * 60)


# ------------------------------------------------------------
# 2. ASK MEANINGFUL QUESTIONS
# ------------------------------------------------------------

print("\nEDA QUESTIONS")
print("-" * 60)

print("1. How many quotes are present in the dataset?")
print("2. How many different authors are present?")
print("3. Which authors have the most quotes?")
print("4. Which tags are most common?")
print("5. Are there any missing values?")
print("6. Are there any duplicate records?")
print("7. What is the average length of a quote?")
print("8. Are there any unusual or extreme quote lengths?")


# ------------------------------------------------------------
# 3. EXPLORE THE DATA STRUCTURE
# ------------------------------------------------------------

print("\n\nDATASET STRUCTURE")
print("-" * 60)

print("\nFirst 5 rows:")
print(df.head())

print("\nNumber of rows and columns:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)


# ------------------------------------------------------------
# 4. CHECK MISSING VALUES
# ------------------------------------------------------------

print("\n\nMISSING VALUES")
print("-" * 60)

missing_values = df.isnull().sum()

print(missing_values)


# ------------------------------------------------------------
# 5. CHECK DUPLICATE VALUES
# ------------------------------------------------------------

print("\n\nDUPLICATE ROWS")
print("-" * 60)

duplicate_count = df.duplicated().sum()

print("Number of duplicate rows:", duplicate_count)


# ------------------------------------------------------------
# 6. BASIC DATASET INFORMATION
# ------------------------------------------------------------

print("\n\nDATASET INFORMATION")
print("-" * 60)

print("Total number of quotes:", len(df))

print("Number of unique authors:", df["author"].nunique())


# ------------------------------------------------------------
# 7. AUTHOR ANALYSIS
# ------------------------------------------------------------

print("\n\nAUTHOR ANALYSIS")
print("-" * 60)

author_counts = df["author"].value_counts()

print("\nQuotes by author:")
print(author_counts)

print("\nTop 10 authors:")
print(author_counts.head(10))


# ------------------------------------------------------------
# 8. TAG ANALYSIS
# ------------------------------------------------------------

print("\n\nTAG ANALYSIS")
print("-" * 60)

all_tags = []

for tags in df["tags"].dropna():

    tag_list = str(tags).split(",")

    for tag in tag_list:
        cleaned_tag = tag.strip()
        if cleaned_tag:
            all_tags.append(cleaned_tag)


tag_counts = pd.Series(all_tags).value_counts()

print("\nTop 10 most common tags:")
print(tag_counts.head(10))


# ------------------------------------------------------------
# 9. QUOTE LENGTH ANALYSIS
# ------------------------------------------------------------

print("\n\nQUOTE LENGTH ANALYSIS")
print("-" * 60)

# Calculate the length of each quote
df["quote_length"] = df["quote"].astype(str).str.len()

print("\nAverage quote length:")
print(df["quote_length"].mean())

print("\nShortest quote length:")
print(df["quote_length"].min())

print("\nLongest quote length:")
print(df["quote_length"].max())

print("\nQuote length statistics:")
print(df["quote_length"].describe())


# ------------------------------------------------------------
# 10. FIND SHORTEST QUOTE
# ------------------------------------------------------------

shortest_index = df["quote_length"].idxmin()

print("\n\nSHORTEST QUOTE")
print("-" * 60)

print(df.loc[shortest_index, "quote"])


# ------------------------------------------------------------
# 11. FIND LONGEST QUOTE
# ------------------------------------------------------------

longest_index = df["quote_length"].idxmax()

print("\n\nLONGEST QUOTE")
print("-" * 60)

print(df.loc[longest_index, "quote"])


# ------------------------------------------------------------
# 12. STATISTICAL SUMMARY
# ------------------------------------------------------------

print("\n\nSTATISTICAL SUMMARY")
print("-" * 60)

print(df["quote_length"].describe())


# ============================================================
# VISUALIZATION
# ============================================================

os.makedirs("outputs", exist_ok=True)

# ------------------------------------------------------------
# 13. BAR CHART - TOP AUTHORS
# ------------------------------------------------------------

top_authors = author_counts.head(10)

plt.figure(figsize=(10, 6))

top_authors.plot(kind="bar")

plt.title("Top 10 Authors by Number of Quotes")

plt.xlabel("Author")

plt.ylabel("Number of Quotes")

plt.xticks(rotation=45, ha="right")

plt.tight_layout()

plt.savefig("outputs/top_authors.png")
plt.show(block=False)
plt.close()


# ------------------------------------------------------------
# 14. BAR CHART - TOP TAGS
# ------------------------------------------------------------

top_tags = tag_counts.head(10)

plt.figure(figsize=(10, 6))

top_tags.plot(kind="bar")

plt.title("Top 10 Most Common Tags")

plt.xlabel("Tag")

plt.ylabel("Number of Quotes")

plt.xticks(rotation=45, ha="right")

plt.tight_layout()

plt.savefig("outputs/top_tags.png")
plt.show(block=False)
plt.close()


# ------------------------------------------------------------
# 15. HISTOGRAM - QUOTE LENGTH
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

sns.histplot(
    df["quote_length"],
    bins=20,
    kde=True
)

plt.title("Distribution of Quote Length")

plt.xlabel("Quote Length")

plt.ylabel("Number of Quotes")

plt.tight_layout()

plt.savefig("outputs/quote_length_distribution.png")
plt.show(block=False)
plt.close()


# ------------------------------------------------------------
# 16. DATA QUALITY SUMMARY
# ------------------------------------------------------------

print("\n\nDATA QUALITY SUMMARY")
print("-" * 60)

total_missing = df.isnull().sum().sum()

total_duplicates = df.duplicated().sum()

print("Total missing values:", total_missing)

print("Total duplicate rows:", total_duplicates)


# ------------------------------------------------------------
# 17. FINAL CONCLUSION
# ------------------------------------------------------------

print("\n\nFINAL EDA CONCLUSION")
print("=" * 60)

print("1. The dataset was successfully loaded and explored.")

print("2. The structure, columns, and data types were examined.")

print("3. The number of quotes and unique authors was identified.")

print("4. The authors with the highest number of quotes were analyzed.")

print("5. The most common tags were identified.")

print("6. Missing values and duplicate records were checked.")

print("7. Quote length was analyzed using statistical measures.")

print("8. Visualizations were created to identify patterns and trends.")

print("9. The analysis helps identify potential data quality issues.")

print("10. The results can be used for further data analysis.")


print("\n" + "=" * 60)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 60)
