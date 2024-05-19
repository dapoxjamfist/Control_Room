from flask import Flask, render_template, request, send_from_directory, jsonify
import subprocess
import os

app = Flask(__name__)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to serve video files
@app.route('/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory('static/videos', filename)

# Route to get video path based on coordinates
@app.route('/coordinates_video', methods=['POST'])
def get_coordinates_video():
    coordinates = request.json.get('coordinates')
    video_path = os.path.join('static/videos', coordinates, 'video1.mp4')
    return jsonify({'video_path': video_path})

# Route to run the Python script and get the output video path
@app.route('/detect', methods=['POST'])
def detect():
    data = request.get_json()
    coordinates_folder = data.get('coordinatesFolder')

    # Path to the script
    script_path = os.path.join('static/videos', coordinates_folder, 'main.py')
    
    # Run the Python script
    try:
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500

    # Assuming the output video is stored in the same folder
    output_video_path = os.path.join('/videos', coordinates_folder, 'output.mp4')

    # Verify if the output video exists
    if not os.path.exists(output_video_path):
        return jsonify({'error': 'Output video not found'}), 404

    return jsonify({'outputVideoPath': output_video_path})

if __name__ == '__main__':
    app.run(debug=True)
