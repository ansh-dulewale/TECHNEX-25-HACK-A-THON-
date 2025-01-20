import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Template
import os

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

# Set up the database
engine = create_engine('sqlite:///data/traffic_data.db')

# Define and store data
data = {
    'timestamp': pd.to_datetime(['2023-01-01 00:00:00', '2023-01-01 01:00:00']),
    'location': ['Intersection 1', 'Intersection 1'],
    'vehicle_count': [100, 150],
    'average_speed': [30, 25]
}
df = pd.DataFrame(data)
df.to_sql('traffic_data', engine, if_exists='replace', index=False)

# Load data from the database
df = pd.read_sql('traffic_data', engine)

# Perform data analysis
avg_vehicle_count = df['vehicle_count'].mean()
peak_times = df.groupby(df['timestamp'].dt.hour)['vehicle_count'].sum().idxmax()
print(f'Average Vehicle Count: {avg_vehicle_count}')
print(f'Peak Traffic Time: {peak_times}:00')

# Ensure the plots directory exists
os.makedirs('plots', exist_ok=True)

# Visualize data
plt.figure(figsize=(10, 6))
sns.lineplot(x='timestamp', y='vehicle_count', data=df)
plt.title('Vehicle Count Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Vehicle Count')
plt.savefig('plots/vehicle_count_plot.png')
plt.show()

plt.figure(figsize=(10, 6))
sns.lineplot(x='timestamp', y='average_speed', data=df)
plt.title('Average Speed Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Average Speed (km/h)')
plt.savefig('plots/average_speed_plot.png')
plt.show()

# Generate report
template = Template('''
<html>
<head><title>Traffic Data Report</title></head>
<body>
    <h1>Traffic Data Report</h1>
    <p>Average Vehicle Count: {{ avg_vehicle_count }}</p>
    <p>Peak Traffic Time: {{ peak_times }}:00</p>
    <img src="plots/vehicle_count_plot.png" alt="Vehicle Count Over Time">
    <img src="plots/average_speed_plot.png" alt="Average Speed Over Time">
</body>
</html>
''')
report_html = template.render(avg_vehicle_count=avg_vehicle_count, peak_times=peak_times)
with open('traffic_data_report.html', 'w') as f:
    f.write(report_html)