import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Simple password gate
def check_password():
  def password_entered():
    if st.session_state["password"] == "MArS1SpA":
      st.session_state["password_correct"] = True
      del st.session_state["password"]
    else:
      st.session_state["password_correct"] = False

  if "password_correct" not in st.session_state:
    st.text_input("Password", type="password", on_change=password_entered, key="password")
    return False
  elif not st.session_state["password_correct"]:
    st.text_input("Password", type="password", on_change=password_entered, key="password")
    st.error("Incorrect password")
    return False
  else:
    return True

if not check_password():
  st.stop()

st.set_page_config(page_title="TYD Stabling", layout="wide")
st.title("Tottenham Freight Yard - Stabling")

#Default roads (your original data)
DEFAULT_ROADS=[
  {"road": "A/D Road", "yard": "Arrival/Departure", "status": "Empty", "train": "", "operator": "", "type": "", "length": 0, "arrival": "", "departure": "", "capacity": 1500},
  {"road":"East 1","yard":"East Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":369},
  {"road":"East 2","yard":"East Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":369},
  {"road":"East 3","yard":"East Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":967},
  {"road":"East 4","yard":"East Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":995},
  {"road":"East 5","yard":"East Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":1067},
  {"road":"West 3","yard":"West Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":1231},
  {"road":"West 4","yard":"West Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":1200},
  {"road":"West 5","yard":"West Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":1196},
  {"road":"West 6","yard":"West Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":1207},
  {"road":"1st Class 9","yard":"1st Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":421},
  {"road":"1st Class 10","yard":"1st Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":387},
  {"road":"1st Class 11","yard":"1st Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":357},
  {"road":"2nd Class 14","yard":"2nd Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":435},
  {"road":"2nd Class 15","yard":"2nd Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":414},
  {"road":"2nd Class 16","yard":"2nd Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":388},
  {"road":"2nd Class 17","yard":"2nd Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":357},
  {"road":"2nd Class 18","yard":"2nd Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":335},
  {"road":"2nd Class 19","yard":"2nd Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":304},
]

if "roads" not in st.session_state:
  st.session_state.roads = [r.copy() for r in DEFAULT_ROADS]
if "movements" not in st.session_state:
  st.session_state.movements = []

# Persistent confirmation message
if "action_message" in st.session_state:
  st.success(st.session_state.action_message)
  del st.session_state.action_message

#Sidebar
st.sidebar.header("Actions")
action = st.sidebar.selectbox(
  "What do you want to do?",
  ["View Yard", "Stable Train", "Remove / Depart Train", "Book Out / Return Road", "Reserve Road", "Unreserve Road", "Maintenance Lock", "Statistics & Reports"]
)

roads = st.session_state.roads

# Yard table with visible status indicators
df = pd.DataFrame(st.session_state.roads)

def add_status_icon(status):
    status = str(status)
    if status == "Occupied":
        return "🔴 Occupied"
    elif status == "Reserved":
        return "🟡 Reserved"
    elif status == "Booked Out":
        return "⚪ Booked Out"
    elif status == "Empty":
        return "🟢 Empty"
    elif status == "Maintenance":
        return "🔧 Maintenance"
    elif status == "Occupation":
        return "🚧 Occupation"
    return status

if "status" in df.columns:
    df["status"] = df["status"].apply(add_status_icon)

wanted = ["road", "yard", "status", "train", "type", "operator", "num_locos", "locomotives", "wagons", "loaded", "arrival", "departure", "length", "capacity"]
display_cols = [c for c in wanted if c in df.columns]

st.subheader("Current Yard")
st.dataframe(df[display_cols], use_container_width=True, hide_index=True)

