import pandas as pd

def compare_csv_files(file1_path, file2_path, output_path, primary_col=None):
    try:
        # Read the CSV files
        df1 = pd.read_csv(file1_path)
        df2 = pd.read_csv(file2_path)
        
        # Check if dataframes are empty
        if df1.empty or df2.empty:
            print("Warning: One or both CSV files are empty")
            return pd.DataFrame()
        
        # Set the primary column as index if provided, otherwise use the first column
        if primary_col:
            if primary_col not in df1.columns or primary_col not in df2.columns:
                raise ValueError(f"Primary column '{primary_col}' not found in both CSV files")
            df1 = df1.set_index(primary_col)
            df2 = df2.set_index(primary_col)
        else:
            df1 = df1.set_index(df1.columns[0])
            df2 = df2.set_index(df2.columns[0])
        
        # Remove rows with null values in the index and any invalid data
        df1 = df1[df1.index.notnull()]
        df2 = df2[df2.index.notnull()]
        
        # Find differences between the two dataframes
        columns = list(set(df1.columns) | set(df2.columns))
        
        # Initialize empty DataFrames for changes
        changes = {
            'added': pd.DataFrame(),
            'removed': pd.DataFrame(),
            'modified': pd.DataFrame()
        }
        
        try:
            # Find added and removed rows
            changes['added'] = df2[~df2.index.isin(df1.index)]
            changes['removed'] = df1[~df1.index.isin(df2.index)]
            
            # Find modified rows safely
            common_indices = df1.index.intersection(df2.index)
            for idx in common_indices:
                try:
                    if not df1.loc[idx].equals(df2.loc[idx]):
                        row1 = df1.loc[idx].to_frame().T
                        row2 = df2.loc[idx].to_frame().T
                        row1['change_type'] = 'old_value'
                        row2['change_type'] = 'new_value'
                        changes['modified'] = pd.concat([changes['modified'], row1, row2])
                except (AttributeError, TypeError) as e:
                    print(f"Warning: Skipping comparison for index {idx} due to invalid data")
                    continue
            
            # Add change_type column safely
            if not changes['added'].empty:
                changes['added']['change_type'] = 'added'
            if not changes['removed'].empty:
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
            if not all_changes.empty:
                all_changes.to_csv(output_path)
                return all_changes
            else:
                print("No differences found between the files")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"Error during comparison: {str(e)}")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"Error processing CSV files: {str(e)}")
        return pd.DataFrame()

# Example usage
if __name__ == "__main__":
    file1_path = "old_file.csv"
    file2_path = "new_file.csv"
    output_path = "differences.csv"
    primary_col = "ID"  # Replace with your primary column name
    
    differences = compare_csv_files(file1_path, file2_path, output_path, primary_col)
    print(f"Differences have been saved to {output_path}")