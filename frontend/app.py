import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from folium import plugins
import pandas as pd
import difflib

# CONFIG
API_URL = "http://127.0.0.1:8000/optimize"

# --- EXPANDED CITY DATABASE (Prevents "Mathura" -> "Madurai" errors) ---
INDIAN_CITIES = [
    # Tier 1
    "Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Surat",
    
    # Tier 2
    "Pune", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal", 
    "Visakhapatnam", "Pimpri-Chinchwad", "Patna", "Vadodara", "Ghaziabad", "Ludhiana", 
    "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot", "Kalyan-Dombivli", "Vasai-Virar", 
    "Varanasi", "Srinagar", "Aurangabad", "Dhanbad", "Amritsar", "Navi Mumbai", "Prayagraj", 
    "Howrah", "Ranchi", "Jabalpur", "Gwalior", "Coimbatore", "Vijayawada", "Jodhpur", 
    "Madurai", "Raipur", "Kota", "Guwahati", "Chandigarh", "Solapur", "Hubli–Dharwad", 
    "Tiruchirappalli", "Tiruppur", "Moradabad", "Mysore", "Bareilly", "Gurgaon", "Aligarh", 
    "Jalandhar", "Bhubaneswar", "Salem", "Mira-Bhayandar", "Warangal", "Thiruvananthapuram", 
    "Guntur", "Bhiwandi", "Saharanpur", "Gorakhpur", "Bikaner", "Amravati", "Noida", 
    "Jamshedpur", "Bhilai", "Cuttack", "Firozabad", "Kochi", "Nellore", "Bhavnagar", 
    "Dehradun", "Durgapur", "Asansol", "Nanded", "Kolhapur", "Ajmer", "Kalaburagi", 
    "Jamnagar", "Ujjain", "Loni", "Siliguri", "Jhansi", "Ulhasnagar", "Jammu", 
    "Sangli-Miraj & Kupwad", "Mangalore", "Erode", "Belgaum", "Ambattur", "Tirunelveli", 
    "Malegaon", "Gaya", "Jalgaon", "Udaipur", "Maheshtala", "Davanagere", "Kozhikode", 
    "Kurnool", "Akola", "Rajpur Sonarpur", "Rajahmundry", "Bokaro", "South Dumdum", 
    "Bellary", "Patiala", "Gopalpur", "Agartala", "Bhagalpur", "Muzaffarnagar", "Bhatpara", 
    "Panihati", "Latur", "Dhule", "Tirupati", "Rohtak", "Korba", "Bhilwara", "Berhampur", 
    "Muzaffarpur", "Ahmednagar", "Mathura", "Kollam", "Avadi", "Kadapa", "Kamarhati", 
    "Bilaspur", "Shahjahanpur", "Bijapur", "Rampur", "Shivamogga", "Chandrapur", "Junagadh", 
    "Thrissur", "Alwar", "Bardhaman", "Kulti", "Kakinada", "Nizamabad", "Parbhani", "Tumkur", 
    "Khammam", "Ozhukarai", "Bihar Sharif", "Panipat", "Darbhanga", "Bally", "Aizawl", 
    "Dewas", "Ichalkaranji", "Karnal", "Bathinda", "Jalna", "Eluru", "Kirari Suleman Nagar", 
    "Barasat", "Purnia", "Satna", "Mau", "Sonipat", "Farrukhabad", "Sagar", "Rourkela", 
    "Durg", "Imphal", "Ratlam", "Hapur", "Arrah", "Karimnagar", "Anantapur", "Etawah", 
    "Ambarnath", "North Dumdum", "Bharatpur", "Begusarai", "New Delhi", "Gandhidham", 
    "Baranagar", "Tiruvottiyur", "Pondicherry", "Sikar", "Thoothukudi", "Rewa", "Mirzapur", 
    "Raichur", "Pali", "Ramagundam", "Silchar", "Haridwar", "Vizianagaram", "Tenali", 
    "Nagercoil", "Sri Ganganagar", "Karawal Nagar", "Mango", "Thanjavur", "Bulandshahr", 
    "Uluberia", "Murwara", "Sambhal", "Singrauli", "Nadiad", "Secunderabad", "Naihati", 
    "Yamunanagar", "Bidhan Nagar", "Pallavaram", "Bidar", "Munger", "Panchkula", "Burhanpur", 
    "Raurkela Industrial Township", "Kharagpur", "Dindigul", "Gandhinagar", "Hospet", 
    "Nangloi Jat", "Malda", "Ongole", "Deoghar", "Chapra", "Haldia", "Khandwa", "Nandyal", 
    "Chittoor", "Morena", "Amroha", "Anand", "Bhind", "Bhalswa Jahangir Pur", "Madhyamgram", 
    "Bhiwani", "Navi Mumbai Panvel Raigad", "Baharampur", "Ambala", "Morvi", "Fatehpur", 
    "Rae Bareli", "Khora", "Bhusawal", "Orai", "Bahraich", "Vellore", "Mahesana", "Sambalpur", 
    "Raiganj", "Sirsa", "Danapur", "Serampore", "Sultan Pur Majra", "Guna", "Jaunpur", 
    "Panvel", "Shivpuri", "Surendranagar Dudhrej", "Unnao", "Hugli and Chinsurah", "Alappuzha", 
    "Kottayam", "Machilipatnam", "Shimla", "Adoni", "Udupi", "Katihar", "Proddatur", 
    "Mahbubnagar", "Saharsa", "Dibrugarh", "Jorhat", "Hazaribagh", "Hindupur", "Nagaon", 
    "Hajipur", "Sasaram", "Giridih", "Bhimavaram", "Kumbakonam", "Bongaigaon", "Dehri", 
    "Madanapalle", "Siwan", "Bettiah", "Ramgarh", "Tinsukia", "Guntakal", "Srikakulam", 
    "Motihari", "Dharmavaram", "Gudivada", "Phagwara", "Pudukkottai", "Hosur", "Narasaraopet", 
    "Suryapet", "Miryalaguda", "Tadipatri", "Karaikudi", "Kishanganj", "Jamalpur", "Ballia", 
    "Kavali", "Tadepalligudem", "Amaravati", "Buxar", "Tezpur", "Jehanabad", "Aurangabad", 
    "Gangtok", "Vasco Da Gama"
]

