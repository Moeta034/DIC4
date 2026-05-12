import streamlit as st
import sqlite3
import pandas as pd
import time

st.set_page_config(page_title="AIoT Dashboard", layout="wide")
st.title("ESP32 Sensor Dashboard")

DB_NAME = 'aiotdb.db'

def load_data():
    try:
        conn = sqlite3.connect(DB_NAME)
        query = "SELECT timestamp, temp, humd, device_id, ip_address FROM sensors ORDER BY id DESC LIMIT 100"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
        return df
    except Exception as e:
        return pd.DataFrame()

# placeholder for auto-refresh
placeholder = st.empty()

while True:
    df = load_data()
    
    with placeholder.container():
        if df.empty:
            st.warning("No data available yet. Waiting for ESP32 simulator...")
        else:
            latest = df.iloc[-1]
            avg_temp = df['temp'].mean()
            avg_humd = df['humd'].mean()
            
            # KPIs
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Latest Temperature", f"{latest['temp']} °C")
            col2.metric("Latest Humidity", f"{latest['humd']} %")
            col3.metric("Average Temp", f"{avg_temp:.1f} °C")
            col4.metric("Average Humidity", f"{avg_humd:.1f} %")
            
            st.markdown("---")
            
            # Charts
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Temperature Trend")
                st.line_chart(df.set_index('timestamp')['temp'], color="#FF5733")
            with c2:
                st.subheader("Humidity Trend")
                st.line_chart(df.set_index('timestamp')['humd'], color="#33C1FF")
                
            st.markdown("---")
            st.subheader("Recent Data (Table)")
            st.dataframe(df.sort_values('timestamp', ascending=False).head(10), use_container_width=True)
            
    time.sleep(2)