#Actions
if action == "Stable Train":
  st.subheader("Stable a Train")
  
  with st.form("stable_form"):
    train = st.text_input("Train ID")
    operator = st.text_input("Operator")
    train_type = st.selectbox("Type", ["Intermodal", "Grain", "Steel", "Container", "Ballast", "Infrastructure", "Locomotive", "Other"])
    length = st.number_input("Length (m)", min_value=1, value=1200)
    num_locomotives = st.number_input("Number of Locomotives", min_value=1, value=1)
    locomotive_number = st.text_input("Locomotive Number")
    num_wagons = st.number_input("Number of wagons", min_value=0, value=0)
    loaded = st.checkbox("Wagons are loaded", value=True)

    col1, col2 = st.columns(2)
    with col1:
      arrival_date = st.date_input("Arrival date")
      arrival_time = st.time_input("Arrival time")
    with col2:
      departure_date = st.date_input("Departure date")
      departure_time = st.time_input("Departure time")
    
    submitted = st.form_submit_button("Find suitable roads")

    if submitted and train:
      arrival_str = f"{arrival_date.strftime('%d-%m-%Y')} {arrival_time.strftime('%H:%M')}"
      departure_str = f"{departure_date.strftime('%d-%m-%Y')} {departure_time.strftime('%H:%M')}"
      
      st.session_state.pending_train = {
        "train": train,
        "operator": operator,
        "type": train_type,
        "length": int(length),
        "num_locomotives": int(num_locomotives),
        "locomotive_number": locomotive_number,
        "num_wagons": int(num_wagons),
        "loaded": loaded,
        "arrival": arrival_str,
        "departure": departure_str
      }
      suitable = [r for r in st.session_state.roads if r ["status"] == "Empty" and r["capacity"] >= length]
      suitable.sort(key=lambda x: x["capacity"])
      st.session_state.suitable_roads = suitable

    if "pending_train" in st.session_state and st.session_state.pending_train:
      pending = st.session_state.pending_train
      suitable = st.session_state.get("suitable_roads", [])

      if not suitable:
        st.error("No suitable empty roads")
      else:
        road_options = [f"{r['yard']} - {r['road']} ({r['capacity']}m)" for r in suitable]
        chosen = st.selectbox("Allocate to", road_options)
        if st.form_submit_button("Confirm allocation"):
          road_name = chosen.split(" - ")[1].split(" (")[0]
          for road in st.session_state.roads:
            if road["road"] == road_name:
              road.update({
                "status": "Occupied",
                "train": pending["train"],
                "operator": pending["operator"],
                "type": pending["type"],
                "length": pending["length"],
                "num_locomotives": pending["num_locomotives"],
                "locomotive_number": pending["locomotive_number"],
                "num_wagons": pending["num_wagons"],
                "loaded": pending["loaded"],
                "arrival": pending["arrival"],
                "departure": pending["departure"]
              })
              st.session_state.movements.append(
                f"{datetime.now():%d-%m-%Y %H:%M} - ALLOCATED {pending['train']} TO {road_name}"
              )
              st.session_state.action_message = f"Train {pending['train']} allocated to {road_name}"
              st.rerun()

elif action == "Remove / Depart Train":
    st.subheader("Remove or Depart a Train")
    
    occupied = [
        r for r in st.session_state.roads 
        if "Occupied" in str(r.get("status", "")) and r.get("train")
    ]
    
    if not occupied:
        st.info("No trains currently stabled")
    else:
        train_ids = [r["train"] for r in occupied]
        selected = st.selectbox("Select train to remove", train_ids)
        
        if st.button("Remove / Depart", type="primary"):
            for road in st.session_state.roads:
                if road.get("train") == selected:
                    road.update({
                        "status": "Empty",
                        "train": "",
                        "operator": "",
                        "type": "",
                        "length": 0,
                        "num_locos": 0,
                        "locomotives": "",
                        "wagons": 0,
                        "loaded": False,
                        "arrival": "",
                        "departure": ""
                    })
                    st.session_state.movements.append(
                        f"{datetime.now():%Y-%m-%d %H:%M} — DEPARTED {selected} FROM {road['road']}"
                    )
                    st.session_state.action_message = f"{selected} removed from {road['road']}"
                    st.rerun()

