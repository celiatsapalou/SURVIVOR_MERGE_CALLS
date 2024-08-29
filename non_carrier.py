import pandas as pd

# Load the carrier_non_carrier data with appropriate column names
df_non_carrier = pd.read_csv(
    'carrier_non_carrier.tsv', sep='\t', 
    names=['chrom', 'start', 'end', 'id', 'carrier', 'non_carrier'], 
    header=None
)

# Remove rows where 'start' or 'end' are NA
df_non_carrier.dropna(subset=['start', 'end'], inplace=True)

# Convert 'start' and 'end' to integers now that NA values have been removed
df_non_carrier['start'] = df_non_carrier['start'].astype(int)
df_non_carrier['end'] = df_non_carrier['end'].astype(int)

# Load the high_gq data, assuming it has been loaded into df_high_gq with correct column types
df_high_gq = pd.read_csv('high_gq.tsv', sep='\t')

# Now perform the merge. Make sure the columns you're merging on are of the same type
merged_df = pd.merge(df_high_gq, df_non_carrier[['chrom', 'start', 'end', 'id', 'non_carrier']],
                     on=['chrom', 'start', 'end', 'id'], how='left')

# Save the merged DataFrame
merged_df.to_csv('high_gq_with_non_carriers.tsv', sep='\t', index=False)
