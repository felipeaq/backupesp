import 'package:phorse_wireless/receiver.dart';
import 'package:phorse_wireless/sensor.dart';

class PairSensorRecv {
  Sensor sensor;
  Receiver receiver;
  PairSensorRecv(this.sensor, this.receiver);
}

class SensorList {
  static SensorList _instance;
  List<PairSensorRecv> sensorList = List<PairSensorRecv>();
  factory SensorList() {
    _instance ??= SensorList._internalConstructor();
    return _instance;
  }
  SensorList._internalConstructor();

  void addSensor() {
  
    Sensor sensor = Sensor();
    Receiver r = Receiver();
    PairSensorRecv p = PairSensorRecv(sensor, r);
    sensorList.add(p);
  }

  Future<void> connectReceivAt(int pos, String ip, int port) async {
    await sensorList[pos].receiver.connect(ip, port);
    sensorList[pos].receiver.recv(sensorList[pos].sensor);
  }

  Sensor getAt(int pos) {
    
    return sensorList[pos].sensor;
  }

  void closeAt(int pos) {
    sensorList[pos].receiver.close();
  }
}
