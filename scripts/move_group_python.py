# Импорты для совместимости Python 2/3
from __future__ import print_function
from six.moves import input

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

try:
    from math import pi, tau, dist, fabs, cos
except:  # Совместимость с Python 2
    from math import pi, fabs, cos, sqrt

    tau = 2.0 * pi

    def dist(p, q):
        return sqrt(sum((p_i - q_i) ** 2.0 for p_i, q_i in zip(p, q)))


from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

# Инициализация moveit_commander и узла rospy
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node("move_group_python_interface_tutorial", anonymous=True)

# Создание объекта RobotCommander
# Этот объект предоставляет информацию о кинематической модели робота и текущих состояниях суставов
robot = moveit_commander.RobotCommander()

# Создание объекта PlanningSceneInterface
# Этот объект предоставляет удаленный интерфейс для работы с внутренним пониманием окружающего мира
scene = moveit_commander.PlanningSceneInterface()

group_name = "panda_arm"           #С каким ты роботом работаешь? 
move_group = moveit_commander.MoveGroupCommander(group_name)

display_trajectory_publisher = rospy.Publisher(     #мы-топик, не майка
    "/move_group/display_planned_path",
    moveit_msgs.msg.DisplayTrajectory,
    queue_size=20,
)

planning_frame = move_group.get_planning_frame() #Имя опорного кадра робота
print("============ Planning frame: %s" % planning_frame)

eef_link = move_group.get_end_effector_link() #Имя звена конечного эффектора
print("============ End effector link: %s" % eef_link)

group_names = robot.get_group_names()  #Список всех групп планирования робота
print("============ Available Planning Groups:", robot.get_group_names())

print("============ Printing robot state") #Текущее состояние робота:
print(robot.get_current_state())
print("")




