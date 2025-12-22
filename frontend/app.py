# import streamlit as st
# import requests
# import folium
# from streamlit_folium import st_folium
# from folium import plugins
# import pandas as pd
# import difflib

# # CONFIG
# API_URL = "http://127.0.0.1:8000/optimize"

# # --- EXPANDED CITY DATABASE (Prevents "Mathura" -> "Madurai" errors) ---
# INDIAN_CITIES = [
#     # Tier 1
#     "Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Surat",
    
#     # Tier 2
#     "Pune", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal", 
#     "Visakhapatnam", "Pimpri-Chinchwad", "Patna", "Vadodara", "Ghaziabad", "Ludhiana", 
#     "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot", "Kalyan-Dombivli", "Vasai-Virar", 
#     "Varanasi", "Srinagar", "Aurangabad", "Dhanbad", "Amritsar", "Navi Mumbai", "Prayagraj", 
#     "Howrah", "Ranchi", "Jabalpur", "Gwalior", "Coimbatore", "Vijayawada", "Jodhpur", 
#     "Madurai", "Raipur", "Kota", "Guwahati", "Chandigarh", "Solapur", "Hubli–Dharwad", 
#     "Tiruchirappalli", "Tiruppur", "Moradabad", "Mysore", "Bareilly", "Gurgaon", "Aligarh", 
#     "Jalandhar", "Bhubaneswar", "Salem", "Mira-Bhayandar", "Warangal", "Thiruvananthapuram", 
#     "Guntur", "Bhiwandi", "Saharanpur", "Gorakhpur", "Bikaner", "Amravati", "Noida", 
#     "Jamshedpur", "Bhilai", "Cuttack", "Firozabad", "Kochi", "Nellore", "Bhavnagar", 
#     "Dehradun", "Durgapur", "Asansol", "Nanded", "Kolhapur", "Ajmer", "Kalaburagi", 
#     "Jamnagar", "Ujjain", "Loni", "Siliguri", "Jhansi", "Ulhasnagar", "Jammu", 
#     "Sangli-Miraj & Kupwad", "Mangalore", "Erode", "Belgaum", "Ambattur", "Tirunelveli", 
#     "Malegaon", "Gaya", "Jalgaon", "Udaipur", "Maheshtala", "Davanagere", "Kozhikode", 
#     "Kurnool", "Akola", "Rajpur Sonarpur", "Rajahmundry", "Bokaro", "South Dumdum", 
#     "Bellary", "Patiala", "Gopalpur", "Agartala", "Bhagalpur", "Muzaffarnagar", "Bhatpara", 
#     "Panihati", "Latur", "Dhule", "Tirupati", "Rohtak", "Korba", "Bhilwara", "Berhampur", 
#     "Muzaffarpur", "Ahmednagar", "Mathura", "Kollam", "Avadi", "Kadapa", "Kamarhati", 
#     "Bilaspur", "Shahjahanpur", "Bijapur", "Rampur", "Shivamogga", "Chandrapur", "Junagadh", 
#     "Thrissur", "Alwar", "Bardhaman", "Kulti", "Kakinada", "Nizamabad", "Parbhani", "Tumkur", 
#     "Khammam", "Ozhukarai", "Bihar Sharif", "Panipat", "Darbhanga", "Bally", "Aizawl", 
#     "Dewas", "Ichalkaranji", "Karnal", "Bathinda", "Jalna", "Eluru", "Kirari Suleman Nagar", 
#     "Barasat", "Purnia", "Satna", "Mau", "Sonipat", "Farrukhabad", "Sagar", "Rourkela", 
#     "Durg", "Imphal", "Ratlam", "Hapur", "Arrah", "Karimnagar", "Anantapur", "Etawah", 
#     "Ambarnath", "North Dumdum", "Bharatpur", "Begusarai", "New Delhi", "Gandhidham", 
#     "Baranagar", "Tiruvottiyur", "Pondicherry", "Sikar", "Thoothukudi", "Rewa", "Mirzapur", 
#     "Raichur", "Pali", "Ramagundam", "Silchar", "Haridwar", "Vizianagaram", "Tenali", 
#     "Nagercoil", "Sri Ganganagar", "Karawal Nagar", "Mango", "Thanjavur", "Bulandshahr", 
#     "Uluberia", "Murwara", "Sambhal", "Singrauli", "Nadiad", "Secunderabad", "Naihati", 
#     "Yamunanagar", "Bidhan Nagar", "Pallavaram", "Bidar", "Munger", "Panchkula", "Burhanpur", 
#     "Raurkela Industrial Township", "Kharagpur", "Dindigul", "Gandhinagar", "Hospet", 
#     "Nangloi Jat", "Malda", "Ongole", "Deoghar", "Chapra", "Haldia", "Khandwa", "Nandyal", 
#     "Chittoor", "Morena", "Amroha", "Anand", "Bhind", "Bhalswa Jahangir Pur", "Madhyamgram", 
#     "Bhiwani", "Navi Mumbai Panvel Raigad", "Baharampur", "Ambala", "Morvi", "Fatehpur", 
#     "Rae Bareli", "Khora", "Bhusawal", "Orai", "Bahraich", "Vellore", "Mahesana", "Sambalpur", 
#     "Raiganj", "Sirsa", "Danapur", "Serampore", "Sultan Pur Majra", "Guna", "Jaunpur", 
#     "Panvel", "Shivpuri", "Surendranagar Dudhrej", "Unnao", "Hugli and Chinsurah", "Alappuzha", 
#     "Kottayam", "Machilipatnam", "Shimla", "Adoni", "Udupi", "Katihar", "Proddatur", 
#     "Mahbubnagar", "Saharsa", "Dibrugarh", "Jorhat", "Hazaribagh", "Hindupur", "Nagaon", 
#     "Hajipur", "Sasaram", "Giridih", "Bhimavaram", "Kumbakonam", "Bongaigaon", "Dehri", 
#     "Madanapalle", "Siwan", "Bettiah", "Ramgarh", "Tinsukia", "Guntakal", "Srikakulam", 
#     "Motihari", "Dharmavaram", "Gudivada", "Phagwara", "Pudukkottai", "Hosur", "Narasaraopet", 
#     "Suryapet", "Miryalaguda", "Tadipatri", "Karaikudi", "Kishanganj", "Jamalpur", "Ballia", 
#     "Kavali", "Tadepalligudem", "Amaravati", "Buxar", "Tezpur", "Jehanabad", "Aurangabad", 
#     "Gangtok", "Vasco Da Gama"
# ]

