import csv

def read_csv(file_path):
  data = []
  with open(file_path, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
      data.append(row)
  
  return data

source_data = read_csv('source.csv')
target_data = read_csv('target.csv')

