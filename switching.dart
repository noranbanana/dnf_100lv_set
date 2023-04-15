import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:ui';
import 'package:http/http.dart' as http;
import 'package:device_info_plus/device_info_plus.dart';
import 'package:flutter/material.dart';
import 'package:flutter_background_service/flutter_background_service.dart';
import 'package:flutter_background_service_android/flutter_background_service_android.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:vibration/vibration.dart';
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await initializeService();
  runApp(const MyApp());
}

//TextEditingController _controller = TextEditingController(text: ': 성령의 메이스');
TextEditingController _controller = TextEditingController();



Future<void> initializeService() async {
  final service = FlutterBackgroundService();

  /// OPTIONAL, using custom notification channel id
  const AndroidNotificationChannel channel = AndroidNotificationChannel(
    'my_foreground', // id
    'MY FOREGROUND SERVICE', // title
    description:
    'This channel is used for important notifications.', // description
    importance: Importance.low, // importance must be at low or higher level
  );

  final FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin =
  FlutterLocalNotificationsPlugin();

  /*if (Platform.isIOS) {
    await flutterLocalNotificationsPlugin.initialize(
      const InitializationSettings(
        iOS: IOSInitializationSettings(),
      ),
    );
  }*/

  await flutterLocalNotificationsPlugin
      .resolvePlatformSpecificImplementation<
      AndroidFlutterLocalNotificationsPlugin>()
      ?.createNotificationChannel(channel);

  await service.configure(
    androidConfiguration: AndroidConfiguration(
      // this will be executed when app is in foreground or background in separated isolate
      onStart: onStart,

      // auto start service
      autoStart: true,
      isForegroundMode: true,

      notificationChannelId: 'my_foreground',
      initialNotificationTitle: 'AWESOME SERVICE',
      initialNotificationContent: 'Initializing',
      foregroundServiceNotificationId: 888,
    ),
    iosConfiguration: IosConfiguration(
      // auto start service
      autoStart: true,

      // this will be executed when app is in foreground in separated isolate
      onForeground: onStart,

      // you have to enable background fetch capability on xcode project
      onBackground: onIosBackground,
    ),
  );

  service.startService();
}

// to ensure this is executed
// run app from xcode, then from xcode menu, select Simulate Background Fetch

@pragma('vm:entry-point')
Future<bool> onIosBackground(ServiceInstance service) async {
  WidgetsFlutterBinding.ensureInitialized();
  DartPluginRegistrant.ensureInitialized();

  SharedPreferences preferences = await SharedPreferences.getInstance();
  await preferences.reload();
  final log = preferences.getStringList('log') ?? <String>[];
  log.add(DateTime.now().toIso8601String());
  await preferences.setStringList('log', log);

  return true;
}