# def correct_spelling(city_name):
#     """
#     Smart Auto-Correct:
#     1. Returns exact match if exists.
#     2. Returns fuzzy match ONLY if similarity > 80% (Prevents Mathura->Madurai).
#     3. Returns original input if uncertain.
#     """
#     if not city_name: return city_name
    
#     clean_input = city_name.strip()
    
#     # 1. Exact Match (Case Insensitive)
#     city_map = {c.lower(): c for c in INDIAN_CITIES}
#     if clean_input.lower() in city_map:
#         return city_map[clean_input.lower()]

#     # 2. Fuzzy Match (Strict Cutoff 0.8)
#     # This prevents "Mathura" (M...a) matching "Madurai" (M...a) loosely
#     matches = difflib.get_close_matches(clean_input, INDIAN_CITIES, n=1, cutoff=0.8)
    
#     if matches:
#         return matches[0]
    
#     # 3. No confident match? Trust the user!
#     return clean_input

# st.set_page_config(page_title="Flipr Logistics AI", layout="wide")

# # --- SESSION STATE ---
# if 'destinations' not in st.session_state:
#     st.session_state['destinations'] = []
# if 'optimization_result' not in st.session_state:
#     st.session_state['optimization_result'] = None

# st.title("🚛 AI-Powered Route Optimizer")

