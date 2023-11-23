import streamlit as st
import pandas as pd

import fastf1
import fastf1.plotting
import GettingData
import matplotlib.pyplot as plt

st.title("Fast F1 Dashboard")
grand_prix = st.selectbox('Which GP would you like to view data for?', (GettingData.getGPList()))
st.pyplot(GettingData.getTrackPlot(grand_prix))
st.table(GettingData.getSessionResultsDf(grand_prix))
st.pyplot(GettingData.getPlotForDrivers(grand_prix))
st.pyplot(GettingData.getQualifyingPlot(grand_prix))
driver = st.selectbox('Which driver data would you like to see?', (GettingData.getDriverList(grand_prix)))
st.pyplot(GettingData.getDriverLapTimePlot(grand_prix, driver))