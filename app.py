from flask import Flask, render_template, jsonify
from src.detection import EvolutionSimulation
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

simulation = None
sim_thread = None

def run_simulation():
    while True:
        try:
            simulation.run_generation()
            time.sleep(1)
        except Exception as e:
            logging.error(f"Error in simulation: {e}")

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/simulation')
def start_simulation():
    global simulation, sim_thread
    if simulation is None:
        simulation = EvolutionSimulation()
        sim_thread = threading.Thread(target=run_simulation)
        sim_thread.daemon = True
        sim_thread.start()
    return render_template('simulation.html')

@app.route('/spectator-data')
def get_spectator_data():
    try:
        return simulation.spectator.get_spectator_data()
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(
        debug=True,
        use_reloader=False
    ) 