import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px
 #Database connection
def create_connection():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='traffic_stops',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return None
# Fetch data from database
def fetch_data(query):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                df = pd.DataFrame(result)
                return df
        finally:
            connection.close()
    else:
        return pd.DataFrame()
    # Streamlit UI
st.set_page_config(
    page_title="🚓 SecureCheck: Police Vehicle Check Dashboard",
    layout="wide"
)

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #ffe6ea;
        background-image: radial-gradient(#f8bbd0 1px, transparent 1px);
        background-size: 20px 20px;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] {
        background: transparent;
    }

    [data-testid="stVerticalBlock"] {
        background: #ffffffbb;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    .stDataFrame, .stTable, iframe {
        background: #ffffffdd !important;
        border-radius: 12px !important;
        padding: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    h1, h2, h3, h4 {
        color: #880e4f;
    }

    button[kind="primary"] {
        border-radius: 8px !important;
    }

    .stTextInput > div > div,
    .stNumberInput > div,
    .stSelectbox > div,
    .stDateInput > div,
    .stTimeInput > div {
        border-radius: 8px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🚓 **SecureCheck: Police Vehicle Check Dashboard**")
st.markdown("Real-time **monitoring**, **queries**, and **insights** for law enforcement 🚔")


# Show full table
st.header("📋 **Police Logs Overview**")
query = "SELECT * FROM traffic_stops"
data = fetch_data(query)
st.dataframe(data, use_container_width=True)

# Charts section 
st.header("📊 **Visual Insights**")
tab1, tab2, tab3 = st.tabs(["Stops by Violation", "Driver Gender Distribution", "Driver Race Metrics"])

with tab1:
    if not data.empty and 'violation' in data.columns:
        violation_data = data['violation'].value_counts().reset_index()
        violation_data.columns = ['Violation', 'Count']
        fig = px.bar(
            violation_data,
            x='Violation',
            y='Count',
            title="🚦 Stops by Violation Type",
            color='Violation',
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for Violation chart.")

with tab2:
    if not data.empty and 'driver_gender' in data.columns:
        gender_data = data['driver_gender'].value_counts().reset_index()
        gender_data.columns = ['Gender', 'Count']
        fig = px.pie(
            gender_data,
            names='Gender',
            values='Count',
            title="🚻 Driver Gender Distribution",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for Driver Gender chart.")

with tab3:
    if not data.empty and 'driver_race' in data.columns:
        race_data = data['driver_race'].value_counts().reset_index()
        race_data.columns = ['Driver Race', 'Count']
        fig = px.bar(
            race_data,
            x='Driver Race',
            y='Count',
            title="🧑🏽‍🤝‍🧑🏾 Driver Race Metrics",
            color='Driver Race',
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for Driver Race chart.")

    # --- Advanced Queries ---
st.header("🧩 Advanced Insights")

selected_query = st.selectbox("**Select a Query to Run**", [
    "Top 10 vehicle numbers involved in drug-related stops",
    "Vehicles most frequently searched",
    "The driver age group which had the highest arrest rate",
    "Gender distribution of drivers that are stopped in each country",
    "The race and gender combination that has the highest search rate:",
    "The time of day that sees the most traffic stops",
    "The average stop duration for different violations",
    "Are stops during the night more likely to lead to arrests?",
    "Violations that are most associated with searches or arrests",
    "Violations that are most common among younger drivers (<25)",
    "Is there a violation that rarely results in search or arrest?",
    "Countries that report the highest rate of drug-related stops",
    "Arrest rate by country and violation",
    "Country that has the most stops with search conducted",
    "Yearly Breakdown of Stops and Arrests by Country",
    "Driver Violation Trends Based on Age and Race",
    "Time Period Analysis of Stops (Year, Month, Hour)",
    "Violations with High Search and Arrest Rates",
    "Driver Demographics by Country (Age, Gender, and Race)",
    "Top 5 Violations with Highest Arrest Rates"
])
query_map = {
    "Top 10 vehicle numbers involved in drug-related stops":"SELECT vehicle_number, COUNT(*) AS drug_stop_count FROM traffic_stops WHERE drugs_related_stop = 1 GROUP BY vehicle_number ORDER BY drug_stop_count DESC LIMIT 10;",
    "Vehicles most frequently searched":"SELECT vehicle_number, COUNT(*) AS search_count FROM traffic_stops WHERE search_conducted = 1 GROUP BY vehicle_number ORDER BY search_count DESC LIMIT 10;",
    "The driver age group which had the highest arrest rate":"SELECT CASE WHEN driver_age < 18 THEN 'Under 18' WHEN driver_age BETWEEN 18 AND 24 THEN '18-24' WHEN driver_age BETWEEN 25 AND 34 THEN '25-34' WHEN driver_age BETWEEN 35 AND 44 THEN '35-44' WHEN driver_age BETWEEN 45 AND 54 THEN '45-54' ELSE '55+' END AS age_group, COUNT(*) AS total_stops, SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS arrest_count, ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS arrest_rate FROM traffic_stops GROUP BY age_group ORDER BY arrest_rate DESC LIMIT 1;",
    "Gender distribution of drivers that are stopped in each country":"SELECT country_name, driver_gender, COUNT(*) AS stop_count FROM traffic_stops GROUP BY country_name, driver_gender ORDER BY country_name, driver_gender;",
    "The race and gender combination that has the highest search rate":"SELECT driver_race, driver_gender, COUNT(*) AS total_stops, SUM(search_conducted) AS searches, ROUND(SUM(search_conducted) * 100.0 / COUNT(*), 2) AS search_rate FROM traffic_stops GROUP BY driver_race, driver_gender ORDER BY search_rate DESC LIMIT 1;",
    "The time of day that sees the most traffic stops":"SELECT EXTRACT(HOUR FROM stop_time) AS hour_of_day, COUNT(*) AS stop_count FROM traffic_stops GROUP BY hour_of_day ORDER BY stop_count DESC LIMIT 1;",
    "The average stop duration for different violations":"SELECT violation, ROUND(AVG(stop_duration), 2) AS avg_duration FROM traffic_stops GROUP BY violation ORDER BY avg_duration DESC;",
    "Are stops during the night more likely to lead to arrests?":"SELECT CASE WHEN (SELECT SUM(is_arrested) FROM traffic_stops WHERE EXTRACT(HOUR FROM stop_time) BETWEEN 19 AND 23 OR EXTRACT(HOUR FROM stop_time) BETWEEN 0 AND 5) > (SELECT SUM(is_arrested) FROM traffic_stops WHERE EXTRACT(HOUR FROM stop_time) BETWEEN 6 AND 18) THEN 'Yes' ELSE 'No' END AS night_more_arrests;",
    "Violations that are most associated with searches or arrests":"SELECT violation, COUNT(*) AS total_stops, SUM(search_conducted) AS searches, SUM(is_arrested) AS arrests FROM traffic_stops GROUP BY violation ORDER BY searches + arrests DESC;",
    "Violations that are most common among younger drivers (<25)":"SELECT violation, COUNT(*) AS stop_count FROM traffic_stops WHERE driver_age < 25 GROUP BY violation ORDER BY stop_count DESC;",
    "Is there a violation that rarely results in search or arrest?":"SELECT CASE WHEN EXISTS (SELECT 1 FROM traffic_stops GROUP BY violation HAVING SUM(search_conducted) + SUM(is_arrested) < 0.05 * COUNT(*)) THEN 'Yes' ELSE 'No' END AS rarely_results_in_search_or_arrest;",
    "Countries that report the highest rate of drug-related stops":"SELECT country_name, COUNT(*) AS total_stops, SUM(drugs_related_stop) AS drug_stops, ROUND(SUM(drugs_related_stop) * 100.0 / COUNT(*), 2) AS drug_stop_rate FROM traffic_stops GROUP BY country_name ORDER BY drug_stop_rate DESC;",
    "Arrest rate by country and violation":"SELECT country_name, violation, COUNT(*) AS total_stops, SUM(is_arrested) AS arrests, ROUND(SUM(is_arrested) * 100.0 / COUNT(*), 2) AS arrest_rate FROM traffic_stops GROUP BY country_name, violation ORDER BY arrest_rate DESC;",
    "Country that has the most stops with search conducted":"SELECT country_name, COUNT(*) AS total_stops, SUM(search_conducted) AS search_stops FROM traffic_stops GROUP BY country_name ORDER BY search_stops DESC LIMIT 1;",
    "Yearly Breakdown of Stops and Arrests by Country":"SELECT DISTINCT country_name, year, COUNT(*) OVER (PARTITION BY country_name, year) AS total_stops, SUM(is_arrested) OVER (PARTITION BY country_name, year) AS arrests FROM (SELECT country_name, EXTRACT(YEAR FROM stop_date) AS year, is_arrested FROM traffic_stops) AS sub ORDER BY country_name, year;",
    "Driver Violation Trends Based on Age and Race":"SELECT a.driver_race, b.age_group, a.violation, COUNT(*) AS stop_count FROM traffic_stops a JOIN (SELECT id, CASE WHEN driver_age < 18 THEN 'Under 18' WHEN driver_age BETWEEN 18 AND 24 THEN '18-24' WHEN driver_age BETWEEN 25 AND 34 THEN '25-34' WHEN driver_age BETWEEN 35 AND 44 THEN '35-44' WHEN driver_age BETWEEN 45 AND 54 THEN '45-54' ELSE '55+' END AS age_group FROM traffic_stops) b ON a.id = b.id GROUP BY a.driver_race, b.age_group, a.violation ORDER BY a.driver_race, b.age_group, stop_count DESC;",
    "Time Period Analysis of Stops (Year, Month, Hour)":"SELECT a.year, a.month, a.hour, COUNT(*) AS stop_count FROM traffic_stops b JOIN (SELECT id, EXTRACT(YEAR FROM stop_date) AS year, EXTRACT(MONTH FROM stop_date) AS month, EXTRACT(HOUR FROM stop_time) AS hour FROM traffic_stops) a ON a.id = b.id GROUP BY a.year, a.month, a.hour ORDER BY a.year, a.month, a.hour;",
    "Violations with High Search and Arrest Rates":"SELECT DISTINCT violation, COUNT(*) OVER (PARTITION BY violation) AS total_stops, SUM(search_conducted) OVER (PARTITION BY violation) AS searches, SUM(is_arrested) OVER (PARTITION BY violation) AS arrests, ROUND(SUM(search_conducted) OVER (PARTITION BY violation) * 100.0 / COUNT(*) OVER (PARTITION BY violation), 2) AS search_rate, ROUND(SUM(is_arrested) OVER (PARTITION BY violation) * 100.0 / COUNT(*) OVER (PARTITION BY violation), 2) AS arrest_rate FROM traffic_stops ORDER BY search_rate DESC, arrest_rate DESC;",
    "Driver Demographics by Country (Age, Gender, and Race)":"SELECT country_name, driver_gender, driver_race, ROUND(AVG(driver_age), 1) AS avg_age, COUNT(*) AS stop_count FROM traffic_stops GROUP BY country_name, driver_gender, driver_race ORDER BY country_name, driver_gender, driver_race;",
    "Top 5 Violations with Highest Arrest Rates":"SELECT violation, COUNT(*) AS total_stops, SUM(is_arrested) AS arrests, ROUND(SUM(is_arrested) * 100.0 / COUNT(*), 2) AS arrest_rate FROM traffic_stops GROUP BY violation ORDER BY arrest_rate DESC LIMIT 5;"
}
if st.button("Run Query"):
    result = fetch_data(query_map[selected_query])
    if not result.empty:
        st.write(result)
    else:
        st.warning("No results found for the selected query.")

# 🔻 Divider and closing remark
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #004d40;'>🚓 Built with ❤️ to Empower Law Enforcement</h3>", unsafe_allow_html=True)

# 📝 Additional context heading
st.markdown(
    """
    <div style='background-color: #e0f7fa; padding: 15px; border-radius: 8px;'>
        <h4 style='color: #004d40;'>🔍 How it Works</h4>
        <p style='color: #004d40;'>
        Fill in the details below to simulate a traffic stop scenario. Our system will analyze the inputs and predict the most likely stop outcome and violation based on similar historical records.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Section heading
st.header("📝 **Add New Police Log & Predict Outcome**")

# Input form (unchanged)
with st.form("new_log_form"):
    stop_date = st.date_input("Stop Date")
    stop_time = st.time_input("Stop Time")
    country_name = st.text_input("Country Name")
    driver_gender = st.selectbox("Driver Gender", ["male", "female"])
    driver_age = st.number_input("Driver Age", min_value=16, max_value=100, value=27)
    driver_race = st.text_input("Driver Race")
    search_conducted = st.selectbox("Was a Search Conducted?", ["0", "1"])
    search_type = st.text_input("Search Type")
    drugs_related_stop = st.selectbox("Was it Drug Related?", ["0", "1"])
    stop_duration = st.selectbox("Stop Duration", data['stop_duration'].dropna().unique())
    vehicle_number = st.text_input("Vehicle Number")
    stop_datetime = pd.Timestamp.now()

    submitted = st.form_submit_button("🔎 Predict Stop Outcome & Violation")

    if submitted:
        # Filter data for prediction
        filtered_data = data[
            (data['driver_gender'] == driver_gender) &
            (data['driver_age'] == driver_age) &
            (data['search_conducted'] == int(search_conducted)) &
            (data['stop_duration'] == stop_duration) &
            (data['drugs_related_stop'] == int(drugs_related_stop))
        ]

        if not filtered_data.empty:
            predicted_outcome = filtered_data['stop_outcome'].mode()[0]
            predicted_violation = filtered_data['violation'].mode()[0]
        else:
            predicted_outcome = "warning"
            predicted_violation = "speeding"

        search_text = "A search was conducted" if int(search_conducted) else "No search was conducted"
        drug_text = "was drug-related" if int(drugs_related_stop) else "was not drug-related"

        st.markdown(
            f"""
            <div style='background-color: #f0f8ff; padding: 20px; border-radius: 8px; border: 2px solid #004d40;'>
                <h4 style='color: #004d40;'>✅ Prediction Summary</h4>
                <ul style='color: #004d40;'>
                    <li><strong>Predicted Violation:</strong> {predicted_violation}</li>
                    <li><strong>Predicted Stop Outcome:</strong> {predicted_outcome}</li>
                </ul>
                <p style='color: #004d40;'>
                🗒️ A {driver_age}-year-old {driver_gender} driver in {country_name} was stopped at {stop_time.strftime('%I:%M %p')} on {stop_date}.<br>
                {search_text}, and the stop {drug_text}.<br>
                Stop duration: <strong>{stop_duration}</strong>.<br>
                Vehicle Number: <strong>{vehicle_number}</strong>.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #004d40; font-size: 18px;'>
    👮‍♂️ <strong>Thank you for using SecureCheck!</strong><br>
    Stay vigilant. Drive safe. Support law enforcement.
</div>
""", unsafe_allow_html=True)



