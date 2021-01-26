import 'dart:io';
import 'dart:convert';
import 'package:phorse_wireless/sensor.dart';

class Receiver {
  Socket socket;

  Receiver();

  Future<void> connect(String ip, int port) async {
    this.socket = await Socket.connect(ip, port);
    this.socket.add(utf8.encode('start'));
  }

  Future<void> recv(Sensor sensor) async {
    socket.listen((List<int> v) {
      sensor.addFromWindow(v);
    });
  }

  Future<void> close() async {
    try {
      this.socket.close();
    } catch (e) {
      print(e);
    }
  }
}
