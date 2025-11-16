from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import joblib
import numpy as np
import os, random
import json
from datetime import timedelta, datetime
import re
import sqlite3
from encryption import encrypt_prediction_data, decrypt_prediction_data

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-me-please")

# -------- Load model & scaler (place your files under Models/) --------
MODEL_PATH = "Models/model.sav"
SCALER_PATH = "Models/scaler.sav"

def safe_load(path):
    try:
        return joblib.load(path)
    except Exception as e:
        print(f"[WARN] Could not load {path}: {e}")
        return None

model = safe_load(MODEL_PATH)
scaler = safe_load(SCALER_PATH)

# -------- feature order (must match training) --------
FEATURES = [
    'Age','Gender','Height_cm','Weight_kg','BMI',
    'Blood_Pressure_Systolic','Blood_Pressure_Diastolic',
    'Cholesterol_Level','Blood_Sugar_Level','Genetic_Risk_Factor',
    'Allergies','Daily_Steps','Exercise_Frequency','Sleep_Hours',
    'Alcohol_Consumption','Smoking_Habit','Dietary_Habits',
    'Caloric_Intake','Protein_Intake','Carbohydrate_Intake','Fat_Intake'
]

LABELS = ['Diabetes','Heart Disease','Hypertension','Obesity', 'None']

# -------- Database initialization --------
def init_prediction_history_db():
    # Initialize the database for prediction history
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            encrypted_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    con.commit()
    con.close()

# Initialize database on startup
init_prediction_history_db()

def map_label(raw):
    try:
        if isinstance(raw, (int, np.integer)):
            return LABELS[int(raw)]
        if isinstance(raw, str):
            if raw in LABELS:
                return raw
            if raw.isdigit() and int(raw) < len(LABELS):
                return LABELS[int(raw)]
    except Exception:
        pass
    return str(raw)

