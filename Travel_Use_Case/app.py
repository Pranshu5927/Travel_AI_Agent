import streamlit as st
from itinerary import generate_itinerary

st.set_page_config(page_title="Travel AI Agent")

st.title("Travel Itinerary Generator")

# User Inputs
destination = st.text_input("Enter destination")
days = st.number_input("Number of days", min_value=1, max_value=30, value=3)
budget = st.text_input("Budget (optional)")

# Button
if st.button("Generate Itinerary"):
    if destination:
        with st.spinner("Planning your trip... ✈️"):
            itinerary = generate_itinerary(destination, days, budget)
        
        st.subheader("📍 Your Itinerary")
        st.write(itinerary)
    else:
        st.warning("Please enter a destination")