# # --- SIDEBAR ---
# with st.sidebar:
#     st.header("1. Configuration")
#     source_input = st.text_input("Source City", "Delhi")
#     source_name = correct_spelling(source_input)
    
#     # Show feedback on source name
#     if source_name != source_input and source_name.lower() != source_input.lower():
#         st.caption(f"✨ Auto-corrected to: **{source_name}**")
#     elif source_name not in INDIAN_CITIES and source_input:
#         st.caption(f"⚠️ Unknown city. Using raw input.")

#     st.divider()
#     st.header("2. Add Destination")
    
#     new_city_input = st.text_input("City Name")
    
#     c1, c2 = st.columns(2)
#     with c1:
#         new_priority = st.selectbox("Priority", [1, 2, 3], index=2, help="1=Urgent")
#     with c2:
#         new_deadline = st.number_input("Deadline (Hrs)", min_value=1.0, value=24.0, step=1.0, format="%.1f")
        
#     if st.button("➕ Add Stop"):
#         if new_city_input:
#             final_name = correct_spelling(new_city_input)
#             target_id = final_name.lower().replace(" ", "_")
            
#             # --- DUPLICATE CHECK LOGIC ---
#             # Check if this ID already exists in our list
#             existing_idx = -1
#             for i, d in enumerate(st.session_state['destinations']):
#                 if d['id'] == target_id:
#                     existing_idx = i
#                     break
            
#             if existing_idx != -1:
#                 # UPDATE existing entry
#                 st.session_state['destinations'][existing_idx]['priority'] = new_priority
#                 st.session_state['destinations'][existing_idx]['deadline_hours'] = new_deadline
#                 st.warning(f"⚠️ City '{final_name}' already exists! Updated with new settings.")
#             else:
#                 # ADD new entry
#                 st.session_state['destinations'].append({
#                     "id": target_id,
#                     "name": final_name,
#                     "priority": new_priority,
#                     "deadline_hours": new_deadline,
#                     "service_time_minutes": 30
#                 })
                
#                 if final_name != new_city_input:
#                     st.info(f"✨ Auto-corrected '{new_city_input}' -> '{final_name}'")
#                 else:
#                     st.success(f"Added {final_name}")
#         else:
#             st.error("Please enter a city name")

#     st.divider()
#     st.header("3. Manage Stops")
    
#     if st.session_state['destinations']:
#         for i, dest in enumerate(st.session_state['destinations']):
#             c_name, c_del = st.columns([3, 1])
#             with c_name:
#                 st.write(f"**{i+1}. {dest['name']}** (P{dest['priority']}, {dest['deadline_hours']}h)")
#             with c_del:
#                 if st.button("❌", key=f"del_{i}"):
#                     st.session_state['destinations'].pop(i)
#                     st.session_state['optimization_result'] = None
#                     st.rerun()
        
#         if st.button("🗑️ Clear All"):
#             st.session_state['destinations'] = []
#             st.session_state['optimization_result'] = None
#             st.rerun()

#     st.divider()
#     if st.button("🚀 Optimize Route", type="primary"):
#         if not st.session_state['destinations']:
#             st.error("Add at least one destination!")
#         else:
#             payload = {
#                 "source": {"id": source_name.lower(), "name": source_name},
#                 "destinations": st.session_state['destinations'],
#                 "vehicle_speed_kmh": 60.0
#             }
            
#             with st.spinner("🤖 AI is finding the best route..."):
#                 try:
#                     response = requests.post(API_URL, json=payload)
#                     if response.status_code == 200:
#                         st.session_state['optimization_result'] = response.json()
#                     else:
#                         st.error(f"API Error: {response.text}")
#                 except Exception as e:
#                     st.error(f"Connection Error: {e}")

# # --- MAIN DISPLAY ---
# result = st.session_state['optimization_result']

# if result:
#     c1, c2, c3 = st.columns(3)
#     c1.metric("Total Distance", f"{result['total_distance_km']} km")
#     c2.metric("Total Duration", f"{result['total_time_hours']} hrs")
#     c3.metric("Solver", result['solver_used'])
    