# -------- Extensive guidance knowledge base (60 tips per disease: 20 diet, 20 habits, 20 prevention) --------
GUIDANCE = {
    "None": {
        "diet": [
            "Half your plate vegetables at lunch and dinner.",
            "Rotate whole grains: oats, brown rice, millets, quinoa.",
            "Add a source of protein to every meal (eggs, legumes, fish, lean meat).",
            "Drink water instead of sugar-sweetened beverages.",
            "Snack on fruit, yogurt, or a handful of nuts.",
            "Cook with measured amounts of healthy oil (olive/mustard) — avoid free-pouring.",
            "Try a new vegetable every week to increase variety.",
            "Prefer whole fruit to fruit juice to preserve fiber.",
            "Batch-cook legumes and whole grains for quick healthy meals.",
            "Start meals with a salad or vegetable soup to reduce overeating.",
            "Season with herbs and spices instead of extra salt.",
            "Choose minimally processed items most of the time.",
            "Keep desserts small and infrequent.",
            "Aim for 25–30 g fiber daily from plant sources.",
            "Include probiotic foods like curd/yogurt occasionally.",
            "Have 2–3 alcohol-free days per week.",
            "Limit packaged snacks and read labels for hidden sugar/salt.",
            "Finish dinner 2–3 hours before sleep.",
            "Use smaller plates to naturally reduce portions.",
            "Plan balanced weekly menus to avoid impulsive takeout."
        ],
        "habits": [
            "Aim for 150–300 minutes of moderate activity weekly.",
            "Include 2–3 sessions of strength training per week.",
            "Stand up and move for 2–5 minutes every hour of sitting.",
            "Take a 10–15 minute walk after main meals.",
            "Keep a consistent sleep schedule: 7–9 hours nightly.",
            "Practice 5 minutes of deep breathing daily to lower stress.",
            "Hydrate throughout the day—keep a bottle visible as a reminder.",
            "Take stairs instead of lifts where safe.",
            "Schedule and keep preventive health checkups annually.",
            "Track steps/sleep for two weeks to learn your baseline.",
            "Create a wind-down pre-sleep routine: dim lights, no screens 30–60 min before bed.",
            "Plan active social time: walking dates, sport with friends.",
            "Do 5–10 minutes of mobility/stretching every morning.",
            "Stand during phone calls or pacing meetings.",
            "Meal-prep on a chosen day to reduce weekday decision fatigue.",
            "Celebrate small wins to build habit momentum.",
            "Keep comfortable walking shoes handy to nudge movement.",
            "Pair TV time with standing or light exercises.",
            "Set hydration and posture reminders during the workday.",
            "Adopt a short after-dinner tidy walk: 10 minutes every evening."
        ],
        "prevention": [
            "Maintain healthy BMI and protect muscle mass with resistance work.",
            "Monitor BP, fasting glucose, and lipids as advised by provider.",
            "Stay current with age-appropriate screenings (cancer, eye, etc.).",
            "Use sunscreen and sun-protective habits outdoors.",
            "Get recommended vaccinations (influenza, etc.).",
            "Foster social support and regular social activities.",
            "Practice daily micro-stress relief (breathing, short meditations).",
            "Avoid tobacco and limit alcohol consumption.",
            "Guard sleep hygiene—treat snoring or disrupted sleep if present.",
            "Have a basic first-aid and medication checklist when traveling.",
            "Reassess lifestyle goals every quarter to maintain progress.",
            "Keep a standing desk or sit-stand routine if possible.",
            "Organize emergency contacts and medication lists.",
            "Reduce excessive noise exposure and protect hearing.",
            "Keep good oral hygiene—gum health influences systemic inflammation.",
            "Plan grocery lists focused on whole foods rather than impulse buys.",
            "Stay alert to work-related stress and take recovery days.",
            "Ensure hydration strategies during hot weather or intense activity.",
            "Use sensory relaxation before bed: calm music, reading.",
            "Build an environment that makes healthy choices easy (visible water, prepared veggies)."
        ]
    },

    "Diabetes": {
        "diet": [
            "Prefer low-GI carbohydrates: oats, barley, millets, quinoa, brown rice.",
            "Make non-starchy vegetables half your plate (greens, cruciferous veg).",
            "Include a healthy protein source with every meal (eggs, dal, fish, tofu).",
            "Avoid sugar-sweetened beverages—choose water or unsweetened tea.",
            "Break large meals into smaller, regular meals to reduce post-meal spikes.",
            "Use vinegar or lemon-based dressings to blunt carbohydrate response.",
            "Favor boiling/steaming/grilling over deep-frying.",
            "Carry a protein/fiber snack (roasted chana, nuts, yogurt) to avoid high-sugar snacks.",
            "Prefer whole fruit over smoothies or fruit juices to keep fiber intact.",
            "Limit refined grains and sweets—reserve them for special occasions only.",
            "Aim for 25–35 g fiber/day via pulses, vegetables, fruits, and whole grains.",
            "Swap white rice for brown rice or millet mixes where possible.",
            "Choose portion-controlled measures for rice and bread (use the plate rule).",
            "Include healthy fats (olive oil, nuts, avocado) in moderate amounts.",
            "Limit alcohol intake; monitor its effect on blood sugar.",
            "Prefer low-fat dairy options or plain yogurt instead of flavored versions.",
            "Add non-starchy vegetable-based starters like salad or soup to meals.",
            "Use herbs/spices like cinnamon, fenugreek (methi) as adjuncts after checking tolerance.",
            "Avoid dried fruits as everyday snacks—they concentrate sugar.",
            "Read labels to spot hidden sugars (maltodextrin, dextrose, syrups)."
        ],
        "habits": [
            "Take a 10–20 minute walk after main meals to lower post-meal glucose.",
            "Accumulate 150–300 minutes/week of aerobic activity (walking/cycling/swimming).",
            "Add 2–3 resistance sessions/week to increase muscle glucose uptake.",
            "Maintain consistent sleep (7–9 hours); poor sleep raises glucose.",
            "Use a glucometer per clinician advice—track fasting and post-meal levels.",
            "Perform a daily foot check: inspect for cuts, blisters, or infections.",
            "Carry a small hypo-kit (glucose tablets, small snack) if on insulin or sulfonylureas.",
            "Keep a simple log of food, activity, and glucose to find patterns.",
            "Coordinate medication/insulin timing with meals as instructed by clinician.",
            "Set reminders for medication and glucose checks on busy days.",
            "Stay hydrated—dehydration can increase blood sugar readings.",
            "Break long sitting times each hour with 2–5 minutes of movement.",
            "Plan ahead for holidays—choose smaller dessert portions and extra activity.",
            "Discuss supplement options with healthcare provider before use.",
            "Schedule retinal (eye) checks yearly if diabetic for early detection.",
            "Get kidney function tests as advised to detect changes early.",
            "Wear well-fitting shoes to reduce risk of foot injury.",
            "Use mindful eating techniques to reduce overeating and binge episodes.",
            "Discuss CGM (continuous glucose monitoring) with your clinician if available.",
            "Have a documented sick-day plan for medication and food intake adjustments."
        ],
        "prevention": [
            "Aim for modest weight loss (5–10% of body weight) if overweight—big impact on risk.",
            "Protect lean mass with protein and regular resistance training.",
            "Quit smoking to reduce vascular and metabolic risks.",
            "Keep blood pressure and lipids in target ranges to reduce complications.",
            "Get HbA1c checked every 3–6 months as advised.",
            "Keep annual eye exams and foot exams scheduled and attended.",
            "Get vaccinated (influenza, pneumococcal) to lower complication risks.",
            "Create a family/friend hypoglycemia action plan if on insulin.",
            "Address sleep apnea (snoring, daytime sleepiness) to improve metabolic control.",
            "Have an emergency medical ID if on insulin or with severe hypoglycemia risk.",
            "Plan structured follow-ups with diabetes educator and dietitian.",
            "Practice stress-reduction techniques consistently to blunt stress-induced glucose rises.",
            "Ensure dental checks—periodontal disease is linked with poorer glycemic control.",
            "Review medications annually with clinician to optimize regimens.",
            "Carry a simple carbohydrate source during exercise or long activities.",
            "Read package labels and be able to count carbs for portion planning.",
            "Consider structured behavior programs for weight and glucose control.",
            "Work on sleep hygiene—poor sleep affects appetite hormones and glucose.",
            "Educate household members on hypo/hyperglycemia recognition and care.",
            "Keep realistic, measurable goals and celebrate adherence milestones."
        ]
    },

    "Heart Disease": {
        "diet": [
            "Use heart-healthy oils (olive, canola, mustard) in measured amounts.",
            "Limit saturated fats (butter, ghee, full-fat dairy) and replace with lean proteins.",
            "Avoid trans fats: packaged baked goods and repeated deep-frying.",
            "Eat oily fish (salmon, mackerel) 1–2 times weekly or plant omega-3 sources (flax, chia).",
            "Choose whole grains (oats, brown rice, millet) over refined grains.",
            "Increase intake of vegetables and berries for antioxidants and fiber.",
            "Limit salt intake and flavor with herbs, spices, garlic, and citrus.",
            "Prefer home-cooked meals to better control sodium and fat.",
            "Snack on unsalted nuts in moderation (almonds, walnuts).",
            "Limit sugar-sweetened beverages and refined sweets.",
            "Choose lean cuts of meat and remove visible fat before cooking.",
            "Replace creamy sauces with tomato- or yogurt-based versions.",
            "Include legumes regularly as a protein and fiber source.",
            "Choose low-fat dairy or fortified plant alternatives where appropriate.",
            "Limit processed meats (bacon, sausages) that are high in sodium & nitrates.",
            "Reduce refined carbohydrate loads—balance carbs with protein & fiber.",
            "Add garlic and turmeric for flavor and potential anti-inflammatory benefits.",
            "Use portion control—measure oils and servings rather than free-hand serving.",
            "Limit fried and fast-food frequency to special occasional meals.",
            "Read labels for sodium and trans fat — choose lowest options."
        ],
        "habits": [
            "Accumulate 150–300 minutes/week of moderate-intensity aerobic activity.",
            "Include 2–3 resistance training sessions weekly for muscle strength.",
            "Break long sitting periods every 30–60 minutes for short activity.",
            "Stop smoking and avoid exposure to secondhand smoke.",
            "Monitor blood pressure and cholesterol at intervals recommended by your clinician.",
            "Limit alcohol; follow clinician guidance on safe levels.",
            "Practice daily stress-management (breathing, meditation, short walks).",
            "Aim for 7–9 hours of quality sleep to support heart health.",
            "Use a pillbox, alarms, or apps to improve medication adherence.",
            "Walk after meals to support blood pressure and glucose responses.",
            "Engage in social activities to reduce loneliness—beneficial for cardiac outcomes.",
            "Plan active leisure (hikes, biking, dancing) rather than sedentary pastimes.",
            "Build a home first-aid/medication list and share with family members.",
            "Practice mindful eating to avoid overeating and large post-prandial loads.",
            "Avoid intense exertion if you have known coronary disease without clinician clearance.",
            "Keep weight in a healthy range via diet and activity.",
            "Prioritize dental care—gum disease is associated with higher cardiovascular risk.",
            "Use heart-rate or step goals to help maintain regular activity.",
            "Limit caffeine intake if it causes palpitations or anxiety.",
            "Schedule periodic cardiac reviews with your clinician if risk factors exist."
        ],
        "prevention": [
            "Aim for LDL and HDL targets as advised by your clinician—diet + meds as needed.",
            "Keep blood pressure under recommended thresholds for your risk profile.",
            "Manage diabetes tightly—good glucose control reduces vascular damage.",
            "Maintain waist circumference and BMI targets to reduce metabolic burden.",
            "Know the symptoms of heart attack & have an action plan (call emergency services).",
            "Stay current with vaccinations to avoid cardiac complications from infections.",
            "Use stress-management tools during high-pressure seasons (work/deadlines).",
            "Avoid prolonged exposure to heavy air pollution for outdoor exercise—choose low-pollution times.",
            "Have an action plan for angina or unusual chest discomfort and emergency contacts.",
            "Encourage family screening if there is a strong family history of heart disease.",
            "Take cardiac medications exactly as prescribed and track refills.",
            "Work with a dietitian for structured heart-healthy meal planning when needed.",
            "Address sleep disorders—untreated sleep apnea increases cardiac risk.",
            "Ensure thyroid function is checked if cholesterol remains high despite therapy.",
            "Understand safe exercise progressions—avoid abrupt increases.",
            "Carry relevant medical ID if you have implantable devices or important medications.",
            "Check alcohol intake and reduce if it elevates blood pressure or interacts with meds.",
            "Be cautious with supplements—discuss with clinician to avoid interactions.",
            "Build a long-term plan for medication optimization and lifestyle maintenance.",
            "Plan holiday and travel strategies for diet/activity to prevent lapses."
        ]
    },

    "Hypertension": {
        "diet": [
            "Adopt DASH-style plates: vegetables, fruits, whole grains, low-fat dairy, legumes.",
            "Reduce sodium intake — target 1.5–2.3 g/day depending on clinician advice.",
            "Avoid high-sodium packaged foods (soups, sauces, instant noodles).",
            "Rinse canned vegetables/beans to remove excess sodium where possible.",
            "Use potassium-rich foods (bananas, spinach, tomatoes, sweet potato) to support BP.",
            "Flavor with herbs, citrus, vinegar, and garlic instead of salt.",
            "Prefer whole grains and fiber-rich cereals over refined carbs.",
            "Eat unsalted nuts and seeds as snacks instead of salted chips.",
            "Limit alcohol intake—excess raises blood pressure.",
            "Choose low-sodium dairy or reduced-salt cheese options.",
            "Avoid processed meats and cured foods high in sodium.",
            "Use low-sodium broths when cooking soups or stews.",
            "Limit pickles and sauces consumed at the table.",
            "Moderate caffeine; consider your personal sensitivity when exercising or before bed.",
            "Opt for fresh or frozen vegetables without sauces or added salt.",
            "Incorporate oats/psyllium for soluble fiber to help with lipids.",
            "Keep hydration steady—dehydration sometimes causes compensatory BP changes.",
            "Consider hibiscus tea in moderation—some benefit shown for BP lowering.",
            "Plan meals with herbs like coriander, cumin, and pepper for complexity without salt.",
            "Avoid energy drinks that can spike blood pressure."
        ],
        "habits": [
            "Aim for 20–40 min of moderate aerobic activity daily—start gently and build up.",
            "Include 2 strength sessions per week to support vascular health.",
            "Practice daily breathing or meditation (4–7–8 or box breathing).",
            "Sleep 7–9 hours on a regular schedule to support BP regulation.",
            "Check home blood pressure twice daily initially to establish baseline.",
            "Stand and move hourly to reduce vascular stiffness from sitting.",
            "Weigh weekly when actively reducing weight; small losses can lower BP.",
            "Avoid tobacco in any form; even occasional use worsens BP.",
            "Set medication reminders to avoid missed doses.",
            "Reduce screen time close to bedtime to improve sleep quality.",
            "Plan active commuting or short walking meetings when possible.",
            "Avoid heavy lifting spikes unless medically cleared—they transiently raise BP.",
            "Make home-cooked meals to control salt and portion sizes.",
            "Use a simple relaxation routine pre-bed (warm shower, breathing) to lower nighttime BP.",
            "Pair TV time with light mobility or stretching to reduce sedentary load.",
            "Identify personal stress triggers and a short response plan (5-min walk, breathing).",
            "Have a calibrated home BP cuff and log values to discuss with clinician.",
            "Limit NSAID overuse—these can raise blood pressure in some individuals.",
            "Avoid excessive licorice and certain herbal supplements that can raise BP.",
            "Build a social support system to help maintain lifestyle adjustments."
        ],
        "prevention": [
            "Treat BP consistently—do not stop meds without clinician guidance.",
            "Aim for gradual weight reduction if overweight to help lower BP.",
            "Address sleep apnea if loud snoring/daytime sleepiness occur—treating it lowers BP.",
            "Reassess the salt content of favorite recipes monthly and reduce gradually.",
            "Avoid chronic high-stress exposure by planning recovery days.",
            "Coordinate care if you have diabetes or kidney disease; combined risks raise priority.",
            "Check kidney function and electrolytes as advised by clinician.",
            "Keep alcohol intake well within recommended limits.",
            "Have an action plan for sudden very high readings (contact clinician/emergency services).",
            "Avoid extreme diets that may cause electrolyte disturbances affecting BP.",
            "Stay mindful of medication interactions (e.g., decongestants raise BP).",
            "Use relaxation apps or short daily guided meditations to reduce baseline stress.",
            "Educate family on when to seek urgent help for severe BP-related symptoms.",
            "Plan lower-sodium restaurant choices: ask for sauces/salt on the side.",
            "Monitor caffeine and stimulant-containing supplement use.",
            "Consider supervised exercise programs if starting new routines.",
            "Keep track of dietary potassium sources and maintain balance with clinician advice.",
            "Recheck BP after travel or sleep routine disruptions.",
            "Avoid energy drinks and stimulant-heavy preworkout supplements.",
            "Engage in community support or groups for chronic disease prevention accountability."
        ]
    },

    "Obesity": {
        "diet": [
            "Create a small calorie deficit (≈300–500 kcal/day) for sustainable weight loss.",
            "Prioritize protein at each meal to support satiety and muscle retention.",
            "Fill half the plate with vegetables to increase volume without many calories.",
            "Swap sugary drinks and juices for plain water or unsweetened tea.",
            "Limit highly-processed hyper-palatable foods kept at home.",
            "Plan two balanced snacks daily to reduce binge impulses.",
            "Use smaller plates and bowls to reduce portions automatically.",
            "Batch-cook lean proteins and vegetables for easy, healthy meals.",
            "Avoid skipping breakfast to reduce later-day overeating for many people.",
            "Choose whole grains and fiber-rich carbs for lasting fullness.",
            "Measure oil and nut servings — they’re nutritious but calorie-dense.",
            "Replace creamy sauces with tomato or yogurt-based alternatives.",
            "Favor home-cooked meals to control ingredients and portions.",
            "Limit alcohol—alcohol adds calories and reduces inhibitions.",
            "Keep fruit visible and sweets out of immediate sight for habit control.",
            "Plan meals for busy days to avoid fast-food fallback.",
            "Replace vending machine snacks with fruit, yogurt, or unsalted nuts.",
            "Prepare a simple protein-based breakfast to curb mid-day cravings.",
            "Use vinegar or citrus to add flavor without calories.",
            "Track intake for a short sample period to learn true calorie habits."
        ],
        "habits": [
            "Aim for at least 150 minutes/week moderate activity, increase to 250–300 for greater weight loss.",
            "Include 2–3 resistance training sessions/week to preserve muscle mass.",
            "Increase NEAT: take stairs, park further, stand for tasks when possible.",
            "Sleep 7–9 hours; poor sleep dysregulates appetite and hunger hormones.",
            "Plan grocery shops with a list and avoid shopping when hungry.",
            "Keep trigger foods out of the home environment or out of sight.",
            "Use mindful eating: chew slowly, pause between bites, notice fullness.",
            "Track body weight weekly rather than daily to smooth noise.",
            "Celebrate non-scale victories (energy, improved fitness, clothing fit).",
            "Use accountability: a friend, coach, or support group can help adherence.",
            "Pair sedentary hobbies with mini-active breaks (e.g., walk during ads).",
            "Take short walks after meals to assist satiety and glucose control.",
            "Build incremental changes—one sustainable habit per week.",
            "Keep a small home kit (band, mat, light dumbbells) to remove barriers to exercise.",
            "Avoid all-or-nothing thinking; aim for progress over perfection.",
            "Use automated reminders to plan workouts and wind-down routines.",
            "Pre-log meals in a tracker to set realistic daily intake targets.",
            "Plan active weekend activities (hiking, cycling) to boost weekly activity.",
            "Limit screen time in the evening to improve sleep and reduce nighttime snacking.",
            "Practice stress-management tools to reduce emotional eating triggers."
        ],
        "prevention": [
            "Protect muscle mass during weight loss with adequate protein and resistance training.",
            "Get baseline labs (glucose, lipids, liver enzymes) and repeat as advised.",
            "Screen for sleep apnea if you snore or have daytime sleepiness.",
            "Consider behavioral therapy for emotional or binge eating patterns.",
            "Set realistic, incremental weight targets (e.g., 0.25–0.75 kg/week).",
            "Plan holiday strategies to avoid large setbacks (small portions, extra activity).",
            "Use a long-term maintenance plan after weight loss—do not expect 'finish line'.",
            "Engage a registered dietitian for personalized planning when needed.",
            "Monitor for weight-regain triggers and have a rapid action plan.",
            "Avoid crash dieting; they often cause rebound weight gain.",
            "Use meal prep to increase adherence on busy days.",
            "Keep healthy snacks in your bag and car to avoid poor choices when hungry.",
            "Review medications with clinician if weight gain seems medication-related.",
            "Encourage family-based changes to make the environment supportive.",
            "Plan for relapse events—identify triggers and a recovery strategy.",
            "Use a combination of diet, activity, sleep, and stress management for best outcomes.",
            "Consider structured programs or supervised exercise if self-guided attempts plateau.",
            "Check for endocrine contributors (thyroid, Cushing’s) if unexplained weight changes occur.",
            "Recognize that maintenance is a distinct phase—plan support for it.",
            "Work on healthy body image and psychological well-being alongside weight goals."
        ]
    }
}  # end GUIDANCE

