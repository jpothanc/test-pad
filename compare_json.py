import json
import pandas as pd
from typing import Dict, Any

def compare_json_files(file1_path: str, file2_path: str, output_path: str) -> Dict[str, Any]:
    # Read the JSON files
    with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
        json1 = json.load(f1)
        json2 = json.load(f2)
    
    # Convert JSONs to DataFrames for easier comparison
    df1 = pd.json_normalize(json1)
    df2 = pd.json_normalize(json2)
    
    # Find differences between the two dataframes
    # First, ensure both dataframes have the same columns
    columns = list(set(df1.columns) | set(df2.columns))
    
    # Create a dictionary to store different types of changes
    changes = {
        'added': [],
        'removed': [],
        'modified': []
    }
    
    # Convert DataFrames back to dictionaries for comparison
    dict1 = df1.to_dict('records')
    dict2 = df2.to_dict('records')
    
    # Find added and removed entries
    dict1_set = {json.dumps(d, sort_keys=True) for d in dict1}
    dict2_set = {json.dumps(d, sort_keys=True) for d in dict2}
    
    # Added entries (in dict2 but not in dict1)
    for item in dict2_set - dict1_set:
        entry = json.loads(item)
        entry['change_type'] = 'added'
        changes['added'].append(entry)
    
    # Removed entries (in dict1 but not in dict2)
    for item in dict1_set - dict2_set:
        entry = json.loads(item)
        entry['change_type'] = 'removed'
        changes['removed'].append(entry)
    
    # Find modified entries
    for item1 in dict1:
        for item2 in dict2:
            # Remove None values for comparison
            item1_clean = {k: v for k, v in item1.items() if v is not None}
            item2_clean = {k: v for k, v in item2.items() if v is not None}
            
            # Check if items are related but different
            common_keys = set(item1_clean.keys()) & set(item2_clean.keys())
            if common_keys:
                some_matches = any(item1_clean[k] == item2_clean[k] for k in common_keys)
                all_match = all(item1_clean[k] == item2_clean[k] for k in common_keys)
                
                if some_matches and not all_match:
                    old_value = item1_clean.copy()
                    new_value = item2_clean.copy()
                    old_value['change_type'] = 'old_value'
                    new_value['change_type'] = 'new_value'
                    changes['modified'].extend([old_value, new_value])
    
    # Combine all changes
    all_changes = {
        'changes': {
            'added': changes['added'],
            'removed': changes['removed'],
            'modified': changes['modified']
        },
        'summary': {
            'total_changes': len(changes['added']) + len(changes['removed']) + len(changes['modified']),
            'added_count': len(changes['added']),
            'removed_count': len(changes['removed']),
            'modified_count': len(changes['modified']) // 2  # Divide by 2 as we store both old and new values
        }
    }
    
    # Save the differences to a new JSON file
    with open(output_path, 'w') as f:
        json.dump(all_changes, f, indent=4)
    
    return all_changes

# Example usage
if __name__ == "__main__":
    file1_path = "old_file.json"
    file2_path = "new_file.json"
    output_path = "differences.json"
    
    differences = compare_json_files(file1_path, file2_path, output_path)
    print(f"Differences have been saved to {output_path}")