BEGIN { FS="\t"; OFS="\t" }

{
    # Initialize arrays for carriers and non-carriers
    delete carriers
    delete non_carriers

    # Loop over the sample fields starting from the 8th field
    for (i = 8; i <= NF; i++) {
        # Split the field into sample and genotype
        split($i, arr, "=")
        sample = arr[1]
        genotype = arr[2]

        # Determine if the sample is a carrier or a non-carrier
        if (genotype != "0/0") {
            carriers[sample] = genotype
        } else {
            non_carriers[sample] = genotype
        }
    }

    # Print the inversion information
    print $1, $2, $3, $4

    # Print carriers and non-carriers
    print "Carriers:"
    for (sample in carriers) {
        print sample, carriers[sample]
    }
    
    print "Non-Carriers:"
    for (sample in non_carriers) {
        print sample, non_carriers[sample]
    }
    
    print "---------------------------------"
}