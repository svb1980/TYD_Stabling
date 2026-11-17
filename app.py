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

def style_status(val):
  if val == "Occupied":
    return "background-colour: #ffccc; colour: #990000; font-weight: bold"
  elif val == "Reserved":
    return "background-colour: #ff3cd; colour: #856404; font-weight: bold"
  elif val == "Booked Out":
    return "background-colour: #e9ecef; colour: #495057; font-weight: bold"
  else:
    return "background-colour: #d4edda; colour: #155724; font-weight: bold"

#Sidebar
st.sidebar.header("Actions")
action = st.sidebar.selectbox(
  "What do you want to do?",
  ["View Yard", "Stable Train", "Remove / Depart Train", "Book Out / Return Road", "Reserve Road", "Statistics & Reports"]
)

roads = st.session_state.roads

#Yard table with coloured status
df = pd.DataFrame(roads)
display_cols = ["road", "yard", "status", "train", "type", "operator", "num_locos", "locomotives", "wagons", "arrival", "departure", "length", "capacity"]
styled = df[display_cols].style.applymap(style_status, subset=["status"])
st.subheader("Current Yard")
st.dataframe(styled, use_container_width=True, hide_index=True)

#Actions
if action == "Stable Train":
  st.subheader("Stable a Train")
  
  with st.form("stable_form"):
    train = st.text_input("Train ID")
    operator = st.text_input("Operator")
    train_type = st.selectbox("Type", ["Intermodal", "Grain", "Steel", "Container", "Ballast", "Infrastructure", "Locomotive", "Other"])
    length = st.number_input("Length (m)", min_value=1, value=1)
    num_locomotives = st.text_input("Number of Locomotives", min_value=1, value=1)
    locomotives = st.text_input("Locomotive number(s)")
    num_wagons = st.text_input("Number of wagons", min_value=0, value=0)

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
      
      st.session_state.pending_train = {
        "train": train,
        "operator": operator,
        "type": train_type,
        "length": int(length),
        "num_locomotives": int(num_locos),
        "locomotives": Locomotives,
        "num_wagons": int(num_wagons),
        "arrival": arrival_str,
        "departure": departure_str
      }
      suitable = [r for r in roads if r ["status"] == "Empty" and r["capacity"] >= length]
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
          road_name = chosen.split(" - ")[1].split(' (')[0]
          for road in st.session_state.roads:
            if road["road"] == road_name:
              road.update({
                "status": "Occupied",
                "train": pending["train"],
                "operator": pending["operator"],
                "type": pending["type"],
                "length": pending["length"],
                "num_locomotives": pending["num_locos"],
                "locomotives": pending["Locomotives"],
                "num_wagons": pending["num_wagons"],
                "arrival": pending["arrival"],
                "departure": pending["departure"]
              })
              st.session_state.movements.append(
                f"{datetime.now():%d-%m-%Y %H:%M} - ALLOCATED {pending['train']} TO {road_name}"
              )
              st.success(f"Allocated {pending['train']} to {road_name}")
              del st.session_state.pending_train
              if "suitable_roads" in st.session_state:
                del st.session_state.suitable_roads
              st.rerun()

elif action == "Remove / Depart Train":
  st.subheader("Remove or Depart a Train")
  occupied = [r for r in roads if r["status"] == "Occupied" and r["train"]]
  if occupied:
    train_ids = [r["train"] for r in occupied]
    selected = st.selectbox("Select train", train_ids)
    if st.button("Remove / Depart"):
      for road in roads:
        if road["train"] == selected:
          road.update({"status": "Empty", "train": "", "operator": "", "type": "", "length": 0, "arrival": "", "departure": ""})
          st.session_state.movements.append(f"{datetime.now():%D-%m-%y %H:%M} - DEPARTED {selected} FROM {road['road']}")
          st.success(f"{selected} cleared")
          st.rerun()
    else:
      st.info("No trains currently stabled")

elif action == "Book Out / Return Road":
  st.subheader("Book Out or Return a Road")
  road_names = [r["road"] for r in roads]
  selected_road = st.selectbox("Road", road_names)
  col1, col2 = st.columns(2)
  if col1.button("Book Out"):
    for road in roads:
      if road["road"] == selected_road:
        road["status"] = "Empty"
        road["train"] = ""
        st.session_state.movements.append(f"{datetime.now():%D-%m-%y %H:%M} - BOOKED OUT {selected_road}")
        st.rerun()
  if col2.button("Return to Service"):
    for road in roads:
      if road["reoad"] == selected_road:
        road["status"] = "Empty"
        road["train"] = ""
        st.session_state.movements.append(f"{datetime.now():%D-%m-%y %H:%M} - RETURNED {selected_road}")
        st.rerun()

elif action == "Reserve Road":
  st.subheader("Reserve a Road")
  road_names = [r["road"] for r in roads if r["status"] == "Empty"]
  if road_names:
    selected_road = st.selectbox("Emptyroad", road_names)
    train = st.text_input("Reserved for train")
    if st.button("Reserve") and train:
      for road in roads:
        if road["road"] == selected_road:
          road["status"] = "Reserved"
          road["train"] = train
          st.session_state.movements.append(f"{datetime.now():%D-%m-%y %H:%M} - RESERVED {selected_road} FOR {train}")
          st.rerun()
  else:
    st.info("No empty roads available")

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
  length_util = round((occupied_length / total_capcity) * 100) if total_capacity else 0
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
