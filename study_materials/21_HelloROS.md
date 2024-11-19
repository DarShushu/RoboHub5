# Я, ROS и мой первый пакет (не из пятерочки)

## Содержание

- [Я, ROS и мой первый пакет (не из пятерочки)](#я-ros-и-мой-первый-пакет-не-из-пятерочки)
  - [Содержание](#содержание)
  - [Что нужно, чтобы начать?](#что-нужно-чтобы-начать)
  - [Основная информация](#основная-информация)
  - [Рабочие-пространства](#рабочие-пространства)
    - [Подготовка рабочего пространства (workspace -\> ws)](#подготовка-рабочего-пространства-workspace---ws)
      - [Добавить подключение рабочего пространства в сессию терминала](#добавить-подключение-рабочего-пространства-в-сессию-терминала)
    - [Проверка установки](#проверка-установки)
    - [Пространство готово - теперь создаем пакет](#пространство-готово---теперь-создаем-пакет)
    - [Сборка пакета](#сборка-пакета)
    - [Разместим новый пакет в репозиторий на GitHub](#разместим-новый-пакет-в-репозиторий-на-github)
    - [Первый узел](#первый-узел)
    - [Залить наработки в конце работы](#залить-наработки-в-конце-работы)
  - [С чем познакомились?](#с-чем-познакомились)
  - [Полезные ресурсы](#полезные-ресурсы)

## Что нужно, чтобы начать? 

- Установленная [Ubuntu 20.04 LTS](https://releases.ubuntu.com/20.04/)
- Установленный [ROS Noetic](https://wiki.ros.org/noetic/Installation/Ubuntu)
- Установленный пакет `git`
- Созданный аккаунт на GitHub
- Готовность к изучению нового и интересного =)

## Основная информация
> **Что такое ROS?**
 - **ROS** (Операционная система роботов) — это открытая платформа для разработки программного обеспечения для роботов. Она предоставляет инструменты, библиотеки и фреймворки, которые помогают разработчикам создавать сложные и модульные системы для робототехники.
 
Пример для простоты понимания:
Представьте себе робота. У него есть:

- камеры
- радары
- датчик GPS
- инерциальный модуль

Это очень "умный" робот, но чтобы он работал, нужно:

- Собирать данные со всех его датчиков.
- Обрабатывать эти данные.
- Передавать эти данные системе управления.

Здесь нам на помощь и приходит ROS. Он позволяет объединить и "подружить" данные от разных датчиков, обработать их и отправить дальше — всё это в единой системе!

Для понимания принципа работы нам нужно рассмотреть главные элементы: 

- Узлы (Узлы): Программы, которые решают отдельные задачи, например, считывают данные с датчиков или управляют моторами (Проще говоря занимаются обработкой данных).
- Топики (Topics): Каналы, через которые узлы получают и передают данные (Занимаются передачей данных).

Топики можно сравнивать с переменными, которые хранят информацию и передают ее между узлами. У них, как и у переменных, есть формат данных, который определяет, что можно в них записывать или читать. 

Пример:
<p align="center">
<img src="../assets/ros/ROS_Shemas_0_2.jpg" width=400>
</p>

На данной схеме показан лишь небольшой фрагмент системы для нашего робота, который помогает ему определить свое текущее местоположение (модуль позиционирования). Каждый датчик на роботе работает через свой драйвер, публикуя данные в отдельный топик. Например, драйвер GPS запускает узел (узел 1), который определяет географические координаты, такие как широта и долгота, и отправляет (публикует) их в определенный топик (топик 1). Параллельно геоданные определяет инерциальный модуль, который также при помощи своего драйвера (узел 2) публикует их в своем топике (топик 2). Для обработки этих данных мы создали третий узел, который берет данные из топиков 1 и 2 (слушает их), фильтрует и корректирует информацию, а затем публикует уточненные геоданные в своем новом топике (топик 3). Таким образом, мы собрали данные с двух датчиков, обработали их, убрали все ошибки в данных и отправили дальше в систему. Эти данные могут быть использованы, например, в узле, отвечающем за планирование маршрута, или в любом другом. Таким образом, мы связываем все датчики в единую систему, которая собирает данные, обрабатывает и выдает управление нашему роботу.

## Рабочие-пространства

Чтобы нам делать такие системы нам сначала нужно правильно создать место, где мы будем работать.
Такое место называется **рабочим пространством**. Давайте посмотрим на его структуру.

<p align="center">
<img src="../assets/ros/ROS_Shemas_0_1.jpg" width=500>
</p>

- **Рабочее пространство**- база для нашего дальнейшего програмирования, папка, в которой храняться все наши проекты. Рабочих пространст может быть несколько, но пока не забивайте себе голову. Несколько рабочих пространств вам понадобится не скоро.
- **Src**- наиболее интересующая нас папка в рабочем пространстве, ведь в ней хранятся **ПАКЕТЫ**. Вы спросите, что за пакеты? Так как мы в Петербурге могу уверенно сказать, что в этих пакетах вся "соль" нашей работы. Пакеты прикопаны в корнях нашего рабочего пространства именно в папке Src.
    
Пакеты- хранят в себе набор скриптов и лаунчей (о них поговорим попозже), которые как раз и запускают наши узлы и топики. Проще говоря- это все что нужно нам для запуска проекта.  
Возвращаясь к роботуь - наши драйвера и узлы преобразователей могли бы храниться в одном пакете.


> **Пакет** - это набор файлов, объединенных единым смыслом или задачей. Например, пакет драйвера для камеры, пакет для подключения джойстика, пакет колесного робота и т.д.

Пакетов в интернете очень много мы можем их качать и запускать, но для начала нам нужно создать наше рабочее пространство. Этим и займемся!

### Подготовка рабочего пространства (workspace -> ws)

> Для работы с собственным рабочим пространством (использование утилит `catkin_make` и др.) должно быть подключено системное рабочее пространство.

ROS видит пакеты только в рабочем пространстве, поэтому нам необходимо создать собственный **ws** для работы с ним. Можно подглядеть в [исходную инфу на офф сайте](http://wiki.ros.org/catkin/Tutorials/create_a_workspace), а можно сделать следующие шаги:

Во-первых, создаем папочку, которая будет нашим ws. Назовем ее `catkin_ws`:

```bash
mkdir -p ~/catkin_ws/src
```

> Опция `-p` указывает, что нужно создать полный путь, даже если каких-то папок в пути нет.

В нашем случае папки `catkin_ws` нет, так что создаем весь путь с опцией `-p`. `src` папку внутри надо создавать, чтобы потом туда размещать исходные коды. Делаем два действия одной командой =)

После этого переходим в корень ws и вызываем утилиту сборки (так нужно в первый раз инициализировать ws):

```bash
cd ~/catkin_ws
catkin_make
```

> Обрати внимание что команда **catkin_make** аналогична для любого названия рабочега пространства и не связана с его названием (как и все команды catkin). Например сборка рабочего пространства first_ws будет осуществляться этой же командой.

На этом этапе в нашем рабочем пространстве появятся папки:  
- **build** : Папка для сборки временных файлов.
- **devel** : Папка с результатами сборки, такими как исполняемые файлы и скрипты.

Рабочее пространство готово и осталось добавить в файл `~/.bashrc` (этот файл выполняется при каждом запуске терминала) строку для автоматической настройки ROS на подключение нашего ws:

#### Добавить подключение рабочего пространства в сессию терминала

Для этого нам нужно открыть файл `~/.bashrc` и прописать ручками

```bash
source ~/catkin_ws/devel/setup.bash
```
❓ Сейчас должен возникнуть вопрос, что это за файл `~/.bashrc` и как нам его найти на нашем компьютере?

Файл `~/.bashrc` — это конфигурационный файл для оболочки **Bash**, который выполняется каждый раз, когда вы открываете новую сессию терминала. Он используется для настройки среды, в которой работает ваша оболочка, и может содержать различные команды, такие как экспорт переменных окружения, настройка алиасов и выполнение других скриптов.

Найти его достаточно просто, для этого нам нужно зайти в `HOME` и нажать на галочку около `Show hidden files` (это в вверхнем правом углу)

### Проверка установки

После перезапуска терминалов (для настройки сессий) (это, кстати, можно сделать просто командой `bash` в терминале, то есть не обязательно закрывать) можно проверить установку всех **ws**

```bash
echo $ROS_PACKAGE_PATH
```

В результате должен появиться путь до созданного рабочего простанства, а также путь до системного рабочего пространства. То есть, строка должна содержать результат, похожий на вот это:

```bash
/home/user/catkin_ws/src:/opt/ros/noetic/share
```

> Часто переменные окружения содержат список путей. А разделителем списка является символ '`:`'.

Как видно, первый путь является путем до нового ws, а второй - до системного.

### Пространство готово - теперь создаем пакет

Вся экосистема ROS основывается на концепции пакетов, которые включают различные компоненты. В этом топике мы знакомимся с возможностями создания пакетов, их редактирования, а также c инструментом сборки, который будет использоваться далее. Можно также подглядеть на [оф страницу =)](http://wiki.ros.org/ROS/Tutorials/CreatingPackage).

Для начала перейдем в наш ws, в директорию `src`:

```bash
cd ~/catkin_ws/src
```

Для создания пакета используется команда:

```bash
catkin_create_pkg [pkg_name] [dep1 dep2 ...]
```

В данной команде первым аргументом передается имя нового пакета, после перечисляются зависимости данного пакета.

> Квадратные скобки указывают, что это аргументы команды и при подставлении своих значений квадратные скобки не нужны!

Для начала создадим пакет и добавим поддержку библиотек python (rospy):

```bash
catkin_create_pkg study_pkg rospy
```

Далее наблюдаем созданную папку `study_pkg` и два главных файла внутри: `CMakeLists.txt` и `package.xml`

В содержании `package.xml` можно выделить основные блоки:  

Заголовок, в нем содержится основная инфа о пакете

```xml
<?xml version="1.0"?>
<package format="2">
  <name>study_pkg</name>
  <version>0.0.0</version>
  <description>The study_pkg package</description>
  <maintainer email="user@todo.todo">user</maintainer>
  <license>TODO</license>
```

Зависимости (инструмент сборки, сборка, экспорт, runtime (exec) - выполнение)

```xml
  <buildtool_depend>catkin</buildtool_depend>
  <build_depend>roscpp</build_depend>
  <build_depend>rospy</build_depend>
  <build_export_depend>roscpp</build_export_depend>
  <build_export_depend>rospy</build_export_depend>
  <exec_depend>roscpp</exec_depend>
  <exec_depend>rospy</exec_depend>
```

Остальное можно также наблюдать внутри комметариев формата xml. Там также приведены некоторые описания строк и блоков.

Внутри `CMakeLists.txt` можно также видеть много закомментированных блоков, но в основном можно вытащить базовые куски на момент инициализации:  

Определение минимальной версии сборки `cmake` и название проекта

```cmake
cmake_minimum_required(VERSION 3.0.2)
project(study_pkg)
```

Поиск и подключение зависимостей

```cmake
find_package(catkin REQUIRED COMPONENTS
  rospy
)
```

Также создается базовая папка `src` для файлов исходных текстов.  

### Сборка пакета

А теперь сделаем пакет видимым системе ROS - для этого надо просто вызвать сборку в корне рабочего пространства. Перейдите в папку рабочего пространства:

```bash
cd ~/catkin_ws
```

и выполните команду сборки:

```bash
catkin_make
```

После успешного выполнения сборки убедимся в том, что экосистема ROS видит наш пакет! Перезапустите терминал и проверяйте список пакетов в системе:

```bash
rospack list
```

В списке должна быть строка:

```bash
...
study_pkg /home/user/catkin_ws/src/study_pkg
...
```

С помощью команды `rospack help` можно получить информацию об утилите и ее аргументах.

> Вообще рекомендую не забывать этот аргумент `help` (или опцию `-h`), так как он применим ко всем утилитам ROS экосистемы.

### Разместим новый пакет в репозиторий на GitHub

Для начала необходимо создать новый репозиторий на [github.com](https://github.com/) в своем аккаунте. Если чего-то не хватает - разбираемся вместе или по инструкциям из веба, их благо достаточно. **Обязательно установите опцию "Add a README file", чтобы репозиторий не был пустым!**

> Можно глянуть как [инициализировать git с дальнейшими действиями](https://help.github.com/articles/adding-an-existing-project-to-github-using-the-command-line/).

После каждой команды `git *` рекомендую выполнять `git status`, чтобы видеть результат действий

Теперь перейдем в папку пакета `study_pkg`:

```bash
roscd study_pkg
```

Инициализируем папку как локальный git репозиторий и переключимся на ветку main (по новым правилам GitHub):

```bash
git init
git checkout -b main
```

Результат

```console
Initialized empty Git repository in /home/user/catkin_ws/src/study_pkg/.git/
```

Посмотрите состояние свежего репозитория командой:

```bash
git status
```

Теперь надо привязать локальный репозиторий к удаленному:

```bash
git remote add origin [Repo URL]
```

Repo URL - путь удаленного репозитория, берется со страницы репозитория из зеленой кнопки "Clone or download".
Например, для репозитория курса была использована следующая команда:

```bash
git remote add origin https://github.com/user/super_user_study_pkg.git
```

Как видно, в URL содержится имя владельца репозитория и его названия.

Настроим, чтобы ветка `main` локального репозитория следила за веткой `main` удаленного репозитория, для этого стянем все данные с ветки `main` удаленного репозитория (который при соединении в предыдущей команде мы назвали `origin`):

```bash
git pull origin main
```

> На удаленном репозитории ветка `main` называется `origin/main`

После этого можно учесть (индексировать) новые файлы пакета:

```bash
git add -A
```

> Опция `-A` добавляет все неучтенные файлы. Вместо нее можно просто перечислить файлы, которые необходимо добавить к учету в коммитах.

И сделать коммит в локальном репо:

```bash
git commit -am "First package commit"
```

> Опция `-a` делает `git add` ко всем изменениям учтенных (индексированных) файлов - упрощает нам задачу.

> Опция `-m` устанавливает коммент к коммиту. Коммент пишется после опции.

> ❔ Если гит не хочет делать коммит и пишет просьбу указать "Ты кто такой?" (почта и имя), глянь в [FAQ раздел](../FAQ.md#я-делаю-git-commit-а-он-хочет-e-mail-и-имя), он не любит работать с незнакомцами 😝

После остается только закинуть все сделанные коммиты (а их пока один штука) на удаленный репо:

```bash
git push --set-upstream origin main
```

> Для выполнения данной команды может потребоваться ввод имя пользователя и пароль (токен, инфа есть в [FAQ](../FAQ.md#как-делать-git-push-с-паролем)).

И все! Можно смотреть на результаты на сайте!

### Первый узел

Мы же тут не просто пакеты создавать собрались? Пора прогать! Да, это будет Hello World, но не просто программа, а целый узел!

Суть в том, что все программы в ROS называются узлами. Это как в графе, где узлы графа соединены ребрами. Так вот мы в будущем узнаем, что узлы действительно соединяются в ROS, но в качестве ребер выступают каналы связи!

Но сегодня наша цель - написать первый просто узел =) Начнем!

В Python есть разделение `.py` файлов на модули исходных кодов и модули исполняемых программ. Отличие простое - первые нужны для хранения логики программ, а вторые для описания процесса запуска программ.

Для исполняемых программ внутри пакета сделайте директорию `scripts` и в ней создайте файл `first_node.py`:

```bash
roscd study_pkg
mkdir scripts
touch scripts/first_node.py
```

После этого открываем любимый редактор и пишем в файле простой кусочек кода:

```python
def main():
    print(f"Hello ROS World!")


if __name__ == "__main__":
    main()
```

Отлично, пробуем стартануть с помощью команды `rosrun`, которой надо передать имя пакета и имя скрипта для запуска!

```bash
rosrun study_pkg first_node.py
```

Упс, ошибочка:

```console
[rosrun] Couldn't find executable named first_node below /home/user/catkin_ws/src/study_pkg
```

Что не так? ROS пытается запустить скрипт, но ему не хватает кое-чего!

Когда мы написали код в файле, то это просто текстовый файл, а чтобы запустить этого код, нужно сделать две вещи:

- Дать файлу права на исполнение;
- Прописать интерпретатор, с помощью которого будет запускаться скрипт

Права даются утилитой `chmod`:

```bash
chmod +x scripts/first_node.py
```

А для указания интерпертатор в начало файла первой строкой пропиши следующую строку:

```python
#!/usr/bin/env python3
```

> Эта строка указывает, чтобы запуск файла производился через интерпретатор `python3`.

Ну что, действия сделаны, пора проверить, заработает ли?

```bash
rosrun study_pkg first_node.py
```

И вот результат!

```console
Hello ROS World!
```

Отлично! Получилось, первый пакет с первым узлом готов! Отличное начало!

### Залить наработки в конце работы

После окончания работы на кодом нужно обязательно заливать наработки в репозиторий, чтобы их не потерять и всегда можно было стянуть последнюю версию даже с другой машины!

Нужно добавить новые файлы к индексу:

```bash
git add scripts/first_node.py
```

После этого сделать коммит:

```bash
git commit -am "My first node in ROS, hooray!"
```

> Над комментарием комита можно еще подумать =)

И отправить новые комиты на репозиторий:

```bash
git push
```

> Да-да, теперь без `--set-upstream` опции, так как этот репо уже связан с удаленным

Молодец!

## С чем познакомились?

- Концепция пакета и рабочего пространства
- `catkin_make`
- `catkin_create_pkg`
- `rospack`
- `git`
- `roscd`
- `rosrun`

## Полезные ресурсы

- [Официальная страничка](http://wiki.ros.org/ROS/Tutorials)
- [Рабочее пространство](http://wiki.ros.org/catkin/Tutorials/create_a_workspace)
- [Информация о файлах в пакете](http://wiki.ros.org/ROS/Tutorials/CreatingPackage)