elif action == "Book Out / Return Road":
  st.subheader("Book Out or Return a Road")
  road_names = [r["road"] for r in st.session_state.roads]
  selected_road = st.selectbox("Select road", road_names)
  
  col1, col2 = st.columns(2)
  
  if col1.button("Book Out", type="primary"):
    for road in st.session_state.roads:
      if road["road"] == selected_road:
        road["status"] = "Booked Out"
        road["train"] = ""
        road["operator"] = ""
        road["type"] = ""
        road["length"] = 0
        road["num_locomotives"] = 0
        road["locomotive nbumber"] = ""
        road["num_wagons"] = 0
        road["loaded"] = False
        road["arrival"] = ""
        road["departure"] = ""
        st.session_state.movements.append(
          f"{datetime.now():%D-%m-%y %H:%M} - BOOKED OUT {selected_road}"
        )
        st.session_state.action_message = f"{selected_road} booked out"
        st.rerun()
        
  if col2.button("Return to Service"):
    for road in st.session_state.roads:
      if road["road"] == selected_road:
        road["status"] = "Empty"
        road["train"] = ""
        road["operator"] = ""
        road["type"] = ""
        road["length"] = 0
        road["num_locomotives"] = 0
        road["locomotive nbumber"] = ""
        road["num_wagons"] = 0
        road["loaded"] = False
        road["arrival"] = ""
        road["departure"] = ""
        st.session_state.movements.append(
          f"{datetime.now():%D-%m-%y %H:%M} - RETURNED {selected_road} TO SERVICE"
        )
        st.session_state.action_message = f"{selected_road} returned to service"
        st.rerun()
        
elif action == "Reserve Road":
    st.subheader("Reserve a Road")
    
    # Show confirmation if we just reserved something
    if "reserve_message" in st.session_state:
        st.success(st.session_state.reserve_message)
        del st.session_state.reserve_message
    
    empty_roads = [
        r for r in st.session_state.roads 
        if str(r.get("status", "")).replace("🟢 ", "").strip() == "Empty"
    ]
    
    if not empty_roads:
        st.warning("No empty roads available")
    else:
        with st.form("reserve_form"):
            road_options = [f"{r['yard']} — {r['road']} ({r['capacity']}m)" for r in empty_roads]
            chosen = st.selectbox("Road to reserve", road_options)
            train = st.text_input("Train ID")
            operator = st.text_input("Operator")
            train_type = st.selectbox("Type", ["Intermodal", "Grain", "Steel", "Container", "Ballast", "Infrastructure", "Locomotive", "Other"])
            length = st.number_input("Length (m)", min_value=1, value=400)
            num_locos = st.number_input("Number of locomotives", min_value=0, value=1)
            locomotives = st.text_input("Locomotive number(s)")
            wagons = st.number_input("Number of wagons", min_value=0, value=0)
            loaded = st.checkbox("Wagons are loaded", value=True)
            
            col1, col2 = st.columns(2)
            with col1:
                arrival_date = st.date_input("Expected arrival date")
                arrival_time = st.time_input("Expected arrival time")
            with col2:
                indefinite = st.checkbox("Departure indefinite / unknown")
                if not indefinite:
                    departure_date = st.date_input("Expected departure date")
                    departure_time = st.time_input("Expected departure time")
            
            submitted = st.form_submit_button("Reserve road")
        
        if submitted and train and chosen:
            road_name = chosen.split(" — ")[1].split(" (")[0]
            arrival_str = f"{arrival_date.strftime('%d-%m-%Y')} {arrival_time.strftime('%H:%M')}"
            departure_str = "Indefinite" if indefinite else f"{departure_date.strftime('%d-%m-%Y')} {departure_time.strftime('%H:%M')}"
            
            for road in st.session_state.roads:
                if road["road"] == road_name:
                    road.update({
                        "status": "Reserved",
                        "train": train,
                        "operator": operator,
                        "type": train_type,
                        "length": int(length),
                        "num_locos": int(num_locos),
                        "locomotives": locomotives,
                        "wagons": int(wagons),
                        "loaded": loaded,
                        "arrival": arrival_str,
                        "departure": departure_str
                    })
                    st.session_state.movements.append(
                        f"{datetime.now():%Y-%m-%d %H:%M} — RESERVED {road_name} FOR {train}"
                    )
                    st.session_state.action_message = f"Road {road_name} successfully reserved for {train}"
                    st.rerun()

