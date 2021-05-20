from gpiozero import OutputDevice, PWMOutputDevice


class MotorController:
    def __init__(self, front_left_pwm, front_left_dir, front_right_pwm,
                 front_right_dir, back_left_pwm, back_left_dir, back_right_pwm,
                 back_right_dir, max_speed=0.5, reverse_fl=False,
                 reverse_bl=False, reverse_fr=False, reverse_br=False):
        # Motor pins
        self.fl_pwm = PWMOutputDevice(front_left_pwm, initial_value=False)
        self.fl_dir = OutputDevice(front_left_dir,
                                   active_high=reverse_fl,
                                   initial_value=False)
        self.fr_pwm = PWMOutputDevice(front_right_pwm, initial_value=False)
        self.fr_dir = OutputDevice(front_right_dir,
                                   active_high=reverse_fr,
                                   initial_value=False)
        self.bl_pwm = PWMOutputDevice(back_left_pwm, initial_value=False)
        self.bl_dir = OutputDevice(back_left_dir,
                                   active_high=reverse_bl,
                                   initial_value=False)
        self.br_pwm = PWMOutputDevice(back_right_pwm, initial_value=False)
        self.br_dir = OutputDevice(back_right_dir,
                                   active_high=reverse_br,
                                   initial_value=False)

        # Motor velocity
        self.max_speed = max_speed
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
        vel *= self.max_speed
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

    def get_telemetry(self):
        return {
            'fl_pwm': self.fl_pwm.value,
            'fl_dir': self.fl_dir.value,
            'fr_pwm': self.fr_pwm.value,
            'fr_dir': self.fr_dir.value,
            'bl_pwm': self.bl_pwm.value,
            'bl_dir': self.bl_dir.value,
            'br_pwm': self.br_pwm.value,
            'br_dir': self.br_dir.value,
            'vl': self.vl,
            'vr': self.vr
        }
