from flask import Flask, jsonify, render_template

# Create Flask App
app = Flask(__name__)

# Define API endpoint
@app.route('/api/data', methods=['GET'])
def get_data():
    # Perform any backend logic here
    data = {'message': 'Hello, World!'}

    # Return the response as JSON
    return jsonify(data)


@app.route('/')
def index():
    return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run()