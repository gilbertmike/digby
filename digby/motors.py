from gpiozero import DigitalOutputDevice


class MotorController:
    def __init__(self, front_left_pwm, front_left_dir, front_right_pwm,
                 front_right_dir, back_left_pwm, back_left_dir, back_right_pwm,
                 back_right_dir):
        # Motor pins
        self.fl_pwm = DigitalOutputDevice(front_left_pwm, initial_value=False)
        self.fl_dir = DigitalOutputDevice(front_left_dir, initial_value=False)
        self.fr_pwm = DigitalOutputDevice(front_right_pwm, initial_value=False)
        self.fr_dir = DigitalOutputDevice(front_right_dir, initial_value=False)
        self.bl_pwm = DigitalOutputDevice(back_left_pwm, initial_value=False)
        self.bl_dir = DigitalOutputDevice(back_left_dir, initial_value=False)
        self.br_pwm = DigitalOutputDevice(back_right_pwm, initial_value=False)
        self.br_dir = DigitalOutputDevice(back_right_dir, initial_value=False)

        # Motor velocity
        MAX_SPEED = 1
        self.vl = 0
        self.vr = 0

    def steer(self, angle, vel):
        """Steer the motors.

        The value `angle` is the smallest angle between the steering
        vector and the Y-axis. The value is between -1 (positive X) and 
        1 (negative X).

        The value `vel` is the speed. Value is between -1 (negative Y)
        and 1 (positive Y).
        """
        if angle > 0:
            self.vl = vel * (1-angle)
            self.vr = vel
        else:
            self.vl = vel
            self.vr = vel * (1-abs(angle))
        self._update()

    def _update(self):
        self.fl_pwm.value = abs(self.vl)
        self.bl_pwm.value = abs(self.vl)
        if self.vl > 0:
            self.fl_dir.on()
            self.bl_dir.on()
        else:
            self.fl_dir.off()
            self.bl_dir.off()

        self.fr_pwm.value = abs(self.vr)
        self.br_pwm.value = abs(self.vr)
        if self.vr > 0:
            self.fr_dir.on()
            self.br_dir.on()
        else:
            self.fr_dir.off()
            self.br_dir.off()
