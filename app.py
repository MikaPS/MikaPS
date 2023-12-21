from flask import Flask, jsonify
import language_use  # This is the script we created earlier
import matplotlib.pyplot as plt
app = Flask(__name__)

@app.route('/chart-data')
def chart_data():
    data = language_use.get_language_data()
    return jsonify(data)

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>Language Chart</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <canvas id="myChart" width="400" height="400"></canvas>
        <script>
            fetch('/chart-data')
                .then(response => response.json())
                .then(data => {
                    let labels = [];
                    let percentages = [];
                    const ctx = document.getElementById('myChart').getContext('2d');
                    data.forEach((l) => {
                        labels.push(l[0]);
                        percentages.push(l[1]);
                    });
                    new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'Languages',
                                data: percentages,
                                backgroundColor: ['orange', 'red', 'purple', 'blue', 'green']  
                            }]
                        },
                    });
                    
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        </script>
    </body>
    </html>
    '''
@app.route('/chart-image')
def chart_image():
    data = language_use.get_language_data()

    labels = [label[0] for label in data] 
    percentages = [percentage[1] for percentage in data] 

    plt.figure(figsize=(6, 6))
    bars = plt.bar(range(len(labels)), percentages, color=['orange', 'red', 'purple', 'blue', 'green'])

    # Add labels on the bars
    for i, bar in enumerate(bars):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 3, f"{percentages[i]}%", ha='center', color='white', fontsize=12)

    # Set x-axis ticks and labels
    plt.xticks(range(len(labels)), labels)

    plt.title('Language Distribution')
    plt.ylabel('Percentage (%)')
    plt.xlabel('Languages')

    # Save the figure
    plt.tight_layout()
    plt.savefig('chart-image.png')
    return 'Chart image generated'

if __name__ == '__main__':
    app.run(debug=True)
