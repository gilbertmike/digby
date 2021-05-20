from digby.motors import MotorController
from digby.keyboard import KeyboardHandler
from flask import Flask, render_template
from flask_socketio import SocketIO

FL_PWM = 14
FL_DIR = 15
BL_PWM = 18
BL_DIR = 23

FR_PWM = 24
FR_DIR = 25
BR_PWM = 8
BR_DIR = 7

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

keyboard = KeyboardHandler()
motors = MotorController(FL_PWM, FL_DIR, FR_PWM, FR_DIR, BL_PWM, BL_DIR,
                         BR_PWM, BR_DIR)


@app.route('/')
def sessions():
    return render_template('main.html')


@socketio.on('connect')
def socket_connect():
    print('Connection')


@socketio.on('keyboard_update')
def socket_keypress(json):
    keyboard.update(json)
    v, angle = keyboard.get_velocity()
    motors.steer(angle, v)


if __name__ == '__main__':
    socketio.run(app)
