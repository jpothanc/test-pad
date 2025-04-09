import pandas as pd

def compare_csv_files(file1_path, file2_path, output_path):
    # Read the CSV files
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)
    
    # Find differences between the two dataframes
    # First, ensure both dataframes have the same columns
    columns = list(set(df1.columns) | set(df2.columns))
    
    # Create a dictionary to store different types of changes
    changes = {
        'added': df2[~df2.index.isin(df1.index)],
        'removed': df1[~df1.index.isin(df2.index)],
        'modified': pd.DataFrame()
    }
    
    # Find modified rows (rows that exist in both but have different values)
    common_indices = df1.index.intersection(df2.index)
    changes['modified'] = pd.DataFrame()
    
    for idx in common_indices:
        if not df1.loc[idx].equals(df2.loc[idx]):
            # Find which columns changed
            changed_columns = []
            changes_details = {}
            
            for col in columns:
                if col in df1.columns and col in df2.columns:
                    if df1.loc[idx, col] != df2.loc[idx, col]:
                        changed_columns.append(col)
                        changes_details[f'{col}_old'] = df1.loc[idx, col]
                        changes_details[f'{col}_new'] = df2.loc[idx, col]
            
            # Create a row with change details
            change_row = pd.DataFrame([changes_details], index=[idx])
            change_row['changed_columns'] = ', '.join(changed_columns)
            change_row['change_type'] = 'modified'
            changes['modified'] = pd.concat([changes['modified'], change_row])
    
    # Add change_type column to added and removed dataframes
    changes['added']['change_type'] = 'added'
    changes['removed']['change_type'] = 'removed'
    
    # Combine all changes into one dataframe
    all_changes = pd.concat([
        changes['added'],
        changes['removed'],
        changes['modified']
    ])
    
    # Sort the results by index and change_type
    all_changes = all_changes.sort_values(['change_type', all_changes.index.name or 'index'])
    
    # Save the differences to a new CSV file
    all_changes.to_csv(output_path)
    
    return all_changes

# Example usage
if __name__ == "__main__":
    file1_path = "old_file.csv"
    file2_path = "new_file.csv"
    output_path = "differences.csv"
    
    differences = compare_csv_files(file1_path, file2_path, output_path)
    print(f"Differences have been saved to {output_path}")