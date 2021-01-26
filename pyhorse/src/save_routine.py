from read_routine import *
import datetime
import time


class SaveRoutine:

    __instance = None

    def __new__(cls):
        if SaveRoutine.__instance is None:
            SaveRoutine.__instance = object.__new__(cls)
            SaveRoutine.__instance.PATH = "../data/"
            SaveRoutine.__instance.__saving = False
            SaveRoutine.__instance.__start = False
            SaveRoutine.__instance.__current_file = ""
            SaveRoutine.__instance.__comment = ""
        return SaveRoutine.__instance

    def __append_points(self):
        with open(self.__current_file, "a") as f:
            end = len(ReadRoutine().sensors.rtc)
            # start=end-begin
            # for k in range (start,end):

            s = ""

            for i in range(-Sensors.WINDOW_N_SIZE, 0, 1):
                s += str(ReadRoutine().sensors.rtc[i])
                for j in range(Sensors.AXIS):
                    s += ";{}".format(ReadRoutine().sensors.accGravity[j][i])
                for j in range(Sensors.AXIS):
                    s += ";{}".format(ReadRoutine().sensors.gyroRad[j][i])
                for j in range(Sensors.AXIS):
                    s += ";{}".format(ReadRoutine().sensors.magNorm[j][-1])
                s += "\n"

            f.write(s)

    def __start_file(self):
        self.__current_file = SaveRoutine().PATH+str(datetime.datetime.now()) + \
            "_"+self.__comment+".csv"
        with open(self.__current_file, "w") as f:
            s = "time"
            axis = ["x", "y", "z"]
            types = ["a", "g", "m"]
            for i in types:
                for j in axis:
                    s += ";{}{}".format(i, j)
            s += "\n"
            f.write(s)

    def save_routine(self):
        if self.__start:
            if not self.__saving:
                self.__saving = True
                self.__start_file()

            if len(ReadRoutine().sensors.rtc) >= 1:
                self.__append_points()

    def start(self, comment=""):
        self.__comment = comment
        self.__start = True

    def stop(self):
        self.__start = False
        self.__saving = False


def main():
    SaveRoutine().start()

    SaveRoutine().save_routine()


if __name__ == "__main__":
    main()
