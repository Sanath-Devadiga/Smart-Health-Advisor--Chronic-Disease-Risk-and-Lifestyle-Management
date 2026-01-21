# Smart-Health-Advisor--Chronic-Disease-Risk-and-Lifestyle-Management

🩺 Smart Health Advisor

Smart Health Advisor is a health-focused application that helps users assess chronic disease risk, store health records securely using AES-256 encryption, and receive personalized health and lifestyle recommendations with the help of an AI-based assistant.

🚀 Features

User health data management

Chronic disease risk assessment

Personalized diet & lifestyle suggestions

Secure health record storage using AES-256 encryption

AI chatbot for health guidance

Separate flow for healthy users and chronic disease patients

🛠️ Technologies Used

Python 3.10 (Anaconda)

Machine Learning (Risk Prediction)

AES-256 Encryption

Flask (Backend)

HTML, CSS, JavaScript (Frontend)

SQLite / MongoDB (Database – based on configuration)

📦 Software Requirements

Before installing the project, make sure you have:

Anaconda 2023.03-1

Python 3.10 (64-bit)

Web Browser (Chrome / Edge / Firefox)

Git (optional, for cloning repository)

⚙️ Installation Steps
1️⃣ Install Anaconda

Download and install Anaconda from the official website:
👉 https://www.anaconda.com/products/distribution

During installation, allow Anaconda to add Python to PATH (recommended).

2️⃣ Clone the Repository
git clone https://github.com/your-username/smart-health-advisor.git
cd smart-health-advisor


(Or download the ZIP file and extract it manually)

3️⃣ Create a Conda Environment (Recommended)
conda create -n smarthealth python=3.10
conda activate smarthealth

4️⃣ Install Required Libraries
pip install -r requirements.txt


If requirements.txt is not available, install manually:

pip install flask numpy pandas scikit-learn cryptography

5️⃣ Run the Application
python app.py

6️⃣ Open in Browser

After running the app, open your browser and go to:

http://127.0.0.1:5000/

🔐 Security

Health data is encrypted using AES-256

Secure handling of sensitive medical information

Encryption keys are managed internally

📁 Project Structure (Example)
smart-health-advisor/
│
├── app.py
├── requirements.txt
├── encryption/
├── ml_models/
├── templates/
├── static/
├── database/
└── README.md

📌 Future Enhancements

Cloud deployment

Mobile application support

Advanced AI health recommendations

Doctor–patient interaction module

👨‍💻 Author

sd
Smart Health Advisor – Academic Project

If you want, I can also:

Create a requirements.txt

Make a short README for viva

Add screenshots section

Write installation steps in exam style (10 marks)

inside models folder ther e is a model.zip that has to unzip give me a step by step readme file'

Below is a step-by-step README.md updated specifically to explain how to unzip model.zip inside the models folder.
Written in simple words, suitable for GitHub + academic submission.

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
smart-health-advisor/
│
├── app.py
├── models/
│   ├── model.zip
│   ├── disease_model.pkl
│   └── scaler.pkl
├── encryption/
├── templates/
├── static/
├── database/
└── README.md

⚠️ Important Notes

Do not delete model.zip before extraction
App will not run if model files are missing
Always activate the conda environment before running the app

👨‍💻 Author
Sanath
Smart Health Advisor – Academic Project