#     st.success(f"📝 {result['summary']}")

#     col_map, col_table = st.columns([2, 1])

#     with col_table:
#         st.subheader("📍 Schedule")
#         display_data = []
#         for item in result['schedule']:
#             # Warn if late
#             warning = "⚠️" if "LATE" in item.get('status', '') else ""
#             display_data.append({
#                 "Stop": f"{item['stop_name']} {warning}", 
#                 "Arr": f"{item['arrival_time']:.2f} h",
#                 "Dep": f"{item['departure_time']:.2f} h"
#             })
#         st.dataframe(pd.DataFrame(display_data), hide_index=True)

#     with col_map:
#         st.subheader("🗺️ Live Map")
#         if result['schedule']:
#             start_lat = result['schedule'][0].get('lat', 20.59)
#             start_lon = result['schedule'][0].get('lon', 78.96)
            
#             m = folium.Map(location=[start_lat, start_lon], zoom_start=5)
            
#             route_coords = []
#             for idx, item in enumerate(result['schedule']):
#                 lat, lon = item.get('lat', 0), item.get('lon', 0)
#                 if lat == 0 and lon == 0: continue
                
#                 route_coords.append([lat, lon])
                
#                 color = "red" if idx == 0 or idx == len(result['schedule'])-1 else "blue"
#                 if "LATE" in item.get('status', ''): color = "orange"
                
#                 folium.Marker(
#                     location=[lat, lon],
#                     popup=f"{idx}. {item['stop_name']}",
#                     icon=folium.Icon(color=color, icon="truck", prefix="fa")
#                 ).add_to(m)
            
#             # --- DRAW PATH WITH ARROWS ---
#             # 1. Draw the main blue line
#             path_line = folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.8).add_to(m)
            
#             # 2. Add directional arrows using PolyLineTextPath
#             plugins.PolyLineTextPath(
#                 path_line,
#                 "      ➤      ", # Arrow symbol with padding for spacing
#                 repeat=True,
#                 offset=7,       # Center alignment adjustment
#                 attributes={'fill': '#0000FF', 'font-weight': 'bold', 'font-size': '24'}
#             ).add_to(m)
#             # -----------------------------

#             st_folium(m, width=800, height=500)




# ////////////////////

import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from folium import plugins
import pandas as pd

# ===================== CONFIG =====================
API_URL = "https://flipr-ai-powered-route-optimizer.onrender.com/optimize"
REPORT_API_URL = "https://flipr-ai-powered-route-optimizer.onrender.com/generate-report"
GEOCODE_URL = "https://nominatim.openstreetmap.org/search"
# REPORT_API_URL = "http://127.0.0.1:8000/generate-report"

HEADERS = {
    "User-Agent": "Flipr-Logistics-AI/1.0"
}

# ===================== INDIA-ONLY CITY VALIDATION =====================
# def validate_city_india_only(city_name: str):
#     """
#     STRICT + PRACTICAL validation:
#     ✔ Only real Indian cities / towns / capitals
#     ❌ No cafes, shops, salons, streets
#     ❌ No foreign city names mapped to Indian POIs
#     """
#     if not city_name or len(city_name.strip()) < 3:
#         return False, None, None

#     query = city_name.strip().lower()

#     params = {
#         "q": city_name.strip(),
#         "format": "json",
#         "limit": 10,
#         "countrycodes": "in",
#         "addressdetails": 1
#     }

#     try:
#         r = requests.get(GEOCODE_URL, params=params, headers=HEADERS, timeout=5)
#         data = r.json()

#         if not data:
#             return False, None, None

#         for place in data:
#             address = place.get("address", {})
#             place_class = place.get("class", "")
#             place_type = place.get("type", "")

#             # 1️⃣ Must be India
#             if address.get("country_code", "").lower() != "in":
#                 continue

