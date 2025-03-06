import os
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import moviepy.editor as mp
import re

# Authenticate Google Drive & Sheets
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

# Open Google Sheet
SHEET_NAME = "AI Agents and Agentic AI in Python" 
sheet = client.open(SHEET_NAME).sheet1  

# Google Drive API Setup
drive_service = build("drive", "v3", credentials=creds)

# List of Module Folder IDs (Update for different courses)
MODULE_FOLDERS = {
    "Module 1": "1F7e8shZLHg4q-eNWyJggHgx2VLhrHGqa",
    "Module 2": "1Ob7pudnTr4Tbkc0trsbdEk9KmvpM75Uy",
    "Module 3": "1_W73JGk81AIcvogdOz7zXnUN4-mAlvku",
    "Module 5": "1QEYdlJvQg21Bq9Z81xyQV0omIHcqosZS"
}

print("🚀 Starting Video URL & Duration Extraction...")

# Get column headers
header_row = sheet.row_values(1)
video_url_col = header_row.index("Video URL") + 1
length_col = header_row.index("Length") + 1

# Get all rows for matching
all_rows = sheet.get_all_values()

for module_name, folder_id in MODULE_FOLDERS.items():
    print(f"📂 Processing: {module_name} (Folder ID: {folder_id})")

    # Get video files sorted correctly
    query = f"'{folder_id}' in parents and mimeType contains 'video'"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    files = sorted(results.get("files", []), key=lambda x: x["name"])  # Sort alphabetically

    print(f"🔍 Found {len(files)} videos in {module_name}")
    if not files:
        print("⚠️ No videos found in this module. Skipping...")
        continue

    for file in files:
        file_id = file["id"]
        file_name = file["name"]
        file_url = f"https://drive.google.com/file/d/{file_id}/view"

        # Find the corresponding row in Column A (Name)
        # Preprocess file name
        file_name_no_ext = re.sub(r"^\d+\.\s*", "", file_name.split(".mp4")[0]).strip().lower()

        # Find best match in sheet
        row_idx = next(
            (i+1 for i, row in enumerate(all_rows) if any(file_name_no_ext in cell.lower().strip() for cell in row)), 
            None
)

        if row_idx:
            # Check if the Video URL and Length columns already have values
            existing_url = sheet.cell(row_idx, video_url_col).value
            existing_duration = sheet.cell(row_idx, length_col).value

            if existing_url and existing_url.strip() and existing_duration and existing_duration.strip():
                print(f"⏭️ Skipping {file_name}, already has URL & duration.")
                continue  # Skip this video
        else:
            print(f"⚠️ No matching row found for {file_name}, skipping...")
            continue

        print(f"🎥 Processing Video: {file_name} (ID: {file_id})")

        # Download video temporarily
        try:
            request = drive_service.files().get_media(fileId=file_id)
            file_path = f"./{file_name}"
            with open(file_path, "wb") as f:
                f.write(request.execute())
            print(f"✅ Downloaded: {file_name}")

            # Extract duration
            video = mp.VideoFileClip(file_path)
            duration = video.duration  # Duration in seconds
            hours = int(duration // 3600)
            minutes = int((duration % 3600) // 60)
            seconds = int(duration % 60)
            duration_str = f"{hours}:{minutes:02}:{seconds:02}"  # Google Sheets format

            print(f"⏳ Extracted Duration: {duration_str}")

            # Delete downloaded file
            os.remove(file_path)
            print(f"🗑️ Deleted Temporary File: {file_name}")

        except Exception as e:
            duration_str = "Error Reading Video"
            print(f"❌ Failed to process {file_name}: {e}")

        # Update Google Sheets
        print(f"📊 Updating Google Sheet: Row {row_idx}, Column {video_url_col} (URL) → {file_url}")
        print(f"📊 Updating Google Sheet: Row {row_idx}, Column {length_col} (Length) → {duration_str}")

        sheet.update_cell(row_idx, video_url_col, file_url)  # Insert Video URL
        sheet.format(f"{chr(64 + length_col)}{row_idx}", {"numberFormat": {"type": "TEXT"}})  # Prevent auto-formatting
        sheet.update_cell(row_idx, length_col, duration_str)  # Insert video duration

        print(f"✅ Successfully updated sheet for {file_name}")

print("🎉 Done! All videos processed.")
