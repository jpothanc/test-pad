import csv
from collections import defaultdict

def compare_csv_files(file1_path, file2_path, output_path, primary_col=None):
    try:
        # Get base filenames without path
        file1_name = file1_path.split('/')[-1]
        file2_name = file2_path.split('/')[-1]
        
        # Read both CSV files into dictionaries
        file1_data = {}
        file2_data = {}
        file1_headers = []
        file2_headers = []
        
        # Read first file
        with open(file1_path, 'r') as f1:
            reader = csv.DictReader(f1)
            file1_headers = reader.fieldnames
            primary_col = primary_col if primary_col else file1_headers[0]
            
            if primary_col not in file1_headers:
                raise ValueError(f"Primary column '{primary_col}' not found in {file1_name}")
            
            for row in reader:
                if row[primary_col] and row[primary_col].strip():  # Skip empty primary keys
                    file1_data[row[primary_col]] = row
        
        # Read second file
        with open(file2_path, 'r') as f2:
            reader = csv.DictReader(f2)
            file2_headers = reader.fieldnames
            
            if primary_col not in file2_headers:
                raise ValueError(f"Primary column '{primary_col}' not found in {file2_name}")
            
            for row in reader:
                if row[primary_col] and row[primary_col].strip():  # Skip empty primary keys
                    file2_data[row[primary_col]] = row
        
        # Combine all headers for output
        all_headers = list(set(file1_headers + file2_headers + ['change_type', 'source_file']))
        
        # Track changes
        changes = []
        
        # Find added rows (in file2 but not in file1)
        for key in file2_data:
            if key not in file1_data:
                row = file2_data[key].copy()
                row['change_type'] = f'new_in_{file2_name}'
                row['source_file'] = file2_name
                changes.append(row)
        
        # Find removed rows (in file1 but not in file2)
        for key in file1_data:
            if key not in file2_data:
                row = file1_data[key].copy()
                row['change_type'] = f'only_in_{file1_name}'
                row['source_file'] = file1_name
                changes.append(row)
        
        # Find modified rows
        for key in set(file1_data.keys()) & set(file2_data.keys()):
            if file1_data[key] != file2_data[key]:
                # Add old version
                row1 = file1_data[key].copy()
                row1['change_type'] = f'removed_from_{file1_name}'
                row1['source_file'] = file1_name
                changes.append(row1)
                
                # Add new version
                row2 = file2_data[key].copy()
                row2['change_type'] = f'added_to_{file2_name}'
                row2['source_file'] = file2_name
                changes.append(row2)
        
        # Write changes to output file if there are any
        if changes:
            with open(output_path, 'w', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=all_headers)
                writer.writeheader()
                writer.writerows(changes)
            print(f"Found {len(changes)} changes. Results written to {output_path}")
            return changes
        else:
            print("No differences found between the files")
            return []
            
    except Exception as e:
        print(f"Error processing CSV files: {str(e)}")
        return []

# Example usage
if __name__ == "__main__":
    file1_path = "old_file.csv"
    file2_path = "new_file.csv"
    output_path = "differences.csv"
    primary_col = "ID"  # Replace with your primary column name
    
    differences = compare_csv_files(file1_path, file2_path, output_path, primary_col)