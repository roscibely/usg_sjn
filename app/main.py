import streamlit as st
import pandas as pd
from io import BytesIO

def shortest_job_next_usg(processes):

    n = len(processes)
    time = [0] * n
    waiting_time = [0] * n
    urgency_factor = [0] * n
    seriousness_factor = [0] * n
    growth_factor = [0] * n
    cost_factor = [0] * n

    for i in range(n):
        time[i] = processes[i][1]
        urgency_factor[i] = processes[i][2]
        seriousness_factor[i] = processes[i][3]
        growth_factor[i] = processes[i][4]
        cost_factor[i] = processes[i][5] # added variable PHAB

    total_waiting_time = 0

    # Sort processes based on the urgency-seriousness-growth (USG) method
    processes.sort(key=lambda x: (-x[2], -x[3], -x[4], x[1], x[5]))

    # Calculate waiting time for each process
    for i in range(n):
        waiting_time[i] = total_waiting_time
        total_waiting_time += time[i]
    average_waiting_time = sum(waiting_time) / n

    data = []
    for id, time, urgency_factor, seriousness_factor, growth_factor, cost_factor in processes:
        data.append({
          'task': id,
          'time': time,
          'urgency': urgency_factor,
          'seriousness': seriousness_factor,
          'growth': growth_factor,
          'cost': cost_factor
      })
    data_ = pd.DataFrame(data)
    return data_

# Set the title of the web app
st.title("Urgency-Seriousness-Growth  based on Shortest Job Next ")

# Create a file uploader widget
uploaded_file = st.file_uploader("Upload an .xlsx file", type=["xlsx"])

# Check if a file has been uploaded
if uploaded_file is not None:
    # Execute your custom function on the uploaded file
    uploaded_file= pd.read_excel(uploaded_file)
    result_df = shortest_job_next_usg(uploaded_file.values.tolist())

    # Display the result DataFrame
    st.write("Result DataFrame:")
    st.write(result_df)

    # Allow the user to download the result as an XLSX file
    result_bytes = BytesIO()
    with pd.ExcelWriter(result_bytes, engine="xlsxwriter", mode="xlsx") as writer:
        result_df.to_excel(writer, sheet_name="Result", index=False)
    result_bytes.seek(0)

    st.markdown("### Download Result")
    st.markdown(
        "Click the link below to download the result as an XLSX file:"
    )

    st.download_button(
        label="Download Result",
        data=result_bytes,
        file_name="result.xlsx",
        key="download_result",
    )

# Provide some instructions to the user
st.markdown("### Instructions:")
st.markdown("1. Click the 'Browse...' button above to upload an XLSX file.")
st.markdown("2. The result will be displayed below, and you can download it as an XLSX file.")

