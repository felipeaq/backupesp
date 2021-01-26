import 'dart:math';
import 'dart:collection';

class Sensor {
  static const double GYRODIV = 10430.3783505;
  static const double ACCDIV = 16384;
  static const int MAX_X = 2048;
  static const int AXIS = 3;
  static const int WINDOW_SIZE = 166;
  static const int CAPACITY = 2048;
  List<Queue<int>> acc = List();
  List<Queue<int>> gyro = List();
  List<Queue<double>> accGravity = List();
  List<Queue<double>> gyroNorm = List();
  List<int> lastData = List();
  Queue<int> rtc;

  Sensor() {
    rtc = Queue();
    for (int i = 0; i < AXIS; i++) {
      print("uidsdsadsa $i");
      acc.add(Queue<int>());
      gyro.add(Queue<int>());
      accGravity.add(Queue<double>());
      gyroNorm.add(Queue<double>());
    }
  }

  int shortToLong(List<int> shortInt) {
    int longInt = 0;
    for (int i = 0; i < shortInt.length; i++) {
      int mult = pow(256, i);
      longInt += shortInt[i] * mult;
    }

    return longInt;
  }

  void addRemove(Queue q, int v, {double div = 0.0}) {
    if (q.length >= Sensor.CAPACITY) {
      q.removeFirst();
    }

    if (div != 0.0) {
      q.add(v.toDouble() / div);
    } else {
      q.add(v);
    }
  }

  void add(int time, List<int> accLocal, List<int> gyroLocal) {
    addRemove(rtc, time);
    for (int i = 0; i < AXIS; i++) {
      addRemove(acc[i], accLocal[i]);
      addRemove(gyro[i], gyroLocal[i]);
      addRemove(accGravity[i], accLocal[i], div: ACCDIV);
      addRemove(gyroNorm[i], gyroLocal[i], div: GYRODIV);
    }
  }

  void addFromSliced(List<int> v) {
    //print (v);
    int time = shortToLong(v.sublist(0, 4));
    List<int> accLocal = List();
    List<int> gyroLocal = List();
    for (int i = 0; i < AXIS; i++) {
      accLocal.add(shortToLong(v.sublist(4 + 2 * i, 4 + 2 * i + 2)));
      gyroLocal.add(shortToLong(v.sublist(10 + 2 * i, 10 + 2 * i + 2)));
    }
    add(time, accLocal, gyroLocal);
  }

  void addFromWindow(List<int> v) {
    print (v.length);
    for (int i = 0; i < v.length - WINDOW_SIZE; i += WINDOW_SIZE) {
      addFromSliced(v.sublist(i, i + WINDOW_SIZE));
    }
  }

  Future<void> addFromStream(Stream<List<int>> v) {
    final sub = v.listen(
      (data) => addFromWindow(data),
    );
  }
}