#             # 2️⃣ Reject POIs (cafes, shops, roads)
#             if place_class in ["amenity", "shop", "tourism", "leisure", "highway"]:
#                 continue

#             # 3️⃣ Allowed admin / city cases
#             valid_place = (
#                 (place_class == "place" and place_type in ["city", "town"]) or
#                 (place_class == "boundary" and place_type == "administrative")
#             )

#             if not valid_place:
#                 continue

#             returned_name = (
#                 address.get("city") or
#                 address.get("city_district") or
#                 address.get("municipality") or
#                 address.get("town") or
#                 address.get("county") or
#                 address.get("state") or
#                 ""
#             ).lower()

#             # 5️⃣ Exact match OR Delhi special-case
#             if query not in returned_name and returned_name not in query:
#                 if not (
#                     query in ["delhi", "new delhi"] and
#                     returned_name in ["delhi", "new delhi"]
#                 ):
#                     continue

#             lat = float(place["lat"])
#             lon = float(place["lon"])
#             return True, lat, lon

#         return False, None, None

#     except Exception:
#         return False, None, None

def normalize_city_name(name: str) -> str:
    """Normalize common Indian city aliases"""
    name = name.lower().strip()

    aliases = {
        "bangalore": "bengaluru",
        "bengaluru": "bengaluru",
        "madras": "chennai",
        "calcutta": "kolkata",
        "trivandrum": "thiruvananthapuram"
    }

    return aliases.get(name, name)


def validate_city_india_only(city_name: str):
    """
    PRACTICAL + ROBUST validation:
    ✔ Accept Indian cities/towns even if district/state differs
    ✔ Case-insensitive
    ✔ Handles Bangalore/Bengaluru etc.
    """
    if not city_name or len(city_name.strip()) < 3:
        return False, None, None

    query = normalize_city_name(city_name)

    params = {
        "q": city_name,
        "format": "json",
        "limit": 10,
        "countrycodes": "in",
        "addressdetails": 1
    }

    try:
        r = requests.get(GEOCODE_URL, params=params, headers=HEADERS, timeout=5)
        data = r.json()

        if not data:
            return False, None, None

        for place in data:
            address = place.get("address", {})
            place_class = place.get("class", "")
            place_type = place.get("type", "")

            # Must be India
            if address.get("country_code", "").lower() != "in":
                continue

            # Reject POIs
            if place_class in ["amenity", "shop", "tourism", "leisure", "highway"]:
                continue

            # Accept cities, towns, districts, administrative regions
            if not (
                (place_class == "place" and place_type in ["city", "town", "village"]) or
                (place_class == "boundary" and place_type == "administrative")
            ):
                continue

            lat = float(place["lat"])
            lon = float(place["lon"])
            return True, lat, lon

        return False, None, None

    except Exception:
        return False, None, None

# ===================== STREAMLIT CONFIG =====================
st.set_page_config(page_title="AI Route Optimizer", layout="wide")

if "destinations" not in st.session_state:
    st.session_state["destinations"] = []

if "optimization_result" not in st.session_state:
    st.session_state["optimization_result"] = None

if "csv_processed" not in st.session_state:
    st.session_state["csv_processed"] = False

if "csv_uploader_key" not in st.session_state:
    st.session_state["csv_uploader_key"] = 0

if "last_csv_signature" not in st.session_state:
    st.session_state["last_csv_signature"] = None

st.title("🚛 AI-Powered Indian Route Optimizer")

