import streamlit as st
import pandas as pd
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
display_cols = ["road", "yard", "status", "train", "type", "operator", "arrival", "departure", "length", "capacity"]
styled = df[display_cols].style.map(style_status, subset=["status"])
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
    arrival = st.text_input("Arrival time")
    departure = st.text_input("Departure time")
    submitted = st.form_submit_button("Find suitable roads")

    if submitted and train:
      st.session_state.pending_train = {
        "train": train,
        "operator": operator,
        "type": train_type,
        "length": int(length),
        "arrival": arrival,
        "departure": departure
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
                "type": pending["type'],
                "length": pending["length"],
                "arrival": pending["arrival"],
                "depareture": pending["departure"]
              })
              st.session_state.movements.append(
                f"{datetime.now():%D-%m-%y %H:%M} - ALLOCATE {train} TO {road_name}"
              )
              st.success(f"Allocated {pending['train']} to {road_name}")
              # clear the pending data
              del st.sessions_state.pending_train
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

  st.subheader("Recent Movements")
  if st.session_state.movements:
    for m in reversed(st.session_state.movements[-15:]):
      st.text(m)
  else: 
    st.info("No movements yet")

st.caption("Session data only - refresh resets the yard. Proper save comes next.")
st.subheader("Statistics")
#Your show_statistics logic goes here
