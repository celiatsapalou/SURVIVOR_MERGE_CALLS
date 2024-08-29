import pandas as pd

# Load the highest GQ per location data
df = pd.read_csv('highest_gq_per_location.tsv', sep='\t')

# Calculate the size of each region
df['size'] = df['end1'] - df['start1']

# Filter to keep only regions < 10kb
df_filtered = df[df['size'] < 10000]

# Save the filtered data
df_filtered.to_csv('regions_10kb.tsv', sep='\t', index=False)