# -------- Routes --------
@app.route("/predict", methods=["GET", "POST"])
def predict():
    err = None
    if request.method == "POST":
        vals = []
        for f in FEATURES:
            v = request.form.get(f, "").strip()
            if v == "":
                err = f"Missing value for {f}"
                return render_template("home.html", features=FEATURES, error=err)
            try:
                vals.append(float(v))
            except ValueError:
                err = f"Invalid numeric value for {f}"
                return render_template("home.html", features=FEATURES, error=err)
        X = np.array(vals, dtype=float).reshape(1, -1)
        Xs = scaler.transform(X) if scaler is not None else X
        if model is None:
            #pred = 0
            err = "Error: Model is not loaded properly. Please check the model file."
            return render_template("home.html", features=FEATURES, error=err)
        else:
            raw = model.predict(Xs)[0]
            label = map_label(raw)
            pred = label
        
        # Store prediction in session
        session["prediction"] = pred
        # clear rotation indices for new session/prediction
        session["rot"] = {}
        
        # Save encrypted prediction data to database
        username = session.get('username')
        if username:
            try:
                # Create inputs dictionary
                inputs_dict = {}
                for i, f in enumerate(FEATURES):
                    inputs_dict[f] = vals[i]
                
                # Encrypt the data
                encrypted_data = encrypt_prediction_data(username, inputs_dict, pred)
                
                # Save to database
                con = sqlite3.connect('signup.db')
                cur = con.cursor()
                cur.execute('''
                    INSERT INTO prediction_history (username, encrypted_data)
                    VALUES (?, ?)
                ''', (username, encrypted_data))
                con.commit()
                con.close()
            except Exception as e:
                print(f"Error saving prediction history: {e}")
        
        return render_template("chat.html", disease=pred) #redirect(url_for("chat"))
    return render_template("home.html", features=FEATURES, error=err)

