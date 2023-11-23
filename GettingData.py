import pandas as pd

import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
from fastf1.core import Laps
from timple.timedelta import strftimedelta
from fastf1.ergast import Ergast
import seaborn as sns

def getGPList():
    ergast = Ergast()
    races = ergast.get_race_schedule(2023)
    listOfRaces = races['raceName']
    return listOfRaces

def getDriverList(grandPrix):
    session = fastf1.get_session(2023, grandPrix, 'R')
    session.load()
    results = session.results
    results = pd.DataFrame(results)
    return results['Abbreviation']
  
def getTrackPlot(grandPrix):
    session = fastf1.get_session(2023, grandPrix, 'R')
    session.load(weather=False)
    lap = session.laps.pick_fastest()
    # Get telemetry data
    x = lap.telemetry['X']
    y = lap.telemetry['Y']
    fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
    fig.suptitle(grandPrix, size=24, y=0.97)

    # Adjust margins and turn of axis
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
    ax.axis('off')

    ax.plot(lap.telemetry['X'], lap.telemetry['Y'], color='black', linestyle='-', linewidth=10, zorder=0)

    return fig

def getSessionResultsDf(grandPrix):
    session = fastf1.get_session(2023, grandPrix, 'R')
    session.load(telemetry=False, weather=False)
    results = session.results
    results_df = pd.DataFrame(results)
    results_df = results_df[["DriverNumber", "BroadcastName", "Abbreviation", "TeamName", "Position", "ClassifiedPosition", "GridPosition", "Status", "Points"]]
    results_df = results_df.astype(str)
    return results_df

def getPlotForDrivers(grandPrix):
    session = fastf1.get_session(2023, grandPrix, 'R')
    session.load(telemetry=False, weather=False)
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
    return fig

def getQualifyingPlot(grandPrix):
    qualifyingSession = fastf1.get_session(2023, grandPrix, 'Qualifying')
    qualifyingSession.load()
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False)
    drivers = pd.unique(qualifyingSession.laps['Driver'])

    list_fastest_laps = list()
    for drv in drivers:
        drvs_fastest_lap = qualifyingSession.laps.pick_driver(drv).pick_fastest()
        list_fastest_laps.append(drvs_fastest_lap)
    fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)

    pole_lap = fastest_laps.pick_fastest()
    fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']

    fastest_laps = fastest_laps[fastest_laps['Driver'].notna()]
    team_colors = list()
    for index, lap in fastest_laps.iterlaps():
        color = fastf1.plotting.team_color(lap['Team'])
        team_colors.append(color)

    fig, ax = plt.subplots()
    ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'],
        color=team_colors, edgecolor='grey')
    ax.set_yticks(fastest_laps.index)
    ax.set_yticklabels(fastest_laps['Driver'])

    # show fastest at the top
    ax.invert_yaxis()

    # draw vertical lines behind the bars
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)
    lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')

    plt.suptitle(f"{qualifyingSession.event['EventName']} {qualifyingSession.event.year} Qualifying\n"
             f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")
    return fig 

def getDriverLapTimePlot(grandPrix, driver):
    fastf1.plotting.setup_mpl(misc_mpl_mods=False)
    session = fastf1.get_session(2023, grandPrix, 'R')
    session.load()

    driver_laps = session.laps.pick_driver(driver).pick_quicklaps().reset_index()

    fig, ax = plt.subplots(figsize=(8, 8))

    # seems to be a problem her around data time casting
    sns.scatterplot(data=driver_laps,
                x="LapNumber",
                y="LapTime",
                ax=ax,
                hue="Compound",
                palette=fastf1.plotting.COMPOUND_COLORS,
                s=80,
                linewidth=0,
                legend='auto')
    
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time")

    # The y-axis increases from bottom to top by default
    # Since we are plotting time, it makes sense to invert the axis
    ax.invert_yaxis()
    plt.suptitle(f"{driver} lap times in the {grandPrix}")

    # Turn on major grid lines
    plt.grid(color='w', which='major', axis='both')
    sns.despine(left=True, bottom=True)

    plt.tight_layout()
    plt.show()
    return fig