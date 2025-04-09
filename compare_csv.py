import pandas as pd

def compare_csv_files(file1_path, file2_path, output_path, primary_col=None):
    # Read the CSV files
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)
    
    # Set the primary column as index if provided, otherwise use the first column
    if primary_col:
        if primary_col not in df1.columns or primary_col not in df2.columns:
            raise ValueError(f"Primary column '{primary_col}' not found in both CSV files")
        df1 = df1.set_index(primary_col)
        df2 = df2.set_index(primary_col)
    else:
        df1 = df1.set_index(df1.columns[0])
        df2 = df2.set_index(df2.columns[0])
    
    # Remove rows with null values in the index
    df1 = df1[df1.index.notnull()]
    df2 = df2[df2.index.notnull()]
    
    # Find differences between the two dataframes
    # First, ensure both dataframes have the same columns (excluding the index)
    columns = list(set(df1.columns) | set(df2.columns))
    
    # Create a dictionary to store different types of changes
    changes = {
        'added': df2[~df2.index.isin(df1.index)],
        'removed': df1[~df1.index.isin(df2.index)],
        'modified': pd.DataFrame()
    }
    
    # Find modified rows (rows that exist in both but have different values)
    common_indices = df1.index.intersection(df2.index)
    for idx in common_indices:
        if not df1.loc[idx].equals(df2.loc[idx]):
            row1 = df1.loc[idx].to_frame().T
            row2 = df2.loc[idx].to_frame().T
            row1['change_type'] = 'old_value'
            row2['change_type'] = 'new_value'
            changes['modified'] = pd.concat([changes['modified'], row1, row2])
    
    # Add change_type column to added and removed dataframes
    changes['added']['change_type'] = 'added'
    changes['removed']['change_type'] = 'removed'
    
    # Combine all changes into one dataframe
    all_changes = pd.concat([
        changes['added'],
        changes['removed'],
        changes['modified']
    ])
    
    # Sort the results by index
    all_changes = all_changes.sort_index()
    
    # Save the differences to a new CSV file
    all_changes.to_csv(output_path)
    
    return all_changes

# Example usage
if __name__ == "__main__":
    file1_path = "old_file.csv"
    file2_path = "new_file.csv"
    output_path = "differences.csv"
    primary_col = "ID"  # Replace with your primary column name
    
    differences = compare_csv_files(file1_path, file2_path, output_path, primary_col)
    print(f"Differences have been saved to {output_path}")