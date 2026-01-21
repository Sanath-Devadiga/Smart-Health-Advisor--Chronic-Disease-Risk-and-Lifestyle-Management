# Smart-Health-Advisor--Chronic-Disease-Risk-and-Lifestyle-Management

🩺 Smart Health Advisor

Smart Health Advisor is a health advisory application that predicts chronic disease risk using machine learning, stores health data securely with AES-256 encryption, and provides personalized health recommendations.

🛠️ Software Requirements

Anaconda 2023.03-1
Python 3.10 (64-bit)
Web Browser (Chrome / Edge / Firefox)
Git (optional)

📦 Project Setup – Step by Step
1️⃣ Install Anaconda

Download and install Anaconda from:
👉 https://www.anaconda.com/products/distribution

After installation, open Anaconda Prompt.

2️⃣ Clone or Download the Project
Option 1: Clone using Git
git clone https://github.com/Sanath-Devadiga/Smart-Health-Advisor--Chronic-Disease-Risk-and-Lifestyle-Management.git

cd smart-health-advisor

Option 2: Download ZIP
Download the project ZIP from GitHub
Extract it
Open the project folder

3️⃣ Create and Activate Conda Environment
conda create -n smarthealth python=3.10
conda activate smarthealth

4️⃣ Install Required Python Packages
pip install -r requirements.txt

If requirements.txt is not present:
pip install flask numpy pandas scikit-learn cryptography

5️⃣ Unzip Machine Learning Model (IMPORTANT STEP)
📁 Go to models Folder
cd models


You will see:
models/
└── model.zip

🔓 Unzip the Model File
▶️ Using Command Line (Recommended)
unzip model.zip


If unzip is not available on Windows, use:

tar -xf model.zip

▶️ Using File Explorer (Alternative)

Open the models folder
Right-click on model.zip
Click Extract Here or Extract All
Make sure the model files are extracted inside the same models folder

✅ Final models Folder Structure
After extraction, it should look like:
models/
├── model.sav
├── madel_rf.sav
└── scaler.sav

6️⃣ Go Back to Project Root Folder
cd ..

7️⃣ Run the Application
python app.py

8️⃣ Open Application in Browser

Open your browser and go to:
http://127.0.0.1:5000/

🔐 Security

Health data is encrypted using AES-256
Machine learning model is loaded securely from the models folder

📁 Project Structure
<pre>
smart-health-advisor/
│
├── app.py
├── README.md
│
├── models/
│   ├── model.zip
│   ├── disease_model.pkl
│   └── scaler.pkl
│
├── encryption/
│   └── encryption.py
│
├── templates/
│   ├── index.html
│   ├── home.html
│   ├── about.html
│   ├── chat.html
│   ├── history.html
│   ├── signin.html
│   ├── signup.html
│   └── notfound.html
│
├── static/
│   ├── css/
│   │   ├── chat.css
│   │   ├── custom.css
│   │   └── styles.css
│   │
│   ├── js/
│   │   └── script.js
│   │
│   ├── favicon_io/
│   │   ├── android-chrome-192x192.png
│   │   ├── android-chrome-512x512.png
│   │   ├── apple-touch-icon.png
│   │   ├── favicon-16x16.png
│   │   ├── favicon-32x32.png
│   │   ├── favicon.ico
│   │   └── site.webmanifest
│   │
│   ├── download.png
│   ├── download (1).png
│   ├── download (2).png
│   ├── download (3).png
│   ├── download (4).png
│   ├── download (5).png
│   ├── download (6).png
│   ├── download (7).png
│   ├── download (8).png
│   └── download (9).png
│
├── database/
│   └──signup.db
│
├── Notebook.ipynb
├── Notebook.html
│
├── .gitignore
└── .gitattributes
</pre>

⚠️ Important Notes

Do not delete model.zip before extraction
App will not run if model files are missing
Always activate the conda environment before running the app

👨‍💻 Author
Sanath
Smart Health Advisor – Academic Project
