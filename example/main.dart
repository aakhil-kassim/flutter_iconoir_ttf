import 'package:flutter/material.dart';
import 'package:flutter_iconoir_ttf/flutter_iconoir_ttf.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Iconoir Icons Example'),
        ),
        body: const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Text('Hello from Regular world:'),
              Icon(IconoirIcons.infinite, color: Colors.purple),
              Icon(IconoirIcons.parking, color: Colors.red),
              Icon(IconoirIcons.pound, color: Colors.blue),
              Icon(IconoirIcons.googleDriveWarning, color: Colors.green),
              Icon(IconoirIcons.tram, color: Colors.orange),
              SizedBox(height: 10,),
              Text('Hello from Bold world:'),
              // Bold version of icons
              Icon(IconoirIconsBold.infinite, color: Colors.purple),
              Icon(IconoirIconsBold.parking, color: Colors.red),
              Icon(IconoirIconsBold.pound, color: Colors.blue),
              Icon(IconoirIconsBold.googleDriveWarning, color: Colors.green),
              Icon(IconoirIconsBold.tram, color: Colors.orange),
            ],
          ),
        ),
      ),
    );
  }
}
