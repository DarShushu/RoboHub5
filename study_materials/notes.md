Существует четыре различных визуализации состояния робота:

1. Конфигурация робота в среде планирования `/planning scene` (активна по умолчанию).

2. Планируемый путь робота (активно по умолчанию).

3. Зеленый: Начальное состояние для планирования движения (по умолчанию отключено).

4. Оранжевый: Состояние цели для планирования движения (активно по умолчанию).

Состояния отображения для каждой из этих визуализаций можно включать и выключать с помощью флажков:

1. Робот сцены планирования с помощью флажка `Show Robot Visual` на вкладке `Scene Robot`.

2. Планируемый путь с помощью флажка `Show Robot Visual` на вкладке `Planned Path`.

3. Начальное состояние с помощью флажка `Query Start State` на вкладке `Planning Request`.

4. Состояние цели с помощью флажка `Query Goal State` на вкладке `Planning Request`.

* Играйте со всеми этими флажками, чтобы включать и выключать различные визуализации.

<p align="center">
    <img src=../assets/ros_topics/1_rviz_plugin_visualize_robots.png />
</p>

## Программы - узлы

Перейдем к одной из важных частей концепции ROS -программы и скрипты называются узлами (nodes). Это всё, что надо знать про определение =)

Что интереснее, как с ними взаимодействовать?

Для начала, надо понять, что при запуске робота запускается сразу несколько узлов, а значит нам нужен способ посмотреть весь список запущенных узлов.

В любой работе относительно узлов нам поможет утилита `rosnode`:

```bash
rosnode list
```

В выводе видим:

```md
/joint_state_publisher
/move_group
/robot_state_publisher
/rosout
/rviz
/virtual_joint_broadcaster_0
```

Прямо сейчас запущено всего 6 узлов, пройдёмся, что это за узлы:

- `joint_state_publisher` - узел для генерации и публикации информации о состояниях суставов робота (joint states), которое включает позицию, скорости и усилия для каждого сочленения;
- `move_group` - узел управления движением робота и планирование траекторий. Это один из ключевых узлов стэка `MoveIt!`, который используется для работы с роботами-манипуляторами;
- `robot_state_publisher` - публикация текущей трансформации (poses) робота в виде дерева преобразований (transform tree) на основе получаемых состояний суставов от узла `joint_state_publisher` (или сенсоров робота) и вычисляет пространственные положения всех частей робота на основе описания его геометрии в формате описания URDF (с URDF-файлами подробно мы познакомимся чуть позже);
- `rosout` - служебный узел, который собирает все выводы логов от других углов и отправляет их в консоль или в файл;
- `rviz` - узел визуализации данных, состояния робота и его окружения в системе ROS.
- `virtual_joint_broadcaster_0` - узел, занимающийся публикацией состояния виртуальных сочленений (virtual_joint) в системе координат робота - используется для симуляции движения звеньев робота, которые не имеют физического эквивалента

Вроде несложно, так? 

Тогда, чтобы разобраться с тем, как работает узел публикации состояния в дерево преобразований `robot_state_publisher`, нам надо глубже копнуть в информацию об узле управления, для этого есть команда `info`:

```bash
rosnode info /robot_state_publisher
```

Вывод

```md
Node [/robot_state_publisher]
Publications: 
 * /rosout [rosgraph_msgs/Log]
 * /tf [tf2_msgs/TFMessage]
 * /tf_static [tf2_msgs/TFMessage]

Subscriptions: 
 * /joint_states [sensor_msgs/JointState]
```

Разберём-с, узел имеет "Publications" и "Subscriptions". Что-то публикуется и на что-то он подписывается. Вот тут мы начинаем пересекаться с понятием **топика**. Пойдём разберёмся с ним!

## Каналы передачи данных - топики

Давай взглянем на то, как организовано общение между узлами в ROS:

<p align="center">
    <img src=../assets/ros_topics/1_nodes_topics_animation.gif />
</p>

В ROS каждый узел выполняет свою задачу, но они не могут работать без коммуникации между собой. Так вот топики - это один из способов общения между узлами. Как видно на анимации, узлы могут *публиковать в топики* (Publication - отправлять через него данные) и *подписываться на топики* (Subscription - получать через него данные).