@pragma('vm:entry-point')
void onStart(ServiceInstance service) async {
  // Only available for flutter 3.0.0 and later
  DartPluginRegistrant.ensureInitialized();

  // For flutter prior to version 3.0.0
  // We have to register the plugin manually

  SharedPreferences preferences = await SharedPreferences.getInstance();
  await preferences.setString("hello", "world");

  /// OPTIONAL when use custom notification
  final FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin =
  FlutterLocalNotificationsPlugin();

  if (service is AndroidServiceInstance) {
    service.on('setAsForeground').listen((event) {
      service.setAsForegroundService();
    });

    service.on('setAsBackground').listen((event) {
      service.setAsBackgroundService();
    });
  }
  /*
  service.on('stopService').listen((event) {
    service.stopSelf();
  });
  */

  //var url = 'https://api.neople.co.kr/df/auction?limit=400&itemName=${_controller.text}&wordType=full&q=minLevel:100&rarity:%EC%9C%A0%EB%8B%88%ED%81%AC&apikey=NwrkuWSx3YoOmFLLM5ylRdQTyPsX0vtH';

  List<String> category = ["무기","상의","어깨","하의","신발","허리","팔찌","목걸이","반지","보조장비","마법석","귀걸이"];

  List<int> lowPriceRecord = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1];
  List<String> record = [];
  var timerCount = 0;
  // bring to foreground
  Timer.periodic(const Duration(seconds: 5), (timer) async {
    if (service is AndroidServiceInstance) {
      if (await service.isForegroundService()) {
        if(timerCount % 12 == 0){
          List<int> lowPrice = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1];
          List<int> counts = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1];
          //String url;
          http.Response response;
          if(_controller.text == ''){
            response = await http.get(Uri.parse('https://api.neople.co.kr/df/auction?limit=400&itemName=%3A%20%EC%84%B1%EB%A0%B9%EC%9D%98%20%EB%A9%94%EC%9D%B4%EC%8A%A4&wordType=full&q=minLevel:100&rarity:%EC%9C%A0%EB%8B%88%ED%81%AC&apikey=NwrkuWSx3YoOmFLLM5ylRdQTyPsX0vtH'));
            //url = 'https://api.neople.co.kr/df/auction?limit=400&itemName=%3A%20%EC%84%B1%EB%A0%B9%EC%9D%98%20%EB%A9%94%EC%9D%B4%EC%8A%A4&wordType=full&q=minLevel:100&rarity:%EC%9C%A0%EB%8B%88%ED%81%AC&apikey=NwrkuWSx3YoOmFLLM5ylRdQTyPsX0vtH';
          }
          else{
            response = await http.get(Uri.parse('https://api.neople.co.kr/df/auction?limit=400&itemName=${_controller.text}&wordType=full&q=minLevel:100&rarity:%EC%9C%A0%EB%8B%88%ED%81%AC&apikey=NwrkuWSx3YoOmFLLM5ylRdQTyPsX0vtH'));
            //url = 'https://api.neople.co.kr/df/auction?limit=400&itemName=${_controller.text}&wordType=full&q=minLevel:100&rarity:%EC%9C%A0%EB%8B%88%ED%81%AC&apikey=NwrkuWSx3YoOmFLLM5ylRdQTyPsX0vtH';
          }
          //var url = 'https://api.neople.co.kr/df/auction?limit=400&itemName=${_controller.text}&wordType=full&q=minLevel:100&rarity:%EC%9C%A0%EB%8B%88%ED%81%AC&apikey=NwrkuWSx3YoOmFLLM5ylRdQTyPsX0vtH';

          //final response = await http.get(Uri.parse(url));
          //print(url);
          final parsed = json.decode(response.body);
          List<String> result = [];
          for (var i = 0; i < parsed["rows"].length; i++) {
            String typeName;
            int typeIndex;
            if (parsed["rows"][i]["itemType"] == "무기") {
              if (lowPrice[0] == -1 ||
                  lowPrice[0] > parsed["rows"][i]["currentPrice"]) {
                lowPrice[0] = parsed["rows"][i]["currentPrice"];
              }
              typeName = "무기";
              typeIndex = 0;
            }
            else {
              var detailParsed = parsed["rows"][i]["itemTypeDetail"].split(' ');
              var detailKey = detailParsed[detailParsed.length - 1];
              if (category.contains(detailKey)) {
                typeIndex = category.indexOf(detailKey);
                typeName = detailKey;

                if (lowPrice[typeIndex] == -1 ||
                    lowPrice[typeIndex] > parsed["rows"][i]["currentPrice"]) {
                  lowPrice[typeIndex] = parsed["rows"][i]["currentPrice"];
                }
              }
              else {
                continue;
              }
            }
            counts[typeIndex] += 1;
            if (parsed["rows"][i]["currentPrice"] <= 30000000) {
              if (!result.contains(typeName)) {
                result.add(typeName);
              }
            }
          }
          var sameList = false;
          /*if (record.length == result.length) {
            sameList = true;
            for (var i = 0; i < record.length; i++) {
              if (record[i] != result[i]) {
                sameList = false;
                break;
              }
            }
            for (var i = 0; i < lowPrice.length; i++) {
              if (lowPrice[i] != lowPriceRecord[i]) {
                sameList = false;
                break;
              }
            }
          }*/

          if (!sameList) {
            Vibration.vibrate(duration: 1000);
            record = [...result];
            lowPriceRecord = [...lowPrice];
          }
          var firstLine = "부위/개수/최저가";
          /*for (int i=0; i<result.length; i++){
          firstLine += result[i];
          if (i != result.length-1){
            for (int j=0; j<13-3*result[i].length; j++){
              firstLine += ' ';
            }
          }
        }*/
          var secondLine = "";
          for (int i = 0; i < lowPrice.length; i++) {
            if (lowPrice[i] < 0) {
              continue;
            }
            secondLine += "${category[i]}/";
            secondLine += "${counts[i]}/";
            secondLine += "${(lowPrice[i] / 10000000).toStringAsFixed(2)}, ";
          }

          /// OPTIONAL for use custom notification
          /// the notification id must be equals with AndroidConfiguration when you call configure() method.
          flutterLocalNotificationsPlugin.show(
            888,
            //'2000이하 배크',
            //'${result.join(" ")}',
            firstLine,
            secondLine,
            const NotificationDetails(
              android: AndroidNotificationDetails(
                'my_foreground',
                'MY FOREGROUND SERVICE',
                icon: 'ic_bg_service_small',
                ongoing: true,
                styleInformation: BigTextStyleInformation(''),
              ),
            ),
          );

          // if you don't using custom notification, uncomment this
          // service.setForegroundNotificationInfo(
          //   title: "My App Service",
          //   content: "Updated at ${DateTime.now()}",
          // );
        }
        timerCount += 1;
      }
    }
    /// you can see this log in logcat
    //print('FLUTTER BACKGROUND SERVICE: ${DateTime.now()}');
    service.on('stopService').listen((event) {
      service.stopSelf();
      timer.cancel();
    });
    // test using external plugin
    final deviceInfo = DeviceInfoPlugin();
    String? device;
    if (Platform.isAndroid) {
      final androidInfo = await deviceInfo.androidInfo;
      device = androidInfo.model;
    }

    if (Platform.isIOS) {
      final iosInfo = await deviceInfo.iosInfo;
      device = iosInfo.model;
    }

    service.invoke(
      'update',
      {
        "current_date": DateTime.now().toIso8601String(),
        "device": device,
      },
    );
  });
}

