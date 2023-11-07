import streamlit as st
import pandas as pd

import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt


session = fastf1.get_session(2023, 1, 'R')
session.load(telemetry=False, weather=False)
results = session.results
results_df = pd.DataFrame(results)
results_df = results_df.astype(str)

fig, ax = plt.subplots(figsize=(8.0, 4.9))

for drv in session.drivers:
    drv_laps = session.laps.pick_driver(drv)

    abb = drv_laps['Driver'].iloc[0]
    color = fastf1.plotting.driver_color(abb)

    ax.plot(drv_laps['LapNumber'], drv_laps['Position'],
            label=abb, color=color)
    
ax.set_ylim([20.5, 0.5])
ax.set_yticks([1, 5, 10, 15, 20])
ax.set_xlabel('Lap')
ax.set_ylabel('Position')

ax.legend(bbox_to_anchor=(1.0, 1.02))

st.title("Fast F1 Dashboard")
st.table(results_df)
st.pyplot(fig)
