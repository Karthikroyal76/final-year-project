import os
import glob
import pandas as pd
import pdfplumber
import re

# Directory containing the PDF files - update this to your PDF directory
pdf_directory = "/Users/kalyan/project/farmer_consumer_marketplace/assets/pdfs"
output_directory = "/Users/kalyan/project/farmer_consumer_marketplace/assets/data"

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Get all PDF files in the directory
pdf_files = glob.glob(os.path.join(pdf_directory, "download*.pdf"))

# Expected column names
expected_columns = [
    "State Name", "District Name", "Market Name", "Commodity", "Variety",
    "Arrivals (Tonnes)", "Min Price (Rs./Quintal)", "Max Price (Rs./Quintal)", 
    "Modal Price (Rs./Quintal)", "Reported Date"
]

# All extracted data will be stored here
all_data = []

for pdf_file in pdf_files:
    print(f"Processing {pdf_file}...")
    
    try:
        # Open the PDF file
        with pdfplumber.open(pdf_file) as pdf:
            # Extract data from each page
            for i, page in enumerate(pdf.pages):
                print(f"  Processing page {i+1}/{len(pdf.pages)}")
                
                # Extract text from the page
                text = page.extract_text()
                
                # Extract tables from the page
                tables = page.extract_tables()
                
                # Process each table on the page
                for table in tables:
                    # Skip header rows and empty rows
                    for row in table:
                        # Clean the row data and filter out empty rows
                        row_data = [str(cell).strip() if cell is not None else "" for cell in row]
                        
                        # Skip empty or header rows
                        if len(row_data) < 5 or all(cell == "" for cell in row_data):
                            continue
                            
                        # Verify this looks like a data row by checking for numeric values
                        # Assuming price columns have numeric values
                        has_numbers = any(re.search(r'\d+', cell) for cell in row_data)
                        if not has_numbers:
                            continue
                            
                        # Pad the row if it's shorter than expected
                        while len(row_data) < len(expected_columns):
                            row_data.append("")
                            
                        # Trim the row if it's longer than expected
                        if len(row_data) > len(expected_columns):
                            row_data = row_data[:len(expected_columns)]
                            
                        all_data.append(row_data)
                        
    except Exception as e:
        print(f"  Error processing {pdf_file}: {e}")

# Create DataFrame
if all_data:
    df = pd.DataFrame(all_data, columns=expected_columns)
    
    # Clean up the data
    # Convert price columns to numeric
    price_columns = [
        "Min Price (Rs./Quintal)", 
        "Max Price (Rs./Quintal)", 
        "Modal Price (Rs./Quintal)"
    ]
    
    for col in price_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].str.replace(r'[^\d.]', '', regex=True), errors='coerce')
    
    # Convert arrivals to numeric
    if "Arrivals (Tonnes)" in df.columns:
        df["Arrivals (Tonnes)"] = pd.to_numeric(df["Arrivals (Tonnes)"].str.replace(r'[^\d.]', '', regex=True), errors='coerce')
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Save to Excel
    output_file = os.path.join(output_directory, "Agmarknet_Price_Data.xlsx")
    df.to_excel(output_file, index=False)
    
    print(f"\nSuccess! Combined data saved to {output_file}")
    print(f"Total rows: {len(df)}")
else:
    print("\nNo data was processed.")