from digby.motors import MotorController
from digby.keyboard import KeyboardHandler
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

FR_PWM = 14
FR_DIR = 15
BR_PWM = 18
BR_DIR = 23

FL_DIR = 4
FL_PWM = 17
BL_DIR = 27
BL_PWM = 22


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

keyboard = KeyboardHandler()
motors = MotorController(FL_PWM, FL_DIR, FR_PWM, FR_DIR, BL_PWM, BL_DIR,
                         BR_PWM, BR_DIR, reverse_bl=True)

@app.route('/')
def sessions():
    return render_template('main.html')


@socketio.on('connect')
def socket_connect():
    print('Connection')
    motor_tel = motors.get_telemetry()
    emit('telemetry', motor_tel)


@socketio.on('keyboard_update')
def socket_keypress(json):
    keyboard.update(json)
    v, angle = keyboard.get_velocity()
    motors.steer(angle, v)
    
    motor_tel = motors.get_telemetry()
    emit('telemetry', motor_tel)


if __name__ == '__main__':
    socketio.run(app)
