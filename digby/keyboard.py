import time


class KeyboardHandler:

    def __init__(self, start_val=0.5, wait_time=0.05):
        self.start_val = start_val
        self.wait_time = wait_time

        # Current values
        self.v = 0
        self.angle = 0
        self.last_time = time.time()

    def update(self, keypress):
        """Takes a dictionary `keypress` that contains
            {
                'KeyW': bool,
                'KeyA': bool,
                'KeyS': bool,
                'KeyD': bool
            }
        """
        if time.time() - self.last_time > self.wait_time:
            if keypress['KeyW']:
                if self.v > 0:
                    self.v += (1 - self.v) * 0.5
                else:
                    self.v = self.start_val
            elif keypress['KeyS']:
                if self.v < 0:
                    self.v += (-1 - self.v) * 0.5
                else:
                    self.v = -self.start_val
            else:
                self.v = 0

            if keypress['KeyA']:
                if self.angle > 0:
                    self.angle += (1 - self.angle) * 0.5
                else:
                    self.angle = self.start_val
            elif keypress['KeyD']:
                if self.angle < 0:
                    self.angle += (-1 - self.angle) * 0.5
                else:
                    self.angle = -self.start_val
            else:
                self.angle = 0

    def get_velocity(self):
        return self.v, self.angle
