import glob 
import pandas as pd 
import xml.etree.ElementTree as ET 
from datetime import datetime 

# Define file paths
log_file = "log_file.txt"
target_file = "transformed_data.csv"

# Function to extract data from CSV files
def extract_from_csv(file_to_process):
    dataframe = pd.read_csv(file_to_process)
    return dataframe

# Function to extract data from JSON files
def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process, lines=True)
    return dataframe

# Function to extract data from XML files
def extract_from_xml(file_to_process):
    dataframe = pd.DataFrame(columns=['car_model', 'year_of_manufacture', 'price', 'fuel'])
    tree = ET.parse(file_to_process)
    root = tree.getroot()
    for car in root:
        model = car.find("car_model").text
        year = int(car.find("year_of_manufacture").text)
        price = float(car.find("price").text)
        fuel = car.find("fuel").text
        # Append extracted data to dataframe
        dataframe = pd.concat([dataframe, pd.DataFrame([{"car_model": model, "year_of_manufacture": year, "price": price, "fuel": fuel}])], ignore_index=True)
    return dataframe

# Function to extract data from all CSV, JSON, and XML files in the directory
def extract():
    extracted_data = pd.DataFrame(columns=['car_model', 'year_of_manufacture', 'price', 'fuel'])
    
    # Process all CSV files
    for csvfile in glob.glob("*.csv"):
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_csv(csvfile))], ignore_index=True)
    
    # Process all JSON files
    for jsonfile in glob.glob("*.json"):
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_json(jsonfile))], ignore_index=True)
    
    # Process all XML files
    for xmlfile in glob.glob("*.xml"):
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_xml(xmlfile))], ignore_index=True)
    
    return extracted_data

# Function to transform the extracted data
def transform(data):
    data['price'] = round(data.price, 2)  # Round the 'price' column to 2 decimal places
    return data

# Function to load transformed data into a CSV file
def load_data(target_file, transformed_data):
    transformed_data.to_csv(target_file)

# Function to log progress with a timestamp
def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'  # Year-Monthname-Day-Hour-Minute-Second
    now = datetime.now()  # Get current timestamp
    timestamp = now.strftime(timestamp_format)
    with open(log_file, "a") as f:
        f.write(timestamp + ',' + message + '\n')

# Log the initialization of the ETL process
log_progress("ETL Job Started")

# Log the beginning of the Extraction process
log_progress("Extract phase Started")
extracted_data = extract()

# Log the completion of the Extraction process
log_progress("Extract phase Ended")

# Log the beginning of the Transformation process
log_progress("Transform phase Started")
transformed_data = transform(extracted_data)
print("Transformed Data")
print(transformed_data)

# Log the completion of the Transformation process
log_progress("Transform phase Ended")

# Log the beginning of the Loading process
log_progress("Load phase Started")
load_data(target_file, transformed_data)

# Log the completion of the Loading process
log_progress("Load phase Ended")

# Log the completion of the ETL process
log_progress("ETL Job Ended")
