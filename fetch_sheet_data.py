# fetch_sheet_data.py
import gspread
import pandas as pd
import os
import json

def main():
    creds_json_str = os.environ.get('GOOGLE_SHEETS_API_CREDENTIALS')
    spreadsheet_id = os.environ.get('GOOGLE_SHEET_ID')
    sheet_name = os.environ.get('GOOGLE_SHEET_NAME', 'Sheet1') 
    output_csv_path = os.environ.get('OUTPUT_CSV_PATH', 'data/your_data.csv') 

    if not creds_json_str:
        print("Error: GOOGLE_SHEETS_API_CREDENTIALS secret not set.")
        exit(1)
    if not spreadsheet_id:
        print("Error: GOOGLE_SHEET_ID environment variable not set.")
        exit(1)

    try:
        
        creds_dict = json.loads(creds_json_str)
        gc = gspread.service_account_from_dict(creds_dict)

       
        print(f"Attempting to open spreadsheet with ID: {spreadsheet_id}")
        spreadsheet = gc.open_by_key(spreadsheet_id) # 使用 Spreadsheet ID 打开
        
        print(f"Attempting to open worksheet: {sheet_name}")
        worksheet = spreadsheet.worksheet(sheet_name)

      
        print("Fetching all records from the worksheet...")
        data = worksheet.get_all_records() # 获取所有数据为字典列表

        if not data:
            print(f"No data found in sheet '{sheet_name}'. Creating an empty CSV.")
            df = pd.DataFrame()
        else:
            df = pd.DataFrame(data)
            print(f"Successfully fetched {len(df)} rows.")

        
        output_dir = os.path.dirname(output_csv_path)
        if output_dir: # 如果路径包含目录
            os.makedirs(output_dir, exist_ok=True)
        
        df.to_csv(output_csv_path, index=False, encoding='utf-8-sig') # utf-8-sig 通常对中文更好
        print(f"Successfully saved sheet '{sheet_name}' to '{output_csv_path}'")

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Error: Spreadsheet with ID '{spreadsheet_id}' not found. "
              "Please check the ID and ensure the service account has access.")
        exit(1)
    except gspread.exceptions.WorksheetNotFound:
        print(f"Error: Worksheet with name '{sheet_name}' not found in the spreadsheet.")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
