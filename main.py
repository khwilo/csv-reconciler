import csv

def read_csv(file_path):
  data = []
  with open(file_path, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
      non_leading_space_row = {key: val.strip() for key, val in row.items()}
      case_insensitive_row = {key: val.lower() for key, val in non_leading_space_row.items()}
      data.append(case_insensitive_row)
  
  return data

def compare_data(source, target):
  mismatches = []
  source_ids = {record['ID'] for record in source}
  target_ids = {record['ID'] for record in target}

  missing_in_source = target_ids.difference(source_ids)
  missing_in_target = source_ids.difference(target_ids)
  similar_ids = source_ids.intersection(target_ids)

  for missing_id in missing_in_target:
    mismatches.append({'Type': 'Missing in Target', 'Record Identifier': missing_id})

  for missing_id in missing_in_source:
    mismatches.append({'Type': 'Missing in Source', 'Record Identifier': missing_id})

  for similar_id in similar_ids:
    source_v2 = {}
    target_v2 = {}

    for row in source:
      if row['ID'] == similar_id:
        source_v2 = row

    for row in target:
      if row['ID'] == similar_id:
        target_v2 = row

    for key in source_v2.keys():
      if source_v2[key] != target_v2[key]:
        mismatches.append({'Type': 'Field Discrepancy', 'Record Identifier': similar_id, 'Field': key, 'Source Value': source_v2[key], 'Target Value': target_v2[key]})

  return mismatches

source_data = read_csv('source.csv')
target_data = read_csv('target.csv')

discrepancies = compare_data(source_data, target_data)
