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

source_data = read_csv('source.csv')
target_data = read_csv('target.csv')
