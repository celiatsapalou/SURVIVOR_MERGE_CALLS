import pandas as pd

# Load the TSV file
carrier_df = pd.read_csv('carrier_non_carrier.tsv', sep='\t', header=None,
                         names=['chrom', 'start', 'end', 'inv_id', 'carrier_sample', 'non_carrier_sample'])

# Load the CSV file
gq_df = pd.read_csv('output_all_GT.csv')

# Create an empty DataFrame for the results
results = []

# Iterate over each row in the carrier DataFrame
for index, carrier_row in carrier_df.iterrows():
    # Filter the GQ DataFrame for overlapping intervals
    overlap_gq = gq_df[(gq_df['CHROM'] == carrier_row['chrom']) & 
                       (gq_df['POS'] <= carrier_row['end']) & 
                       (gq_df['POS'] >= carrier_row['start'])]

    # Proceed if there are overlaps
    if not overlap_gq.empty:
        # Find the sample in the overlap with the highest GQ value
        overlap_gq['GQ'] = pd.to_numeric(overlap_gq['GQ'], errors='coerce')  # Ensure GQ is numeric
        max_gq_row = overlap_gq.loc[overlap_gq['GQ'].idxmax()]

        # Check if the carrier_sample or non_carrier_sample matches the sample with the highest GQ
        if carrier_row['carrier_sample'] == max_gq_row['SAMPLE'] or carrier_row['non_carrier_sample'] == max_gq_row['SAMPLE']:
            results.append(carrier_row)

# Convert the list of matching rows to a DataFrame
results_df = pd.DataFrame(results, columns=carrier_df.columns)

# Save to a new TSV file
results_df.to_csv('filtered_overlaps.tsv', sep='\t', index=False)

print(f"Filtered overlaps saved to 'filtered_overlaps.tsv'. Total rows: {len(results_df)}")
