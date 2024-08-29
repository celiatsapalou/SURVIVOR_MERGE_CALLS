import pandas as pd

# Load the data
columns = ['chrom1', 'start1', 'end1', 'id', 'sample1', 'chrom2', 'start2', 'end2', 'ref', 'alt', 'gq', 'sample2', 'overlap']
df = pd.read_csv('filtered_matches.tsv', sep='\t', header=None, names=columns)

# Convert GQ to numeric for comparison
df['gq'] = pd.to_numeric(df['gq'], errors='coerce')

# Filter to keep rows with matching samples
df_matching_samples = df[df['sample1'] == df['sample2']]

# Group by the genomic location only, then get the row with the max GQ for each group
df_max_gq_per_location = df_matching_samples.loc[df_matching_samples.groupby(['chrom1', 'start1', 'end1'])['gq'].idxmax()]

# Keep relevant columns (now including 'sample1' which corresponds to the sample with the highest GQ)
df_final = df_max_gq_per_location[['chrom1', 'start1', 'end1', 'id', 'sample1', 'gq']]

# Save the result
df_final.to_csv('high_gq.tsv', sep='\t', index=False)
