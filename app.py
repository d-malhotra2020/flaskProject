from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        target_column = request.form.get('target_column')
        if file and target_column:
            try:
                df = pd.read_csv(file)
                if target_column in df.columns:
                    observed_data = df[target_column].dropna()
                    if len(observed_data) > 0:
                        observed_distribution = calculate_distribution(observed_data)
                        expected_distribution = calculate_benford_distribution()
                        plot_graph(observed_distribution, expected_distribution)
                        return render_template('result.html')
                    else:
                        return "No data found in the target column."
                else:
                    return "Target column not found in the file."
            except Exception as e:
                return str(e)
        else:
            return "Please provide a file and a target column."
    return render_template('index.html')

def calculate_distribution(data):
    first_digits = data.astype(str).str[0].astype(int)
    distribution = pd.Series(np.log10(1 + 1 / first_digits.value_counts(normalize=True)), index=range(1, 10))
    return distribution

def calculate_benford_distribution():
    benford_distribution = pd.Series(np.log10(1 + 1 / np.arange(1, 10)), index=range(1, 10))
    return benford_distribution

def plot_graph(observed_distribution, expected_distribution):
    plt.bar(observed_distribution.index, observed_distribution.values, alpha=0.5, color='b', label='Observed')
    plt.plot(expected_distribution.index, expected_distribution.values, 'ro-', label='Expected')
    plt.xlabel('First Digit')
    plt.ylabel('Frequency (log scale)')
    plt.yscale('log')
    plt.title('Benford\'s Law Validation')
    plt.legend()
    plt.savefig('static/result.png')
    plt.close()

if __name__ == '__main__':
    app.run(debug=True)