Ну, а в нашем примере, `/robot_state_publisher` подписывается на `/joint_states`, а публикует в `/tf`, `/tf_static` и `/rosout`.

Если `/rosout` - это сервисный топик, то `/tf` и `/tf_static`, полагаем, отправляет интересную информацию!

Давай проанализируем топики в системе с помощью утилиты `rostopic` и команды `list`:

```bash
rostopic list
```

Вот видим в выводе много разных топиков и в частности:

```md
...
/tf
/tf_static
...
```

Ну, просто получить список полезно, но мы также можем и получить информацию о конкретном топике командой `info`:

```bash
rostopic info /tf
```

Вывод:

```md
Type: tf2_msgs/TFMessage

Publishers: 
 * /robot_state_publisher (http://msi-leopard-156:43231/)

Subscribers: 
 * /move_group (http://msi-leopard-156:38065/)
```

Вот так мы можем видеть, что узел публикации подтвердился, `/robot_state_publisher`, а ещё мы увидели, кто подписался на топик, `/move_group` - основной узел Move_it!






Давай теперь сами подпишемся на топик и посмотрим, какая информация ходит через него?

```bash
rostopic echo /cmd_vel
```

И у нас непрерывно покатился вывод:

```md
...
linear: 
  x: 0.0
  y: 0.0
  z: 0.0
angular: 
  x: 0.0
  y: 0.0
  z: 0.0
...
```

А вот это уже интересно, давай попробуем поуправлять в терминале телеуправления и параллельно смотреть на вывод из подписки /cmd_vel:

<p align="center">
<img src=../assets/01_05_topic_cmd_vel_values.gif />
</p>

Смотри, значения меняются! Значит, через этот топик передаётся информация о команде на движение. Если более конкретно, то через `linear/x` поле передаётся желаемая линейная скорость, а через `angular/z` - команда на скорость поворота.

> ! Таким образом, топик - это канал передачи потоковой информации (так как передаем непрерывно). Данные внутри передаются с определённой структурой, которая регламентирована **типом сообщения у топика**. Это видно и на картинке, а в нашем случае `/cmd_vel` имеет тип "geometry_msgs/Twist". О каждом типе можно почитать в [справке](http://docs.ros.org/en/noetic/api/geometry_msgs/html/msg/Twist.html) или через команду `rosmsg show geometry_msgs/Twist`.

Для аналогии можно привести конвеерную ленту, через которые передаются коробки конкретной формы и размера. информацию о коробке позволяет получить утилита `rosmsg`.

> :muscle: Посмотри, из каких подтипов состоит сообщение `geometry_msgs/Twist` (`geometry_msgs/Vector3`). Найди информацию об этом типе в справке и в `rosmsg`.

А каким образом определить частоту передачи этого потока? Ведь в поток публикуется с каким-то периодом, мы же все знаем про дискретные системы. Попробуй разобраться самостоятельно:

> :muscle: Определи команду у `rostopic`, которая позволяет вывести частоту публикации в топик.

Вот так мы в общих чертах познакомились с узлами и топиками, но это были цветочки, а теперь будут ягодки!

## RQT Graph

Это всё хорошо, но погодите, нам каждый раз, когда хотим посмотреть как и куда направляется информация, надо по каждому топику и узлу выводить информацию?

Отличный вопрос, конечно же нет! Для этого сделана удобная утилита `rqt_graph`, которая показывает, как и через что связаны узлы, проверим:

```bash
rqt_graph
```

И видим:

<p align="center">
<img src=../assets/01_05_rqt_graph.png />
</p>

> Убедись,что настроено меню сверху вот так, иначе много лишних топиков показывается:

<p align="center">
<img src=../assets/01_05_rqt_graph_setup.png />
</p>

Сейчас у нас немного информации между узлами передается, но в сложных системах такие диаграммы позволяют найти ситуации очепяток и других проблем, которые не дают системе нормально работать.

Вот такой простой и удобный инструмент!