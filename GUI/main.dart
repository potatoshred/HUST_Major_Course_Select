import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // TRY THIS: Try running your application with "flutter run". You'll see
        // the application has a purple toolbar. Then, without quitting the app,
        // try changing the seedColor in the colorScheme below to Colors.green
        // and then invoke "hot reload" (save your changes or press the "hot
        // reload" button in a Flutter-supported IDE, or press "r" if you used
        // the command line to start the app).
        //
        // Notice that the counter didn't reset back to zero; the application
        // state is not lost during the reload. To reset the state, use hot
        // restart instead.
        //
        // This works for code too, not just values: Most code changes can be
        // tested with just a hot reload.
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;
  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class Course {
  String name;
  String teacher;
  String result;
  Course({required this.name, required this.teacher, this.result = ""});
}

class _MyHomePageState extends State<MyHomePage> {
  final TextEditingController cookieController = TextEditingController();
  final TextEditingController uaController = TextEditingController(text: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36");
  final TextEditingController retryController = TextEditingController(text: "3");
  final TextEditingController timerController = TextEditingController();
  List<Course> courses = [
    Course(name: "大数据管理概论", teacher: "左琼"),
    Course(name: "函数式编程原理", teacher: "郑然"),
    Course(name: "计算机图形学", teacher: "何云峰"),
    Course(name: "计算机视觉导论", teacher: "刘康"),
  ];
  String newCourseName = "";
  String newTeacherName = "";
  bool isRequesting = false;

  void addCourse() {
    if (newCourseName.isNotEmpty && newTeacherName.isNotEmpty) {
      setState(() {
        courses.add(Course(name: newCourseName, teacher: newTeacherName));
        newCourseName = "";
        newTeacherName = "";
      });
    }
  }

  void removeCourse(int index) {
    setState(() {
      courses.removeAt(index);
    });
  }

  // TODO: 实现并发请求和重试逻辑
  // TODO: 实现定时选课逻辑

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Container(
        width: 400,
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 8)],
        ),
        child: Scaffold(
          backgroundColor: Colors.transparent,
          appBar: AppBar(
            backgroundColor: Theme.of(context).colorScheme.inversePrimary,
            title: Text(widget.title),
            elevation: 0,
            shape: const RoundedRectangleBorder(
              borderRadius: BorderRadius.vertical(top: Radius.circular(12)),
            ),
          ),
          body: SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                TextField(
                  controller: cookieController,
                  decoration: InputDecoration(
                    labelText: "Cookie",
                    labelStyle: const TextStyle(fontWeight: FontWeight.bold, color: Colors.deepPurple),
                    border: OutlineInputBorder(),
                    hintText: "请在浏览器登录后复制Cookie粘贴到此处",
                  ),
                ),
                const SizedBox(height: 12),
                TextField(
                  controller: uaController,
                  decoration: InputDecoration(
                    labelText: "User Agent",
                    labelStyle: const TextStyle(fontWeight: FontWeight.bold, color: Colors.deepPurple),
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 12),
                TextField(
                  controller: retryController,
                  decoration: InputDecoration(
                    labelText: "重试次数",
                    labelStyle: const TextStyle(fontWeight: FontWeight.bold, color: Colors.deepPurple),
                    border: OutlineInputBorder(),
                  ),
                  keyboardType: TextInputType.number,
                ),
                const SizedBox(height: 12),
                TextField(
                  controller: timerController,
                  decoration: InputDecoration(
                    labelText: "定时选课（秒后自动开始）",
                    labelStyle: const TextStyle(fontWeight: FontWeight.bold, color: Colors.deepPurple),
                    border: OutlineInputBorder(),
                    hintText: "留空则立即开始",
                  ),
                  keyboardType: TextInputType.number,
                ),
                const SizedBox(height: 20),
                Row(
                  children: [
                    Expanded(
                      child: TextField(
                        decoration: InputDecoration(
                          labelText: "课程名",
                          labelStyle: const TextStyle(fontWeight: FontWeight.bold, color: Colors.deepPurple),
                          border: OutlineInputBorder(),
                        ),
                        onChanged: (v) => newCourseName = v,
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: TextField(
                        decoration: InputDecoration(
                          labelText: "教师名",
                          labelStyle: const TextStyle(fontWeight: FontWeight.bold, color: Colors.deepPurple),
                          border: OutlineInputBorder(),
                        ),
                        onChanged: (v) => newTeacherName = v,
                      ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.add),
                      onPressed: addCourse,
                    ),
                  ],
                ),
                const SizedBox(height: 20),
                ListView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: courses.length,
                  itemBuilder: (context, index) {
                    final course = courses[index];
                    return Card(
                      child: ListTile(
                        title: Text(course.name),
                        subtitle: Text(course.teacher),
                        trailing: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text(course.result),
                            IconButton(
                              icon: const Icon(Icons.delete),
                              onPressed: () => removeCourse(index),
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                ),
                const SizedBox(height: 20),
                ElevatedButton(
                  onPressed: isRequesting ? null : () {
                    // TODO: 实现选课并发请求和重试逻辑
                    // TODO: 实现定时选课逻辑
                  },
                  child: Text(isRequesting ? "正在选课..." : "开始选课"),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
