from io import BytesIO
import base64
import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
import numpy as np

from flask import Flask, render_template_string, request

app = Flask("Yelptestapp")

db_params = {
    'dbname': 'testyelp',
    'user': 'postgres',
    'password': '123456789',
    'host': 'database-1.ccpdrtqkicjw.us-east-1.rds.amazonaws.com',
    'port': 5432
}

def get_db_connection():
    return psycopg2.connect(**db_params)

@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT DISTINCT city FROM sample ORDER BY city;')
    unique_cities = cur.fetchall()
    cur.execute('SELECT DISTINCT state FROM sample ORDER BY state;')
    unique_states = cur.fetchall()

    cur.close()
    conn.close()

    city_options = ''.join(f"<option value=\"{city[0]}\">{city[0]}</option>" for city in unique_cities)
    state_options = ''.join(f"<option value=\"{state[0]}\">{state[0]}</option>" for state in unique_states)
    return render_template_string('''<!DOCTYPE html>
<html>
<head>
    <title>Yelp Insights App</title>
</head>
<body>
    <h1>Select Your Attributes For the Yelp Analysis!</h1>
    <form action="/submit" method="post">
        <label for="city">Choose a City:</label>
        <select name="city" id="city">
            <option value="">Select City</option>
            ''' + city_options + '''
        </select>
        <label for="state">Choose a State:</label>
        <select name="state" id="state">
            <option value="">Select State</option>
            ''' + state_options + '''
        </select>
        <!-- Your other attributes here -->
        <input type="submit" value="Submit">
        <div><label><input type="checkbox" name="WheelchairAccessible" value="true"> Wheelchair Accessible</label></div>
        <div><label><input type="checkbox" name="BusinessAcceptsCreditCards" value="true"> Accepts Credit Cards</label></div>
        <div><label><input type="checkbox" name="RestaurantsReservations" value="true"> Accepts Reservations</label></div>
        <div><label><input type="checkbox" name="RestaurantsPriceRange2" value="true"> Price Range $$</label></div>
        <div><label><input type="checkbox" name="ByAppointmentOnly" value="true"> By Appointment Only</label></div>
        <div><label><input type="checkbox" name="HappyHour" value="true"> Happy Hour</label></div>
        <div><label><input type="checkbox" name="RestaurantsTakeOut" value="true"> Accept Take Out</label></div>
        <div><label><input type="checkbox" name="GoodForKids" value="true"> Good For Kids</label></div>
        <div><label><input type="checkbox" name="DogsAllowed" value="true"> Dogs Allowed</label></div>
        <div><label><input type="checkbox" name="BYOB" value="true"> Bring Your Own Bottle</label></div>
        <div><label><input type="checkbox" name="noise_loud" value="true"> Noise Loud</label></div>
        <div><label><input type="checkbox" name="noise_quiet" value="true"> Noise Quiet</label></div>
        <div><label><input type="checkbox" name="alcohol_beer_and_wine" value="true"> Beer and Wine</label></div>
        <div><label><input type="checkbox" name="alcohol_none" value="true"> No Alcohol</label></div>
        <input type="submit" value="Submit">
    </form>
</body>
</html>''')

@app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()
    filtered_df = process_form_data(form_data)
    insights = generate_insights(filtered_df)
    return render_template_string('''<!DOCTYPE html>
<html>
<head>
    <title>Analysis Results</title>
</head>
<body>
    <h1>Insights from Yelp Data</h1>

    <!-- Embed positive correlations plot -->
    <h2>Top 10 Positive Correlations with Average Sentiment</h2>
    <img src="data:image/png;base64,{{ insights['top_positive_correlations_plot'] }}" alt="Top 10 Positive Correlations">

    <!-- Embed negative correlations plot -->
    <h2>Top 10 Negative Correlations with Average Sentiment</h2>
    <img src="data:image/png;base64,{{ insights['top_negative_correlations_plot'] }}" alt="Top 10 Negative Correlations">
</body>
</html>''', insights=insights)

def process_form_data(form_data):
    where_clauses = []
    for attribute, value in form_data.items():
        if value == 'true':
            where_clauses.append(f"\"{attribute}\" = 1")
    where_clause = ' AND '.join(where_clauses) if where_clauses else 'TRUE'
    query = f"SELECT * FROM sample WHERE {where_clause};"

    conn = get_db_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
def generate_insights(df):
    df_numeric = df.select_dtypes(include=[np.number])

    insights = {}
    correlation_matrix = df_numeric.corr()
    correlation_with_sentiment = correlation_matrix['average_sentiment']
    correlation_with_sentiment = correlation_with_sentiment.drop(labels=['average_sentiment'])

    top_positive_correlations = correlation_with_sentiment.sort_values(ascending=False).head(10)
    top_negative_correlations = correlation_with_sentiment.sort_values(ascending=True).head(10)

    insights['top_positive_correlations_plot'] = create_plot(top_positive_correlations)
    insights['top_negative_correlations_plot'] = create_plot(top_negative_correlations, positive=False)

    return insights

def create_plot(correlations, positive=True):
    plt.figure(figsize=(10, 8))
    colors = 'green' if positive else 'red'
    plt.barh(correlations.index, correlations.values, color=colors)
    plt.xlabel('Correlation with Average Sentiment')
    title = 'Top 10 Positive Correlations' if positive else 'Top 10 Negative Correlations'
    plt.title(title)
    plt.gca().invert_yaxis()
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return img_base64

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)