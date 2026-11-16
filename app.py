import streamlit as st
import json

st.set_page_config(page_title="TYD Stabling", layout="wide")
st.title("TYD Stabling")

#We'll load your roads data and functions here
#for now this is the shell

if "roads" not in st.session_state:
  st.session_state.roads = [] #we'll replace this with your actual data

st.subheader("Roads")
#Table display goes here next

st.subheader("Statistics")
#Your show_statistics logic goes here