def correct_spelling(city_name):
    """
    Smart Auto-Correct:
    1. Returns exact match if exists.
    2. Returns fuzzy match ONLY if similarity > 80% (Prevents Mathura->Madurai).
    3. Returns original input if uncertain.
    """
    if not city_name: return city_name
    
    clean_input = city_name.strip()
    
    # 1. Exact Match (Case Insensitive)
    city_map = {c.lower(): c for c in INDIAN_CITIES}
    if clean_input.lower() in city_map:
        return city_map[clean_input.lower()]

    # 2. Fuzzy Match (Strict Cutoff 0.8)
    # This prevents "Mathura" (M...a) matching "Madurai" (M...a) loosely
    matches = difflib.get_close_matches(clean_input, INDIAN_CITIES, n=1, cutoff=0.8)
    
    if matches:
        return matches[0]
    
    # 3. No confident match? Trust the user!
    return clean_input

st.set_page_config(page_title="Flipr Logistics AI", layout="wide")

# --- SESSION STATE ---
if 'destinations' not in st.session_state:
    st.session_state['destinations'] = []
if 'optimization_result' not in st.session_state:
    st.session_state['optimization_result'] = None

st.title("🚛 AI-Powered Route Optimizer")

# --- SIDEBAR ---
with st.sidebar:
    st.header("1. Configuration")
    source_input = st.text_input("Source City", "Delhi")
    source_name = correct_spelling(source_input)
    
    # Show feedback on source name
    if source_name != source_input and source_name.lower() != source_input.lower():
        st.caption(f"✨ Auto-corrected to: **{source_name}**")
    elif source_name not in INDIAN_CITIES and source_input:
        st.caption(f"⚠️ Unknown city. Using raw input.")

    st.divider()
    st.header("2. Add Destination")
    
    new_city_input = st.text_input("City Name")
    
    c1, c2 = st.columns(2)
    with c1:
        new_priority = st.selectbox("Priority", [1, 2, 3], index=2, help="1=Urgent")
    with c2:
        new_deadline = st.number_input("Deadline (Hrs)", min_value=1.0, value=24.0, step=1.0, format="%.1f")
        
    if st.button("➕ Add Stop"):
        if new_city_input:
            final_name = correct_spelling(new_city_input)
            target_id = final_name.lower().replace(" ", "_")
            
            # --- DUPLICATE CHECK LOGIC ---
            # Check if this ID already exists in our list
            existing_idx = -1
            for i, d in enumerate(st.session_state['destinations']):
                if d['id'] == target_id:
                    existing_idx = i
                    break
            
            if existing_idx != -1:
                # UPDATE existing entry
                st.session_state['destinations'][existing_idx]['priority'] = new_priority
                st.session_state['destinations'][existing_idx]['deadline_hours'] = new_deadline
                st.warning(f"⚠️ City '{final_name}' already exists! Updated with new settings.")
            else:
                # ADD new entry
                st.session_state['destinations'].append({
                    "id": target_id,
                    "name": final_name,
                    "priority": new_priority,
                    "deadline_hours": new_deadline,
                    "service_time_minutes": 30
                })
                
                if final_name != new_city_input:
                    st.info(f"✨ Auto-corrected '{new_city_input}' -> '{final_name}'")
                else:
                    st.success(f"Added {final_name}")
        else:
            st.error("Please enter a city name")

    st.divider()
    st.header("3. Manage Stops")
    
    if st.session_state['destinations']:
        for i, dest in enumerate(st.session_state['destinations']):
            c_name, c_del = st.columns([3, 1])
            with c_name:
                st.write(f"**{i+1}. {dest['name']}** (P{dest['priority']}, {dest['deadline_hours']}h)")
            with c_del:
                if st.button("❌", key=f"del_{i}"):
                    st.session_state['destinations'].pop(i)
                    st.session_state['optimization_result'] = None
                    st.rerun()
        
        if st.button("🗑️ Clear All"):
            st.session_state['destinations'] = []
            st.session_state['optimization_result'] = None
            st.rerun()

    st.divider()
    if st.button("🚀 Optimize Route", type="primary"):
        if not st.session_state['destinations']:
            st.error("Add at least one destination!")
        else:
            payload = {
                "source": {"id": source_name.lower(), "name": source_name},
                "destinations": st.session_state['destinations'],
                "vehicle_speed_kmh": 60.0
            }
            
            with st.spinner("🤖 AI is finding the best route..."):
                try:
                    response = requests.post(API_URL, json=payload)
                    if response.status_code == 200:
                        st.session_state['optimization_result'] = response.json()
                    else:
                        st.error(f"API Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")

