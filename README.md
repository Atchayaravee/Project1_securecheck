# 🚨 SecureCheck

**SecureCheck** is an interactive data analysis and visualization dashboard built with **Streamlit**, **MySQL**, and **Python (Pandas)**.
It helps law enforcement agencies, analysts, or researchers monitor, analyze, and detect patterns in traffic stop activities — including searches, arrests, and violations — to ensure accountability, improve efficiency, and gain actionable insights.

---

## 📂 Dataset

* **traffic\_stops.sql** – Cleaned database dump file (use to create the MySQL database `traffic_stops`)
* **traffic\_stops.csv** – Original raw data (uncleaned)

---

## 📁 Project Structure

Police\_SecureCheck/
├── DB_clean&sqlcon.ipynb  # Notebook for cleaning and preprocessing
├── ps_sl_conn.py  # Main Streamlit dashboard app
├── requirements.txt  # Python dependencies
├── traffic\_stops.sql  # Cleaned SQL database dump
├── traffic\_stops.csv  # Raw CSV data
└── README.md  # Project documentation


## ⚙️ Set Up Virtual Environment

python -m venv env
# Activate the environment
# On Windows:
.\\venv\\Scripts\\activate


## 📦 Install Dependencies


pip install -r requirements.txt


## 🗄️ Set Up MySQL Database

1. Create a database named `traffic_stops` in your MySQL server.
2. Import the `traffic_stops.sql` file to load the cleaned data.

Example:

```bash
mysql -u root -p traffic_stops < traffic_stops.sql
```

Update your MySQL credentials in your `streamlitapp.py` if needed:

```python
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='YOUR_PASSWORD',
    database='traffic_stops'
)
```

## ▶️ Run the Streamlit App


streamlit run streamlitapp.py
```

## 🙋‍♂️ Author

Atchaya Raveendran

## 📜 License

This project is licensed under the MIT License.
