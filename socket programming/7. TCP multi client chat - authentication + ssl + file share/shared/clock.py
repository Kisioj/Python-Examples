from time import sleep, time


class Clock:
    def __init__(self, fps):
        self.fps = fps
        self.frame_time = 1.0 / fps
        self.last_tick = time()

    def tick(self):
        current_tick = time()
        sleep_time = self.frame_time - (current_tick - self.last_tick)
        self.last_tick = current_tick
        if sleep_time > 0:
            sleep(sleep_time)