# ===================== HELPER: Onboarding / How-to =====================
def show_how_to_use():
    st.info("👋 Welcome — here’s how to use the AI Route Optimizer")
    st.markdown("""
### 🪜 Quick Start (in this order)

**1) Source City**
- Enter the starting city (India only). Example: *Delhi*

**2) Add Destinations**
- **Manual**: Type city name → set *Priority* (1=High,2=Med,3=Low) → set *Deadline (hrs)* → click **➕ Add Stop**
- **Input**: Type the city name(India only). Example: *Jaipur* or you can also add like this *Jaipur,Rajasthan*                
- **Upload CSV/JSON/XLSX**: Use the uploader to import many stops at once.

**CSV / Excel format (example)**:
- Input columns `city`, `priority` and `deadline_hours`.

**JSON format**:
- city, priority and deadline_hours are required

**3) Review & Edit**
- Use the Destinations List to remove or clear stops.

**4) Optimize**
- Click **🚀 Optimize Route**. AI will compute route, schedule, and summary.

**After Optimize**
- You’ll see: AI Summary, Interactive Map, Schedule table and a button to **Download Route Report (PDF)**.

---

Tip: If you uploaded a file and nothing appears, check that the `city` column exists and spelled correctly.
""")

# ===================== SIDEBAR =====================
with st.sidebar:
    st.header("1️⃣ Source City (India only)")
    source_input = st.text_input("Source City", "Delhi")
    valid_src, src_lat, src_lon = validate_city_india_only(source_input)

    if not valid_src:
        st.error("❌ Enter a valid Indian city")
    else:
        st.success(f"📍 Source OK ({src_lat:.2f}, {src_lon:.2f})")

    st.divider()

    st.header("2️⃣ Add Destination")
    st.subheader("📤 Upload Destinations via CSV")

    uploaded_file = st.file_uploader(
        "Upload CSV, JSON, or Excel file",
        type=["csv", "json", "xlsx", "xls"],
        key=f"uploader_{st.session_state['csv_uploader_key']}",
        help="CSV / JSON / Excel. Fields: city (required), priority, deadline_hours"
    )

    csv_signature = None
    if uploaded_file is not None:
        csv_signature = (uploaded_file.name, uploaded_file.size)

    if uploaded_file is not None and csv_signature != st.session_state["last_csv_signature"]:
        try:
            filename = uploaded_file.name.lower()
            # ---------- LOAD FILE ----------
            if filename.endswith(".csv"):
                df = pd.read_csv(uploaded_file, header=None)
                first_row = df.iloc[0].astype(str).str.lower().tolist()
                has_header = "city" in first_row
                uploaded_file.seek(0)
                if has_header:
                    df = pd.read_csv(uploaded_file)
                else:
                    df.columns = ["city", "priority", "deadline_hours"][:len(df.columns)]
            elif filename.endswith(".json"):
                df = pd.read_json(uploaded_file)
            elif filename.endswith((".xlsx", ".xls")):
                df = pd.read_excel(uploaded_file)
            else:
                st.error("❌ Unsupported file format")
                st.stop()

            # ---------- VALIDATE ----------
            if "city" not in df.columns:
                st.error("❌ File must contain a 'city' column")
                st.stop()

            added, updated, skipped = 0, 0, 0
            # ---------- PROCESS ----------
            for _, row in df.iterrows():
                raw_city = str(row.get("city", "")).strip()
                if not raw_city:
                    skipped += 1
                    continue

                valid, lat, lon = validate_city_india_only(raw_city)
                if not valid:
                    skipped += 1
                    continue

                city_name = raw_city.title()
                city_id = city_name.lower().replace(" ", "_")

                priority = int(row.get("priority", 3)) if not pd.isna(row.get("priority", 3)) else 3
                deadline = float(row.get("deadline_hours", 24)) if not pd.isna(row.get("deadline_hours", 24)) else 200.0

                if city_id in [d["id"] for d in st.session_state["destinations"]]:
                    updated += 1
                else:
                    st.session_state["destinations"].append({
                        "id": city_id,
                        "name": city_name,
                        "priority": priority,
                        "deadline_hours": deadline,
                        "lat": lat,
                        "lon": lon,
                        "service_time_minutes": 30
                    })
                    added += 1

            # ---------- FINALIZE ----------
            st.session_state["last_csv_signature"] = csv_signature
            st.session_state["csv_processed"] = True
            st.session_state["csv_uploader_key"] += 1

            st.success(f"✅ Imported → {added} added | {updated} updated | {skipped} skipped")

        except Exception as e:
            st.error(f"❌ Failed to read file: {e}")

    new_city = st.text_input("City Name")
    new_priority = st.selectbox("Priority", [1, 2, 3], index=2)
    new_deadline = st.number_input("Deadline (hrs)", min_value=1.0, value=200.0)

    if st.button("➕ Add Stop"):
        valid, lat, lon = validate_city_india_only(new_city)

        if not new_city:
            st.error("Please enter a city name")
        elif not valid:
            st.error("❌ Enter a valid Indian city")
        else:
            city_name = new_city.strip().title()
            city_id = city_name.lower().replace(" ", "_")

            if city_id in [d["id"] for d in st.session_state["destinations"]]:
                st.warning("⚠️ City already added")
            else:
                st.session_state["destinations"].append({
                    "id": city_id,
                    "name": city_name,
                    "priority": new_priority,
                    "deadline_hours": new_deadline,
                    "lat": lat,
                    "lon": lon,
                    "service_time_minutes": 30
                })
                st.success(f"✅ Added {city_name}")

    st.divider()

    st.header("3️⃣ Destinations List")
    # for i, d in enumerate(st.session_state["destinations"]):
    #     c1, c2 = st.columns([3, 1])
    #     with c1:
    #         st.write(f"{i+1}. {d['name']} (P{d['priority']})")
    for i, d in enumerate(st.session_state["destinations"]):
        c1, c2 = st.columns([3, 1])
        with c1:
            st.write(
                f"{i+1}. **{d['name']}** "
                f"(P{d['priority']}, {int(d['deadline_hours'])}h)"
        )

        with c2:
            if st.button("❌", key=f"del_{i}"):
                st.session_state["destinations"].pop(i)
                st.rerun()

    if st.button("🗑️ Clear All"):
        st.session_state["destinations"] = []
        st.session_state["optimization_result"] = None
        st.session_state["csv_processed"] = False
        st.session_state["last_csv_signature"] = None
        st.session_state["csv_uploader_key"] += 1
        st.rerun()

    st.divider()

    if st.button("🚀 Optimize Route", type="primary"):
        if not valid_src:
            st.error("Invalid source city")
        elif not st.session_state["destinations"]:
            st.error("Add at least one destination")
        else:
            payload = {
                "source": {
                    "id": source_input.lower().replace(" ", "_"),
                    "name": source_input,
                    "lat": src_lat,
                    "lon": src_lon
                },
                "destinations": st.session_state["destinations"],
                "vehicle_speed_kmh": 60
            }

            with st.spinner("🤖 Optimizing..."):
                try:
                    res = requests.post(API_URL, json=payload, timeout=60)
                    if res.status_code == 200:
                        st.session_state["optimization_result"] = res.json()
                    else:
                        st.error(res.text)
                except Exception as e:
                    st.error(f"Optimization failed: {e}")