class MyApp extends StatefulWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  String text = "Stop Service";
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Service App'),
        ),
        body: Column(
          children: [
            StreamBuilder<Map<String, dynamic>?>(
              stream: FlutterBackgroundService().on('update'),
              builder: (context, snapshot) {
                if (!snapshot.hasData) {
                  return const Center(
                    child: CircularProgressIndicator(),
                  );
                }
                final data = snapshot.data!;
                String? device = data["device"];
                DateTime? date = DateTime.tryParse(data["current_date"]);
                return Column(
                  children: [
                    Text(device ?? 'Unknown'),
                    Text(date.toString()),
                  ],
                );
              },
            ),
            ElevatedButton(
              child: const Text("Foreground Mode"),
              onPressed: () {
                FlutterBackgroundService().invoke("setAsForeground");
              },
            ),
            ElevatedButton(
              child: const Text("Background Mode"),
              onPressed: () {
                FlutterBackgroundService().invoke("setAsBackground");
              },
            ),
            ElevatedButton(
              child: Text(text),
              onPressed: () async {
                print(_controller.text);
                final service = FlutterBackgroundService();
                var isRunning = await service.isRunning();
                if (isRunning) {
                  service.invoke("stopService");
                } else {
                  service.startService();
                }

                if (!isRunning) {
                  text = 'Stop Service';
                } else {
                  text = 'Start Service';
                }
                setState(() {});
              },
            ),
            TextField(
              // The TextField is first built, the controller has some initial text,
              // which the TextField shows. As the user edits, the text property of
              // the controller is updated.
              controller: _controller,
              onSubmitted: _handleSubmitted,
            ),
            const Expanded(
              child: LogView(),
            ),
          ],
        ),
        floatingActionButton: FloatingActionButton(
          onPressed: () {},
          child: const Icon(Icons.play_arrow),
        ),
      ),
    );
  }
  void _handleSubmitted(String text) {
    //_controller.clear();
    //timer.cancel();
    _controller.text = text;


  }
}

class LogView extends StatefulWidget {
  const LogView({Key? key}) : super(key: key);

  @override
  State<LogView> createState() => _LogViewState();
}

class _LogViewState extends State<LogView> {
  late final Timer timer;
  List<String> logs = [];

  @override
  void initState() {
    super.initState();
    timer = Timer.periodic(const Duration(seconds: 1), (timer) async {
      final SharedPreferences sp = await SharedPreferences.getInstance();
      await sp.reload();
      logs = sp.getStringList('log') ?? [];
      if (mounted) {
        setState(() {});
      }
    });
  }

  @override
  void dispose() {
    timer.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: logs.length,
      itemBuilder: (context, index) {
        final log = logs.elementAt(index);
        return Text(log);
      },
    );
  }
}
