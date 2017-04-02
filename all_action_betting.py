##### IMPORTS #####
import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__, static_url_path='')


##### Globals #####
BET_FILEPATH = 'test.txt'
SCORE_FILEPATH = 'score.txt'
heartbeat_time = time.time()


##### Routes #####
@app.route('/')
def root():
    return render_main_template()

@app.route('/place_bet.html')
def place_bet():
    return render_main_template()

@app.route('/set_bet_state', methods=['POST'])
def set_state():
    write_txt(BET_FILEPATH, request.form['button'])
    return render_main_template()

@app.route('/set_heartbeat_time', methods=['POST'])
def set_heartbeat_time():
    heartbeat_time = time.time()
    return render_main_template()

@app.route('/set_goal_state', methods=['POST'])
def set_goals():
    text = request.form['T1'] + ' : ' + request.form['T2']
    write_txt(SCORE_FILEPATH, text)
    return render_main_template()

##### Functions #####
def write_txt(filepath, txt):
    with open(filepath, 'a') as file:
        file.write(txt + '\n')

def heartbeat():
    time_since_last_heartbeat = time.time() - heartbeat_time
    if(time_since_last_heartbeat > 300):
        write_txt(BET_FILEPATH, 'Z')

def state(filepath):
    with open(filepath, 'r') as file:
        raw_text = file.readlines()
        if not raw_text:
            return ""
        else:
            return raw_text[-1].strip()

def render_main_template():
    data = {'bet_state': state(BET_FILEPATH), 'goal_state': state(SCORE_FILEPATH)}
    return render_template('place_bet.html', data = data )


##### Heartbeat Scheduler #####
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=heartbeat,
    trigger=IntervalTrigger(seconds=300),
    id='heartbeat_job',
    name='Check heartbeat every 5 minutes',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


##### App Entry #####
if __name__ == '__main__':
    app.run()