# ===================== MAIN OUTPUT =====================
result = st.session_state["optimization_result"]

if result is None:
    # Show onboarding steps until user runs optimization
    show_how_to_use()
else:
    # RESULTS VIEW
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Distance", f"{result['total_distance_km']} km")
    c2.metric("Total Time", f"{result['total_time_hours']} hrs")
    c3.metric("Solver", result["solver_used"])

    # Summary (already generated by backend)
    st.subheader("📝 AI Summary")
    st.write(result["summary"])
    st.divider()
    st.subheader("📄 Route Report")

    if st.button("📥 Generate & Download PDF"):
        report_payload = {
            "summary": result["summary"],
            "schedule": result["schedule"],
            "solver_used": result["solver_used"],
            "total_distance_km": result["total_distance_km"],
            "total_time_hours": result["total_time_hours"]
        }

        with st.spinner("📄 Generating report..."):
            try:
                res = requests.post(REPORT_API_URL, json=report_payload, timeout=30)
                if res.status_code == 200:
                    st.download_button(
                        label="⬇️ Download Route Report (PDF)",
                        data=res.content,
                        file_name="route_report.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("❌ Report generation failed")
            except Exception as e:
                st.error(f"Report generation failed: {e}")

    col1, col2 = st.columns([2, 1])

    # Schedule panel
    with col2:
        st.subheader("📋 Schedule")
        # schedule_df = pd.DataFrame(result["schedule"])

        # # Map deadlines from destinations
        # deadline_map = {
        #     d["id"]: d["deadline_hours"]
        #     for d in st.session_state["destinations"]
        # }

        # def compute_deadline_miss(row):
        #     stop_id = row["stop_id"]
        #     arrival = row["arrival_time"]
        #     if stop_id not in deadline_map:
        #         return 0.0
        #     deadline = deadline_map[stop_id]
        #     return round(max(0, arrival - deadline), 2)

        # if not schedule_df.empty:
        #     schedule_df["deadline_missed_hrs"] = schedule_df.apply(compute_deadline_miss, axis=1)
        #     st.dataframe(schedule_df)
        # else:
        #     st.write("No schedule available.")
        schedule_df = pd.DataFrame(result["schedule"])

        # ---------- deadline map (same as before) ----------
        deadline_map = {d["id"]: d["deadline_hours"] for d in st.session_state["destinations"]}

        def compute_deadline_miss(row):
            stop_id = row["stop_id"]
            arrival = row["arrival_time"]  # hours (backend returns hours)
            if stop_id not in deadline_map:
                return 0.0
            return round(max(0, arrival - deadline_map[stop_id]), 2)

        # compute and attach (keeps original numeric columns for logic)
        schedule_df["deadline_missed_hrs"] = schedule_df.apply(compute_deadline_miss, axis=1)

        # ---------- Make a display copy and rename columns to show units ----------
        display_df = schedule_df.rename(columns={
            "arrival_time": "arrival_time (hours)",
            "departure_time": "departure_time (hours)",
            "deadline_missed_hrs": "deadline_missed (hours)"
        })

        # round numeric columns for clean UI
        for col in ["arrival_time (hours)", "departure_time (hours)", "deadline_missed (hours)"]:
            if col in display_df.columns:
                display_df[col] = pd.to_numeric(display_df[col], errors="coerce").round(2)

        # Optionally reorder columns for nicer presentation
        cols = ["stop_id", "stop_name", "arrival_time (hours)", "departure_time (hours)", "deadline_missed (hours)", "lat", "lon", "status"]
        display_cols = [c for c in cols if c in display_df.columns]
        display_df = display_df[display_cols]

        st.dataframe(display_df)    

    # Map panel
    with col1:
        st.subheader("🗺️ Route Map")
        route_coords = [
            [s.get("lat", 0), s.get("lon", 0)]
            for s in result.get("schedule", [])
            if s.get("lat", 0) != 0 and s.get("lon", 0) != 0
        ]

        if not route_coords:
            st.info("No valid coordinates available to render map.")
        else:
            try:
                m = folium.Map(location=route_coords[0], zoom_start=5)
                total_stops = len(result["schedule"])

                for idx, s in enumerate(result["schedule"]):
                    lat, lon = s.get("lat", 0), s.get("lon", 0)
                    if lat == 0 or lon == 0:
                        continue

                    if idx == 0:
                        color, icon = "red", "play"                 # SOURCE
                    elif idx == total_stops - 1:
                        color, icon = "red", "flag-checkered"       # END
                    else:
                        color, icon = "blue", "truck"               # DELIVERY

                    folium.Marker(
                        [lat, lon],
                        popup=f"{idx}. {s.get('stop_name', '')}",
                        icon=folium.Icon(color=color, icon=icon, prefix="fa")
                    ).add_to(m)

                folium.PolyLine(route_coords, weight=5, color="blue").add_to(m)
                st_folium(m, width=800, height=500)
            except Exception as e:
                st.error(f"Failed to render map: {e}")
# build dataframe from API response (keep this for computations)

