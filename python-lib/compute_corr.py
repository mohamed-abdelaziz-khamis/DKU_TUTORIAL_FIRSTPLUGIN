def compute_pairs()
    # We'll only compute correlations on numerical columns
    # So extract all pairs of names of numerical columns
    pairs = []
    for i in range(0, len(column_names)):
        for j in range(i + 1, len(column_names)):
            col1 = column_names[i]
            col2 = column_names[j]
            if df[col1].dtype == "float64" and \
               df[col2].dtype == "float64":
                pairs.append((col1, col2))

# Compute the correlation for each pair, and write a
# row in the output array
output = []            
for pair in pairs:
    corr = df[[pair[0], pair[1]]].corr().iloc[0][1]
    if np.abs(corr) > threshold:
      output.append({"col0" : pair[0],
                     "col1" : pair[1],
                     "corr" :  corr})