@app.route("/chat", methods=["GET"])
def chat():
    disease = session.get("prediction", "None")
    if isinstance(disease, int) or disease.isdigit() if isinstance(disease, str) else False:
        disease = map_label(disease)
    return render_template("chat.html", disease=disease)

@app.route("/chat/send", methods=["POST"])
def chat_send():
    data = request.get_json(force=True)
    user_text = (data.get("message") or "").lower()
    disease = session.get("prediction", "None")
    disease = map_label(disease) if not isinstance(disease, str) or disease in LABELS else str(disease)

    kb = GUIDANCE.get(disease, GUIDANCE["None"])

    # intent detection
    if any(k in user_text for k in ["diet","food","meal","eat","nutrition","what to eat","foods"]):
        bucket = "diet"
    elif any(k in user_text for k in ["habit","exercise","workout","walk","steps","sleep","stress","activity"]):
        bucket = "habits"
    elif any(k in user_text for k in ["prevent","prevention","control","reduce risk","avoid","complication"]):
        bucket = "prevention"
    elif "more" == user_text.strip():
        # if user asks "more", return next tip across buckets in rotation preference
        bucket = session.get("last_bucket", "diet")
    else:
        bucket = None

    reply = ""
    if bucket is None:
        reply = (f"Hi — I can provide tips for *diet*, *habits* (exercise/sleep/stress), or *prevention* "
                 f"for {disease}. Try asking: 'diet', 'habits', or 'prevention'.")
    else:
        items = kb.get(bucket, [])
        if not items:
            reply = "I don't have items for that category; try another (diet/habits/prevention)."
        else:
            # rotation index stored in session to give variety
            rot = session.setdefault("rot", {}).get(f"{disease}_{bucket}", 0)
            tip = items[rot % len(items)]
            # increment and store
            session["rot"][f"{disease}_{bucket}"] = (rot + 1) % len(items)
            session.modified = True
            reply = f"{bucket.title()} tip: {tip}"
            session["last_bucket"] = bucket

    return jsonify({"reply": reply, "disease": disease})



