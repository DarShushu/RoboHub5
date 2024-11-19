<!-- omit from toc -->
# Roslaunch and Params

## Содержание

- [Содержание](#содержание)
- [Распространенные практики](#распространенные-практики)
  - [Объединение узлов под одним пространством имен](#объединение-узлов-под-одним-пространством-имен)
  - [Мапирование топиков](#мапирование-топиков)
  - [Подключение других launch-файлов](#подключение-других-launch-файлов)
  - [Создание опций для launch-файлов](#создание-опций-для-launch-файлов)
- [ROS параметры](#ros-параметры)
- [Управление параметрами](#управление-параметрами)
- [С чем познакомились?](#с-чем-познакомились)
- [Полезные ресурсы](#полезные-ресурсы)


Помните, когда мы делали с вами прошлую урок, вы сталкивались с тем, что каждый узел нужно запускать в разных терминалах? Но мы с вами запускали по 2-3 узла, а что будет, если нужно одновременно запустить больше таких? Ведь в реальных системах может присутствовать 10, 20 и более узлов, что может вызвать огромную боль при включении/выключении/проверке всех узлов. Звучит как-то не очень...

Для облегчения жизни придумали специальный формат, основанный на формате `xml`. Суть данного формата в том, что он позволяет настраивать и запускать группы узлов. Это еще можно назвать скриптом запуска.

Для начала, попробуем рассмотреть простой launch-файл (так они называются; угадайте, как должна называться папка, в которой они хранятся =) ).

```xml
<launch>
    <node name="listener" pkg="rospy_tutorials" type="listener.py" output="screen"/>
    <node name="talker" pkg="rospy_tutorials" type="talker.py" output="screen"/>
</launch>
```

> Раньше мы запускали узел `talker`, указывая `rosrun rospy_tutorials talker`. Когда мы пишем на Python, мы создаем скрипты `.py`. Так что оригинально при работе с Python запускаемые файлы будут с расширением `.py`. А в пакете `rospy_tutorials` разработчики просто скопировали файл `talker.py` в `talker`. Можете убедиться сами, у них размер одинаковый.

Основа launch-файла лежит в тэге `<launch>`, он оборачивает весь файл. Далее вложенные тэги `<node>` задают запуск узлов. В качестве параметров тэгов указываются:

- `name` - имя, которое присваивается узлу в системе ROS (аналог `__name`)
- `pkg` - название пакета, внутри которого лежит узел
- `type` - название файла узла внутри пакета (для Pyhton - py-файлы, для C++ - исполняемые файл, там уж как назовете при компиляции)
- `output` - (необязательный) режим вывода информации, есть варианты `screen` (в консоль) и `log` (по-умолчанию, в лог-файл)

> При запуске launch-файла также запускается мастер (roscore), если он не был запущен ранее. Таким файлом из примера удобно пользоваться, так как вместо трех консолей потребуется единственная, в которую будет выкладываться вывод всех узлов, у которых `output="screen"`.

Кстати, такой файл уже есть в пакете `rospy_tutorials`, прочитать его можно командой:

```bash
roscat rospy_tutorials talker_listener.launch
```

Утилита для запуска называется `roslaunch` и вот пример запуска такого файла из пакета `rospy_tutorials`:

```bash
roslaunch rospy_tutorials talker_listener.launch
```

Выключение всех узлов из файла производится нажатием Ctrl+C в терминале, в котором запускали launch-файл. При этом система launch проверяет, что все узлы завершились.

> 💪 Напишите launch-файл `my_first.launch` с таким же содержанием и запустите его. Для этого нужно в пакете создать папку `launch` и в ней создать файл с расширением launch. Сделайте небольшую поправочку - измените имена узлов на `sender` и `receiver`. С помощью утилиты `roslaunch`  запустите файл из своего пакета `study_pkg` и убедитесь, что все работает.

## Распространенные практики

А теперь поговорим о наиболее применяемых практиках относительно launch-файлов.

### Объединение узлов под одним пространством имен

Допустим мы хотим запустить узлы в одном пространстве имен, так как они выполняют определенную задачу (являются подсистемой). Можно это сделать красиво с помощью тэга `<group>` и параметра `ns`:

```xml
<launch>
    <group ns="my_namespace">
        <node name="listener" pkg="rospy_tutorials" type="listener.py" output="screen"/>
        <node name="talker" pkg="rospy_tutorials" type="talker.py" output="screen"/>
    </group>
</launch>
```

> 💪 Объедините запускаемые узлы в файле `my_first.launch` в пространство `new_ns`.

### Мапирование топиков

Часто неоходимо переименовать (мапировать) топики узлов. Делается это тэгами `<remap>` внутри тэга `<node>` и параметрами `from` и `to`:

```xml
<launch>
    <node name="listener" pkg="rospy_tutorials" type="listener.py" output="screen">
        <remap from="chatter" to="my_topic"/>
    </node>
    <node name="talker" pkg="rospy_tutorials" type="talker.py" output="screen">
        <remap from="chatter" to="my_topic"/>
    </node>
</launch>
```

> 💪 Смапируйте запускаемые узлы в файле `my_first.launch` к топику `new_topic`.

### Подключение других launch-файлов

Иногда можно написать много простых launch-файлов и запустить все их с помощью одного launch-файла. Для этого существует тэг `<include>`:

```xml
<launch>
    <include file="$(find study_pkg)/launch/otherfile.launch" />
    <node name="listener" pkg="rospy_tutorials" type="listener.py" output="screen"/>
    <node name="talker" pkg="rospy_tutorials" type="talker.py" output="screen"/>
</launch>
```

Директива `(find study_pkg)` ищет пакет, имя которого передано аргументом (в нашем случае ищется путь до пакета `study_pkg`) и подставляет путь до него в случае удачного нахождения. Таким образом выполняется сначала launch-файл `otherfile.launch`, а затем остальное содержимое. Уровни вложенности launch-файлов не ограничены (насколько я знаю).

> 💪 Напишите launch-файл `another_one.launch` и добавьте его запуск в `my_first.launch` под пространством имен `new_ns`. Launch-файл `another_one.launch` должен запускать узел `listener` из пакета `roscpp_tutorials`, иметь имя `listener_cpp` и смапировать топик `chatter` к `new_topic`.

### Создание опций для launch-файлов

Иногда создание опреленной системы упрощается, если при запуске существует возможность передать опции файлу запуска. Для launch-файлов существует тэг `<arg>`, который добавляет аргументы launch-файлу:

```xml
<launch>
    <arg name="new_topic_name" default="new_chatter" />

    <node name="listener" pkg="rospy_tutorials" type="listener.py" output="screen">
        <remap from="chatter" to="$(arg new_topic_name)"/>
    </node>
    <node name="talker" pkg="rospy_tutorials" type="talker.py" output="screen">
        <remap from="chatter" to="$(arg new_topic_name)"/>
    </node>
</launch>
```

❔ Директива `(arg new_topic_name)` подставляет значение аргумента. При наличии параметра `default` в тэге `<arg>` установка параметра при запуске launch-файла не обязательна. Для задания значения аргумента выполнение roslaunch происходит следующим образом:

> 💪 Добавьте аргумент имени топика, через который общаются узлы в файле `my_first.launch`. При запуске задайти имя топика `my_topic`. Посмотрите результат в `rqt_graph`.

## ROS параметры

Есть еще один аспект, который называется сервер параметров.

❗ **Параметрами** в ROS называются просто данные, которые хранятся под определенными именами и пространствами имен. Как было рассмотрено ранее, запуск узла в пространстве имен меняет конечное имя узла, а также топика. Аналогично с этим, вся работа узла с параметрами (чтение, запись) происходит в том пространстве имен, которому он принадлежит.

> Сервер параметров хранит параметры и привязан к мастеру. Перезапуск мастера приводит к потере всех ранее заданных параметров.

Пора знакомиться с основной утилитой работы с параметрами =)

```bash
rosparam help
```

```
rosparam is a command-line tool for getting, setting, and deleting parameters from the ROS Parameter Server.

Commands:
    rosparam set    set parameter
    rosparam get    get parameter
    rosparam load   load parameters from file
    rosparam dump   dump parameters to file
    rosparam delete delete parameter
    rosparam list   list parameter names
```

Попробуем проверить список параметров в системе

```bash
rosparam list
```

```
/rosdistro
/roslaunch/uris/host_user_vb__35559
/rosversion
/run_id
```

Давайте поработаем с параметром /rosdistro

```bash
rosparam get /rosdistro
```

```
noetic
```

Удивительно, правда? =)

А теперь попробуем задать свой параметр и сразу прочитать его

```bash
rosparam set /my_param 'Hello =)'
rosparam set /my_set '{ 'P': 10.0, 'I': 1.0, 'D' : 0.1 }'

rosparam get /my_param
rosparam get /my_set
rosparam get /my_set/P
```

Результат:

```
Hello =)
{D: 0.1, I: 1.0, P: 10.0}
10.0
```

Вроде все логично! А теперь попробуйте перезапустить ячейку с выводом списка параметров в системе.

Как видно из вывода хелпа, параметрами также можно управлять, удаляя их, также выгружать в файл и загружать из файла.

## Управление параметрами

Сейчас хочется обратить внимание на приватные параметры с точки зрения практики. Параметры обычно прописываются в узлах, а они в свою очередь стартуют с помощью launch-файлов, поэтому задаются параметры внутри с помощью тэгов `<param>`. Пример из одного из файлов планера:

Давайте теперь рассмотрим `launch-файл`, который позволяет стартануть драйвер web-камеру, с которой вы уже работали

```xml
<launch>
  <node name="usb_cam" pkg="usb_cam" type="usb_cam_node" output="screen" >
    <param name="video_device" value="/dev/video0" />
    <param name="image_width" value="640" />
    <param name="image_height" value="480" />
    <param name="pixel_format" value="yuyv" />
    <param name="color_format" value="yuv422p" />
    <param name="camera_frame_id" value="usb_cam" />
    <param name="io_method" value="mmap"/>
  </node>
  <node name="image_view" pkg="image_view" type="image_view" respawn="false" output="screen">
    <remap from="image" to="/usb_cam/image_raw"/>
    <param name="autosize" value="true" />
  </node>
</launch>
```

Обратим внимание, что внутри тэга `<node>` параметры задаются приватными!:

```xml
  <node name="usb_cam" pkg="usb_cam" type="usb_cam_node" output="screen" >
    <param name="video_device" value="/dev/video0" />
    <param name="image_width" value="640" />
    <param name="image_height" value="480" />
    <param name="pixel_format" value="yuyv" />
    <param name="color_format" value="yuv422p" />
    <param name="camera_frame_id" value="usb_cam" />
    <param name="io_method" value="mmap"/>
  </node>
```

Здесь с помощью параметров задается путь девайса (конкретный, так как таких может быть много), размеры выходного изображения и в каком виде он будет нам демонстрироваться.

## С чем познакомились?

- Разобрались с утилитой `roslaunch` и рассмотрели ряд тэгов, используемых в формате `XML`.
- Мы познакомились с сервером параметров и утилитой работы с параметрами
- Рассмотрели практические применения утилит и параметров в `roslaunch`, в том числе познакомились с утилитой `rosparam`
  
## Полезные ресурсы

- [XML](http://wiki.ros.org/roslaunch/XML)
- [Сервер параметров](http://wiki.ros.org/Parameter%20Server)
- [Cтраница из туториала про параметры](http://wiki.ros.org/rospy_tutorials/Tutorials/Parameters)
- [API rospy](http://docs.ros.org/api/rospy/html/)
- [Полезная ссылка](http://wiki.ros.org/roslaunch/XML/include)
