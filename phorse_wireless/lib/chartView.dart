import 'package:flutter/material.dart';
import 'realtime_chart.dart';

class ChartView extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Second Route"),
      ),
      body: Center(
        child: Column(
          children: <Widget>[
            Container(height: 150, child: RealtimeChart()),
            SizedBox(
              height: 10,
            ),
            //ConfigurationWidget(),
          ],
        ),
      ),
    );
  }
}
//child: Column(
//          children: <Widget>[
//            Container(height: 150, child: RealtimeChart()),
//            SizedBox(
//              height: 10,
//            ),
//            //ConfigurationWidget(),
//          ],
//        ),
