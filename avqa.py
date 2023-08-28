import pickle
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
import random
import pandas as pd
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = 'avqa-data-collection'
socketio = SocketIO(app)

# # # # # # login page # # # # # # # # # # # # #
with open('registered_emails.pkl', "rb") as f:
    registered_email_ids = pickle.load(f)


@app.route("/")
def home():
    return render_template('homepage.html')


@app.route('/check-credentials', methods=['POST'])
def login():
    email_id = request.form.get('email_id')

    if email_id in registered_email_ids:
        session['worker_id'] = registered_email_ids[email_id]
        return redirect(url_for('instructions'))
    else:
        return render_template('homepage.html', login_error='Incorrect email id or user not registered.')

# # # # # # end of login page # # # # # # # # # # # # #

# # # # # # Instructions page # # # # # # # # # # # # #


@app.route("/instructions")
def instructions():
    return render_template('instructions.html')


@app.route('/instructions-next-button', methods=['POST'])
def instructions_next_button():
    next_value = request.form.get('next')
    if next_value:
        return redirect(url_for('example'))

# # # # # # End of Instructions page # # # # # # # # # # # # #

# # # # # # Example page # # # # # # # # # # # # #


@app.route("/example")
def example():
    return render_template('example.html')


@app.route('/example-proceed-to-task-button', methods=['POST'])
def example_proceed_to_task_button():
    next_value = request.form.get('proceed_to_task')
    if next_value:
        return redirect(url_for('task'))

# # # # # # End of example page # # # # # # # # # # # # #

# # # # # # Task page # # # # # # # # # # # # #

batch_num = 1

#videos_folder = os.path.join(app.static_folder, 'videos/batch{}/'.format(batch_num))
videos_folder = 'videos/batch{}/'.format(batch_num)
#app.config['videos_folder'] = videos_folder

video_files = [filename for filename in os.listdir(videos_folder)]
print(video_files)

output_folder = 'outputs/batch{}/'.format(batch_num)
app.config['output_folder'] = output_folder
os.makedirs('outputs/batch{}/'.format(batch_num), exist_ok=True)


available_video_files = video_files
currently_assigned_dict = {}
currently_assigned_list = []


def assign_video_for_client(client_id):
    if client_id not in currently_assigned_dict:
        video = random.choice(available_video_files)
        while video in currently_assigned_list:
            video = random.choice(available_video_files)
        session['video'] = video
        currently_assigned_dict[client_id] = video
        currently_assigned_list.append(video)
        return video
    else:
        return currently_assigned_dict[client_id]


@app.route("/task")
def task():
    if set(available_video_files) == set(currently_assigned_list):
        print("av vid files = ", available_video_files)
        return render_template('all_tasks_completed.html')

    if available_video_files:
        video = assign_video_for_client(session['worker_id'])
        return render_template('task.html', video=video)
    else:
        return render_template('all_tasks_completed.html')


@app.route('/next-task-button', methods=['POST'])
def next_task_button():
    print("this is called")
    yn_q1 = request.form.get('yes_or_no_q1')
    yn_a1 = request.form.get('yes_or_no_ans1')
    yn_q2 = request.form.get('yes_or_no_q2')
    yn_a2 = request.form.get('yes_or_no_ans2')

    desc_q1 = request.form.get('desc_q1')
    desc_a1 = request.form.get('desc_ans1')
    desc_q2 = request.form.get('desc_q2')
    desc_a2 = request.form.get('desc_ans2')

    logical_q1 = request.form.get('logical_q1')
    logical_a1 = request.form.get('logical_ans1')
    logical_q2 = request.form.get('logical_q2')
    logical_a2 = request.form.get('logical_ans2')

    worker_id = [session['worker_id']]*6
    q_type = ['yes_or_no', 'yes_or_no', 'descriptive', 'descriptive', 'logical', 'logical']
    qns = [yn_q1, yn_q2, desc_q1, desc_q2, logical_q1, logical_q2]
    ans = [yn_a1, yn_a2, desc_a1, desc_a2, logical_a1, logical_a2]

    df = pd.DataFrame(list(zip(worker_id, q_type, qns, ans)), columns=['worker_id', 'q_type', 'question', 'answer'])
    df.to_csv(output_folder + session['video'][:-3] + 'csv')

    available_video_files.remove(session['video'])
    try:
        del currently_assigned_dict[session['worker_id']]
        currently_assigned_list.remove(session['video'])
    except:
        pass

    return redirect(url_for('task'))


@socketio.on('connect')
def handle_connect():
    print("client {} connected successfully".format(session.get('worker_id')))
    print(currently_assigned_dict)
    print(currently_assigned_list)


@socketio.on('disconnect')
def handle_disconnect():
    worker_id = session.get('worker_id')
    try:
        video_assigned_to_disconnected_user = currently_assigned_dict[worker_id]
        del currently_assigned_dict[worker_id]
        currently_assigned_list.remove(video_assigned_to_disconnected_user)
    except:
        pass

    print("client {} disconnected successfully".format(session.get('worker_id')))
    print(currently_assigned_dict)
    print(currently_assigned_list)


@app.route('/videos/batch{}/<filename>'.format(batch_num))
def serve_video(filename):
    return send_from_directory('videos/batch{}'.format(batch_num), filename)


if __name__ == '__main__':
    app.run(debug=True)
