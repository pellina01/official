class executor:
    import datetime
    import math
    import time

    def __init__(self, function, frequency):
        self.function = function
        self.frequency_period = self.math.trunc(1440 / frequency)
        self.schedule = []
        for items in range(0, frequency):
            self.schedule.append(items * frequency)

    def execute(self):
        self.time.sleep(self.__initial_delay())
        while True:
            self.function()
            self.time.sleep(self.frequency_period)

    def __initial_delay(self):
        now = self.datetime.datetime.now()
        min_now = (60 * now.hour) + now.minute
        if min_now in self.schedule:
            temporary_delay = 0
        else:
            time_sched = self.schedule.copy()
            time_sched.append(min_now)
            time_sched.sort()
            index = time_sched.index(min_now)
            if index == len(time_sched) - 1:
                temporary_delay = 1140 - min_now
            else:
                temporary_delay = time_sched(index + 1) - time_sched(index)
            del index
            del time_sched
        del now
        del min_now
        return temporary_delay
