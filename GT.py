import pandas as pd

# Load the overlaps file
overlaps_df = pd.read_csv('overlaps_80.tsv', sep='\t', header=None)

# Correct indices based on the structure you provided
chrom_col, start_col, end_col, id_col, sample_col_first, chrom_col_second, start_col_second, end_col_second, ref_col, alt_col, gq_col, sample_col_second, overlap_size = range(13)

# Create a 'loc' column to uniquely identify locations from the first file
overlaps_df['loc'] = overlaps_df.apply(lambda row: f"{row[chrom_col]}:{row[start_col]}-{row[end_col]}", axis=1)

# Extract GQ scores and sample names from overlaps
overlaps_df['GQ'] = pd.to_numeric(overlaps_df.iloc[:, gq_col], errors='coerce')
overlaps_df['sample'] = overlaps_df.iloc[:, sample_col_second]

# Find the sample with the highest GQ for each location
highest_gq_samples = overlaps_df.loc[overlaps_df.groupby('loc')['GQ'].idxmax()]

# Load the original TSV file; adjust column names as necessary
# Assuming the original TSV has a similar structure to what's been used in overlaps
original_df = pd.read_csv('reformatted_carrier_non_carrier.tsv', sep='\t', header=None, names=['chrom', 'start', 'end', 'id', 'sample'])

# Create a 'loc' column for matching with overlaps_df
original_df['loc'] = original_df.apply(lambda row: f"{row['chrom']}:{row['start']}-{row['end']}", axis=1)

# Keep rows where the 'loc' and 'sample' matches those in highest_gq_samples
filtered_df = original_df[original_df.apply(lambda row: (row['loc'], row['sample']) in highest_gq_samples[['loc', 'sample']].values, axis=1)]

# Optionally, drop the 'loc' column if no longer needed
filtered_df = filtered_df.drop(columns=['loc'])

# Save the filtered data to a new TSV file
filtered_df.to_csv('high_gq_carrier.tsv', sep='\t', index=False, header=False)
