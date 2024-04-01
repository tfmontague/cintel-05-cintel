from shiny import App, reactive, render
from shiny.express import ui
import random
from datetime import datetime
from collections import deque
import pandas as pd
import plotly.express as px

UPDATE_INTERVAL_SECS: int = 1

# Initialize a reactive deque to store the most recent 5 temperature records
temp_records = reactive.Value(deque(maxlen=5))

@reactive.calc()
def reactive_calc_combined():
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)
    temp = round(random.uniform(-18, -16), 1)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_record = {"temp": temp, "timestamp": timestamp}
    # Append new_record to the deque, automatically maintains the most recent 5 entries
    temp_records().append(new_record)
    # Immediately convert to DataFrame for rendering
    df = pd.DataFrame(list(temp_records()), columns=["temp", "timestamp"])
    return df

def display_temperature_chart():
    df = reactive_calc_combined()
    fig = px.line(df, x='timestamp', y='temp', markers=True)
    fig.update_traces(line_color='aqua', marker=dict(color='aqua', size=10))  # Customize line and marker color
    fig.update_layout(plot_bgcolor='#444', paper_bgcolor='#444', font_color='aqua')  # Customize background and font color
    return fig

ui.page_opts(title="PyShiny Express: Live Data (Basic)", fillable=True)

# Original UI layout and style setup
ui.HTML("""
<style>
  body {
    background-color: #E0FFFF;
    color: #333;
  }
</style>
""")

# Sidebar setup
with ui.sidebar():
    with ui.card(style="background-color: #444; color: white; margin-bottom: 20px;"):
        ui.h2("Antarctic Explorer", class_="text-center", style="color: aqua;")
    with ui.card(style="background-color: #444; color: white; margin-bottom: 20px;"):
        ui.p("A demonstration of real-time temperature readings in Antarctica.", class_="text-center", style="color: aqua;")
    with ui.card(style="background-color: #444; color: white; margin-bottom: 20px;"):
        ui.card_header("Additional Details and References:", style="background-color: #555; color: aqua;")
        ui.hr(style="border-top: 1px solid #777;")
        ui.h6("Links:", style="color: aqua;")
        ui.a("GitHub Source", href="https://github.com/denisecase/cintel-05-cintel-basic", target="_blank", style="color: #1E90FF;")
        ui.a("GitHub App", href="https://denisecase.github.io/cintel-05-cintel-basic/", target="_blank", style="color: #1E90FF;")
        ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank", style="color: #1E90FF;")

# Main layout with "Current Temperature" and "Current Date and Time" cards
with ui.layout_columns():
    with ui.card(style="background-color: #444; color: white; margin-bottom: 10px;"):
        ui.card_header("Current Temperature", style="background-color: #555; color: aqua; padding: 10px;")
        @render.ui()
        def display_temp():
            latest_dictionary_entry = reactive_calc_combined().iloc[-1]
            return ui.HTML(f'<div style="font-size: xxx-large; font-weight: bold; color: aqua;">{latest_dictionary_entry["temp"]} C</div>')

    with ui.card(style="background-color: #444; color: white; margin-bottom: 10px;"):
        ui.card_header("Current Date and Time", style="background-color: #555; color: aqua; padding: 10px;")
        @render.ui()
        def display_time():
            latest_dictionary_entry = reactive_calc_combined().iloc[-1]
            return ui.HTML(f'<div style="font-size: xxx-large; font-weight: bold; color: aqua;">{latest_dictionary_entry["timestamp"]}</div>')

# Updated "Current Data" section with the dynamic/reactive data grid
with ui.layout_columns():
    with ui.card(style="background-color: #444; color: white;"):
        ui.card_header("Last 5 Recorded Temperatures and Associated Time Stamps", style="background-color: #555; color: aqua;")
        @render.ui()
        def display_recent_temps2():
            title_html = ui.HTML('<h3 style="color: aqua;">Last 5 Recorded Temperatures and Associated Time Stamps</h3>')
            return reactive_calc_combined()

# Updated "Current Chart" card 
    with ui.layout_columns():
        with ui.card(style="background-color: #444; color: white;"):
            ui.card_header("Temperature Over Time (5 most recent data points)", style="background-color: #555; color: aqua;")
            @render.ui()
            def render_chart():
                # Generate the Plotly figure
                fig = display_temperature_chart()
                # Convert the Plotly figure to HTML for rendering in Shiny
                # Use the full_html=False option to generate a div without the full HTML document structure
                return ui.HTML(fig.to_html(full_html=False))
 