elif action == "Unreserve Road":
    st.subheader("Unreserve a Road")
    
    reserved = [
        r for r in st.session_state.roads 
        if "Reserved" in str(r.get("status", ""))
    ]
    
    if not reserved:
        st.info("No roads are currently reserved")
    else:
        road_options = [f"{r['yard']} — {r['road']} ({r.get('train', 'No train')})" for r in reserved]
        chosen = st.selectbox("Select reserved road", road_options)
        
        if st.button("Unreserve", type="primary"):
            road_name = chosen.split(" — ")[1].split(" (")[0]
            for road in st.session_state.roads:
                if road["road"] == road_name:
                    road.update({
                        "status": "Empty",
                        "train": "",
                        "operator": "",
                        "type": "",
                        "length": 0,
                        "num_locos": 0,
                        "locomotives": "",
                        "wagons": 0,
                        "loaded": False,
                        "arrival": "",
                        "departure": ""
                    })
                    st.session_state.movements.append(
                        f"{datetime.now():%Y-%m-%d %H:%M} — UNRESERVED {road_name}"
                    )
                    st.session_state.action_message = f"{road_name} has been unreserved"
                    st.rerun()

elif action == "Maintenance Lock":
    st.subheader("Maintenance / Occupation Lock")
    st.caption("Override for project managers and rail safety representatives")
    
    # --- Apply Lock ---
    available = [
        r for r in st.session_state.roads 
        if r.get("status") not in ["Maintenance", "Occupation"]
    ]
    
    if not available:
        st.info("All roads are already under maintenance or occupation lock")
    else:
        road_options = [f"{r['yard']} — {r['road']}" for r in available]
        chosen = st.selectbox("Select road to lock", road_options, key="lock_road")
        lock_type = st.radio("Lock type", ["Maintenance", "Occupation"])
        reason = st.text_input("Reason / Works description")
        locked_by = st.text_input("Locked by (name)")
        
        road_name_to_lock = chosen.split(" — ")[1] if chosen else ""
        verify_lock = st.text_input(f"Type the road name to confirm lock: {road_name_to_lock}")
        
        if st.button("Apply Lock", type="primary"):
            if verify_lock.strip() != road_name_to_lock:
                st.error("Verification failed. Road name does not match.")
            elif not locked_by:
                st.error("Please enter who is applying the lock.")
            else:
                for road in st.session_state.roads:
                    if road["road"] == road_name_to_lock:
                        road.update({
                            "status": lock_type,
                            "train": "",
                            "operator": "",
                            "type": "",
                            "length": 0,
                            "num_locos": 0,
                            "locomotives": "",
                            "wagons": 0,
                            "loaded": False,
                            "arrival": "",
                            "departure": "",
                            "lock_reason": reason,
                            "locked_by": locked_by
                        })
                        st.session_state.movements.append(
                            f"{datetime.now():%Y-%m-%d %H:%M} — {lock_type.upper()} LOCK ON {road_name_to_lock} by {locked_by}"
                        )
                        st.session_state.action_message = f"{road_name_to_lock} locked for {lock_type}"
                        st.rerun()
    
    st.divider()
    
    # --- Remove Lock ---
    st.subheader("Remove Lock")
    locked = [
        r for r in st.session_state.roads 
        if r.get("status") in ["Maintenance", "Occupation"]
    ]
    
    if not locked:
        st.info("No roads currently locked")
    else:
        locked_options = [f"{r['yard']} — {r['road']} ({r['status']})" for r in locked]
        to_unlock = st.selectbox("Select locked road", locked_options, key="unlock_road")
        road_name_to_unlock = to_unlock.split(" — ")[1].split(" (")[0] if to_unlock else ""
        verify_unlock = st.text_input(f"Type the road name to confirm unlock: {road_name_to_unlock}")
        
        if st.button("Remove Lock"):
            if verify_unlock.strip() != road_name_to_unlock:
                st.error("Verification failed. Road name does not match.")
            else:
                for road in st.session_state.roads:
                    if road["road"] == road_name_to_unlock:
                        road["status"] = "Empty"
                        road["lock_reason"] = ""
                        road["locked_by"] = ""
                        st.session_state.movements.append(
                            f"{datetime.now():%Y-%m-%d %H:%M} — LOCK REMOVED FROM {road_name_to_unlock}"
                        )
                        st.session_state.action_message = f"Lock removed from {road_name_to_unlock}"
                        st.rerun()