@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        username = request.form.get('user','')
        name = request.form.get('name','')
        email = request.form.get('email','')
        number = request.form.get('mobile','')
        password = request.form.get('password','')

        # Server-side validation
        username_pattern = r'^.{6,}$'
        name_pattern = r'^[A-Za-z ]{3,}$'
        email_pattern = r'^[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$'
        mobile_pattern = r'^[6-9][0-9]{9}$'
        password_pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$'

        if not re.match(username_pattern, username):
            return render_template("signup.html", message="Username must be at least 6 characters.")
        if not re.match(name_pattern, name):
            return render_template("signup.html", message="Full Name must be at least 3 letters, only letters and spaces allowed.")
        if not re.match(email_pattern, email):
            return render_template("signup.html", message="Enter a valid email address.")
        if not re.match(mobile_pattern, number):
            return render_template("signup.html", message="Mobile must start with 6-9 and be 10 digits.")
        if not re.match(password_pattern, password):
            return render_template("signup.html", message="Password must be at least 8 characters, with an uppercase letter, a number, and a lowercase letter.")

        con = sqlite3.connect('signup.db')
        cur = con.cursor()
        cur.execute("SELECT 1 FROM info WHERE user = ?", (username,))
        if cur.fetchone():
            con.close()
            return render_template("signup.html", message="Username already exists. Please choose another.")
        
        cur.execute("insert into `info` (`user`,`name`, `email`,`mobile`,`password`) VALUES (?, ?, ?, ?, ?)",(username,name,email,number,password))
        con.commit()
        con.close()
        return redirect(url_for('login'))

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    else:
        mail1 = request.form.get('user','')
        password1 = request.form.get('password','')
        con = sqlite3.connect('signup.db')
        cur = con.cursor()
        cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
        data = cur.fetchone()

        if data == None:
            return render_template("signin.html", message="Invalid username or password.")    

        elif mail1 == 'admin' and password1 == 'admin':
            session['username'] = 'admin'
            return render_template("home.html")

        elif mail1 == str(data[0]) and password1 == str(data[1]):
            session['username'] = mail1
            return render_template("home.html")
        else:
            return render_template("signin.html", message="Invalid username or password.")

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/home')
def home():
	return render_template('home.html')


@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')

@app.route('/history')
def history():
    """Display prediction history for the logged-in user"""
    username = session.get('username')
    if not username:
        return redirect(url_for('signin'))
    
    try:
        con = sqlite3.connect('signup.db')
        cur = con.cursor()
        cur.execute('''
            SELECT id, encrypted_data, created_at
            FROM prediction_history
            WHERE username = ?
            ORDER BY created_at DESC
        ''', (username,))
        records = cur.fetchall()
        con.close()
        
        # Decrypt the data
        history_data = []
        for record in records:
            try:
                decrypted = decrypt_prediction_data(username, record[1])
                history_data.append({
                    'id': record[0],
                    'inputs': decrypted.get('inputs', {}),
                    'prediction': decrypted.get('prediction', 'Unknown'),
                    'created_at': record[2]
                })
            except Exception as e:
                print(f"Error decrypting record {record[0]}: {e}")
                continue
        
        return render_template('history.html', history=history_data, username=username)
    except Exception as e:
        print(f"Error fetching history: {e}")
        return render_template('history.html', history=[], username=username, error=str(e))

if __name__ == "__main__":
    app.run(debug=True)
