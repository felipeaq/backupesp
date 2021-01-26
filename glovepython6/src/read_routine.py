from sensors import *


class ReadRoutine(object):
    __instance = None
    bytes_sync = [0, 117, 255, 117]

    def __new__(cls):
        if ReadRoutine.__instance is None:
            total_s = 6
            ReadRoutine.__instance = object.__new__(cls)
            ReadRoutine.__instance.sensors = SensorsSet(
                Sensors.TOTAL_S, Sensors.MAX_X)
            ReadRoutine.__instance.cycle_past = 0
            ReadRoutine.__instance.n_s = 6
            ReadRoutine.__instance.active_sensors = [False]*total_s
            ReadRoutine.__instance.sensor_pos = []
            ReadRoutine.__instance.FRTC = 32768.0
            ReadRoutine.__instance.sock = None

        return ReadRoutine.__instance

    def sync(self, data):

        return data[4:]

    def read_values(self, sock):
        data = sock.recv(Sensors.WINDOW_SOCK_SIZE)
        # print(len(data))
        while len(data) != Sensors.WINDOW_SOCK_SIZE:
            data += sock.recv(Sensors.WINDOW_SOCK_SIZE-len(data))
        if len(data) != Sensors.WINDOW_SOCK_SIZE:
            print(len(data))

        data = self.sync(data)
        self.sensors.add(data)
        if len(self.sensors.rtc) > 10:
            print(self.sensors.rtc[-11:])
        # print(self.sensors.a[0])

        #active_sensors = [False]*self.n_s
        #n_s = int.from_bytes(sock.recv(1), "little")

    def update_time(self, cycle):

        deltaCycle = 0
        if (cycle >= self.cycle_past):
            delta_cycle = cycle-self.cycle_past
        else:
            delta_cycle = 2**16-self.cycle_past+cycle

        delta_time = delta_cycle/self.FRTC

        if not self.sensors.rtc:
            self.sensors.rtc.append(delta_time)
        else:
            self.sensors.rtc.append(delta_time+self.sensors.rtc[-1])
        self.cycle_past = cycle


def main():

    ReadRoutine().read_values("a")
    ReadRoutine().update_time(2)
    ReadRoutine().update_time(4)
    ReadRoutine().update_time(2**15-1)
    ReadRoutine().update_time(1)
    #print (ReadRoutine().sensors)


if __name__ == "__main__":
    main()
