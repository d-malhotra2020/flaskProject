from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

def get_first_digit(number):
    while number >= 10:
        number = number // 10
    return number

def benford_law(data):
    observed = [get_first_digit(number) for number in data]
    expected = [np.log10(1 + 1 / d) for d in range(1, 10)]
    return observed, expected

def validate_benford(observed, expected):
    chi_squared = sum((o - e) ** 2 / e for o, e in zip(observed, expected))
    p_value = 1 - chi_squared
    return p_value

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        column_name = request.form['column_name']
        if file:
            try:
                df = pd.read_csv(file)
                data = df[column_name].dropna().astype(int).tolist()
                observed, expected = benford_law(data)
                p_value = validate_benford(observed, expected)

                plt.bar(range(1, 10), observed, label='Observed', alpha=0.7)
                plt.plot(range(1, 10), expected, 'r-', label='Expected')
                plt.xlabel('First Digit')
                plt.ylabel('Frequency')
                plt.legend()
                plt.title('Benford\'s Law Analysis')

                plt.savefig('static/plot.png')  # Save the plot as an image
                plt.close()

                return render_template('result.html', p_value=p_value)

            except Exception as e:
                return render_template('index.html', error=str(e))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)