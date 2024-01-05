import argparse
import csv

# Read data from CSV file
def read_from_csv(file_path):
  data = []
  with open(file_path, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
      non_leading_space_row = remove_trailing_whitespaces(row)
      case_insensitive_row = make_dict_values_case_insensitive(non_leading_space_row)
      data.append(case_insensitive_row)
  
  return data

# Write data from CSV file
def write_to_csv(data, file_path):
  with open(file_path, mode='w') as csv_file:
    field_names = ['Type', 'Record Identifier', 'Field', 'Source Value', 'Target Value']
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(data)

# compare data and check for mismatches
def compare_data(source, target):
  mismatches = []
  field_discrepancies_count = 0
  source_ids = {record['ID'] for record in source} # fetch source IDs
  target_ids = {record['ID'] for record in target} # fetch target IDs

  missing_in_source = target_ids.difference(source_ids) # fetch ids that are in target but not in source
  missing_in_target = source_ids.difference(target_ids) # fetch ids that are in source but not in target
  similar_ids = source_ids.intersection(target_ids) # fetch similar ids in both source and target

  populate_missing_ids('Missing in Target', missing_in_target, mismatches)
  populate_missing_ids('Missing in Source', missing_in_source, mismatches)

  for similar_id in similar_ids:
    source_v2 = next(row for row in source if row['ID'] == similar_id) # create source dictionary from similar ids
    target_v2 = next(row for row in target if row['ID'] == similar_id) # create target dictionary from similar ids

    # check for any mismatches between the source and target dictionaries
    for key in source_v2.keys():
      if source_v2[key] != target_v2[key]:
        field_discrepancies_count += 1
        mismatches.append({'Type': 'Field Discrepancy', 'Record Identifier': similar_id, 'Field': key, 'Source Value': source_v2[key], 'Target Value': target_v2[key]})

  print('Reconciliation completed:')
  print(f'- Records missing in target: {len(missing_in_target)}')
  print(f'- Records missing in source: {len(missing_in_source)}')
  print(f' -Records with field discrepancies: {field_discrepancies_count}')
  return mismatches

# Remove leading & trailing whitespaces from dictionary values
def remove_trailing_whitespaces(dict):
  return {key: val.strip() for key, val in dict.items()}

# Make dict values lower case
def make_dict_values_case_insensitive(dict):
  return {key: val.lower() for key, val in dict.items()}

# populate missing records from source / target
def populate_missing_ids(field_identifier, diff_set, mismatch_records):
  for missing_id in diff_set:
    mismatch_records.append({'Type': field_identifier, 'Record Identifier': missing_id})

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-s", "--source", required=True, help="path to the source CSV file")
  parser.add_argument("-t", "--target", required=True, help="path to the target CSV file")
  parser.add_argument("-o", "--output", required=True, help="path to save the output reconciliation report")

  args = parser.parse_args()

  source_data = read_from_csv(args.source)
  target_data = read_from_csv(args.target)
  discrepancies = compare_data(source_data, target_data)
  write_to_csv(discrepancies, args.output)
  print('\nReport saved to:', args.output)

