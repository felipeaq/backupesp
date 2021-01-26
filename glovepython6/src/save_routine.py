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
            # self.__window=window
            # self.__count=0
            SaveRoutine.__instance.__current_file = ""
            SaveRoutine.__instance.__comment = ""
        return SaveRoutine.__instance

    def __append_points(self):
        with open(self.__current_file, "a") as f:
            end = len(ReadRoutine().sensors.rtc)
            # start=end-begin
            # for k in range (start,end):
            s = str(ReadRoutine().sensors.rtc[-1])
            for i in range(Sensors.TOTAL_S):
                for j in range(Sensors.TOTAL_P//2):
                    s += ";"
                    s += "{}".format(
                        ReadRoutine().sensors[i].a[j][-1])

                for j in range(Sensors.TOTAL_P//2):
                    s += ";"
                    s += "{}".format(
                        ReadRoutine().sensors[i].g[j][-1])
            # for i in range (Sensors.TOTAL_S):
            #    for j in range (Sensors.TOTAL_P//2):
            #        s+=";"
            #        if ReadRoutine().active_sensors[i]:
            #           s+="{}".format(ReadRoutine().sensors.list_s[i].g[j][-1])

            s += "\n"

            f.write(s)

    def __start_file(self):
        self.__current_file = SaveRoutine().PATH+str(datetime.datetime.now()) + \
            "_"+self.__comment+".csv"
        with open(self.__current_file, "w") as f:
            s = "time"
            axis = ["x", "y", "z"]
            for i in range(Sensors.TOTAL_S):
                for j in range(Sensors.TOTAL_P//2):
                    s += ";a{}{}".format(axis[j], i+1)
                for j in range(Sensors.TOTAL_P//2):
                    s += ";g{}{}".format(axis[j], i+1)
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