elif action == "Statistics & Reports":
  st.subheader("Yard Statistics")
  total = len(roads)
  occupied = sum(1 for r in roads if r["status"] == "Occupied")
  empty = sum(1 for r in roads if r["status"] == "Empty")
  booked = sum(1 for r in roads if r["status"] == "Booked Out")
  reserved = sum(1 for r in roads if r["status"] == "Reserved")
  util = round((occupied / total) * 100) if total else 0

  c1, c2, c3, c4, c5 = st.columns(5)
  c1.metric("Total Roads", total)
  c2.metric("Occupied", occupied)
  c3.metric("Empty", empty)
  c4.metric("Booked Out", booked)
  c5.metric("Utilisation", f"{util}%")

  st.divider()

  # Length utilisatrion
  occupied_length = sum(r["length"] for r in roads if r["status"] == "Occupied")
  total_capacity = sum(r["capacity"] for r in roads)
  length_util = round((occupied_length / total_capacity) * 100) if total_capacity else 0
  st.metric("Length Utilisation", f"{length_util}%", f"{occupied_length}m / {total_capacity}m")

  st.divider()

  # Operator summary
  st.subheader("Operator Summary")
  operators = {}
  for r in roads:
    if r.get("operator"):
      operators[r["operator"]] = operators.get(r["operator"], 0) + 1
  if operators:
    op_df = pd.DataFrame(list(operators.items()), columns=["Operator", "Trains"])
    st.dataframe(op_df, hide_index=True, use_container_width=True)
  else:
    st.info("No operators recorded")

  # Yard area summary
  st.subheader("Yard Area Summary")
  areas = {}
  for r in roads:
    yard = r["yard"]
    if yard not in areas:
      areas[yard] = {"occupied": 0, "total": 0}
    areas[yard]["total"] += 1
  area_df = pd.DataFrame([
    {"Yard": k, "Occupied": v["occupied"], "Total Roads": v["total"]}
    for k, v in areas.items()
  ])
  st.dataframe(area_df, hide_index=True, use_container_width=True)

  # Train type summary
  st.subheader("Train Type Summary")
  types = {}
  for r in roads:
    if r.get("type"):
      types[r["type"]] = types.get(r["type"], 0) + 1
    if types:
      type_df = pd.DataFrame(list(types.items()), columns=["Type", "Count"])
      st.dataframe(type_df, hide_index=True, use_container_width=True)
    else:
      st.info("No train types recorded")

  # Capacity hotspots
  st.subheader("Capacity Hotspots (80% or more)")
  hotspots = []
  for r in roads:
    if r["status"] == "Occupied" and r["capacity"] > 0:
      usage = round((r["length"] / r["capacity"]) * 100)
      if usage >= 80:
        hotspots.append({"Road": r["road"], "Train": r["train"], "Usage": f"{usage}%"})
  if hotspots:
    st.dataframe(pd.DataFrame(hotspots), hide_index=True, use_container_width=True)
  else:
      st.info("No roads at or above 80% capacity")

  # Empty roads
  st.subheader("Empty Roads")
  empty_roads = [{"Road": r["road"], "Yard": r["yard"], "Capacity": f"{r['capacity']}m"} for r in roads if r["status"] == "Empty"]
  if empty_roads:
    st.dataframe(pd.DataFrame(empty_roads), hide_index=True, use_container_width=True)
  else:
    st.info("No empty roads")

  st.divider()            
  st.subheader("Recent Movements")
  if st.session_state.movements:
    for m in reversed(st.session_state.movements[-15:]):
      st.text(m)
  else: 
    st.info("No movements yet")

st.divider()
st.subheader("Save / Load Yard")

col1, col2 = st.columns(2)

with col1:
  yard_json = json.dumps(st.session_state.roads, indent=2)
  st.download_button(
    label="Download yard data",
    data=yard_json,
    file_name="yard_data.json",
    mime="application/json"
  )

with col2:
  uploaded = st.file_uploader("Upload yard data", type="json")
  if uploaded is not None:
    try:
      loaded = json.load(uploaded)
      st.session_state.roads = loaded
      st.success("Yard data loaded")
      st.rerun()
    except Exception as e:
      st.error("Could not load file")
st.caption("Session data only - refresh resets the yard. Proper save comes next.")