# --- MAIN DISPLAY ---
result = st.session_state['optimization_result']

if result:
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Distance", f"{result['total_distance_km']} km")
    c2.metric("Total Duration", f"{result['total_time_hours']} hrs")
    c3.metric("Solver", result['solver_used'])
    
    st.success(f"📝 {result['summary']}")

    col_map, col_table = st.columns([2, 1])

    with col_table:
        st.subheader("📍 Schedule")
        display_data = []
        for item in result['schedule']:
            # Warn if late
            warning = "⚠️" if "LATE" in item.get('status', '') else ""
            display_data.append({
                "Stop": f"{item['stop_name']} {warning}", 
                "Arr": f"{item['arrival_time']:.2f} h",
                "Dep": f"{item['departure_time']:.2f} h"
            })
        st.dataframe(pd.DataFrame(display_data), hide_index=True)

    with col_map:
        st.subheader("🗺️ Live Map")
        if result['schedule']:
            start_lat = result['schedule'][0].get('lat', 20.59)
            start_lon = result['schedule'][0].get('lon', 78.96)
            
            m = folium.Map(location=[start_lat, start_lon], zoom_start=5)
            
            route_coords = []
            for idx, item in enumerate(result['schedule']):
                lat, lon = item.get('lat', 0), item.get('lon', 0)
                if lat == 0 and lon == 0: continue
                
                route_coords.append([lat, lon])
                
                color = "red" if idx == 0 or idx == len(result['schedule'])-1 else "blue"
                if "LATE" in item.get('status', ''): color = "orange"
                
                folium.Marker(
                    location=[lat, lon],
                    popup=f"{idx}. {item['stop_name']}",
                    icon=folium.Icon(color=color, icon="truck", prefix="fa")
                ).add_to(m)
            
            # --- DRAW PATH WITH ARROWS ---
            # 1. Draw the main blue line
            path_line = folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.8).add_to(m)
            
            # 2. Add directional arrows using PolyLineTextPath
            plugins.PolyLineTextPath(
                path_line,
                "      ➤      ", # Arrow symbol with padding for spacing
                repeat=True,
                offset=7,       # Center alignment adjustment
                attributes={'fill': '#0000FF', 'font-weight': 'bold', 'font-size': '24'}
            ).add_to(m)
            # -----------------------------

            st_folium(m, width=800, height=500)