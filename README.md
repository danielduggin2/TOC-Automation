# 🎥 Google Sheets Video Duration & URL Automation

## 📌 What This Project Does

This script **automates the extraction of video durations** from Google Drive and updates a **Google Sheets spreadsheet** with:

- ✅ **Accurate video durations** extracted automatically.
- ✅ **Corresponding video URLs** populated based on partial name matching.
- ✅ **Only missing data** updated (previously processed entries are skipped).
- ✅ **Formatted timestamps** written to Google Sheets in `H:MM:SS` format.

---

## 🛠️ How the Code Works

1. **Connects to Google Drive & Sheets** using Google Cloud API credentials.
2. **Lists video files** inside specific course/module folders in Google Drive.
3. **Matches video names with sheet entries** (ignoring numbers & ".mp4").
4. **Downloads each video temporarily** and extracts its duration using `MoviePy`.
5. **Updates the corresponding row** in Google Sheets with:
   - 📌 **Video URL** (column `B`)
   - ⏳ **Duration** (column `C`)
6. ✅ **Skips already processed videos** to prevent duplicate updates.

---

## 🔗 How to Integrate with Google Cloud Services

This project requires **Google Drive API** and **Google Sheets API**.

### **1️⃣ Enable APIs in Google Cloud**

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Click **Create a Project** (or select an existing project).
3. Enable the following APIs:
   - **Google Drive API**
   - **Google Sheets API**
4. Click **Create Credentials** → Select **Service Account**.

### **2️⃣ Get API Credentials**

1. In Google Cloud, go to **IAM & Admin > Service Accounts**.
2. Create a new service account and **download the JSON key file**.
3. Rename it to `credentials.json` and place it in the project folder.

### **3️⃣ Share Google Sheets with the Service Account**

1. Open your **Google Sheets file**.
2. Click **Share** and add the email from your **Google Cloud service account**.
3. Set permissions to **Editor**.

### **4️⃣ Share Google Drive Folders with the Service Account**

1. Open the Google Drive **course folder** containing video files.
2. Click **Share** and add the service account email.
3. Set permissions to **Viewer** (so it can read video files).

---

## 🚀 How to Run the Script

### **1️⃣ Clone the Repository**

```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/GoogleSheets-Video-Duration-Automation.git
cd GoogleSheets-Video-Duration-Automation

```
