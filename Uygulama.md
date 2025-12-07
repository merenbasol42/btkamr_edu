<h1>Uygulamalar</h3>

**0. [Robotik Kol Modeli](#hid-0)**
**1. [Robot Modelinin Çıkarımı](#hid-1)**
**2. [Gazebo Launcher'ı Oluşturumu]()**
**3. [Diferansiyel Sürüş Plugini Eklenmesi]()**
**3. [Klavye Kontrol (teleop keyboard)]()**
**4. [Lidar Sensörünün Eklenmesi]()**
**5. [Genel Launcher Paket Düzenlemesi]()**
**6. [Odometri Plugini ve ROS2 Entegrasyonu]()**
**7. ['slam_toolbox' İle Haritalama]()**
**8. ['nav2' İle Haritalama Çalışması]()**
**9. ['nav2' İle Basit Uygulama]()**

---

<h1 id="hid-0">0. Robotik Kol Modeli </h1>

<div align="center">
    <img src="./images/practices/uygulama-0-1.gif">
</div>  

#### Adım 1:

Yukarıdaki görselde gözüken robot kol modelini çıkarınız.
<details>
    <summary>çözümü görmek için tıklayın</summary>

```xml
<?xml version="1.0"?>

<robot name="robot_kol">

    <material name="red">
        <color rgba="1 0 0 1" />
    </material>

    <material name="green">
        <color rgba="0 1 0 1" />
    </material>

    <material name="blue">
        <color rgba="0 0 1 1" />
    </material>

    <link name="base_link">
    </link>

    <joint name="base_link_TO_rail" type="fixed">
        <parent link="base_link" />
        <child link="rail" />
        <origin xyz="0 0 0" rpy="0 0 0" />
    </joint>

    <link name="rail">
        <visual>
            <origin xyz="0 0 0" rpy="0 0 0" />
            <geometry>
                <box size="0.4 0.2 0.05" />
            </geometry>
            <material name="blue"/>
        </visual>
    </link>

    <joint name="rail_TO_slider" type="prismatic">
        <parent link="rail" />
        <child link="slider" />
        <origin xyz="0 0 0.035" rpy="0 0 0" />
        <axis xyz="1 0 0" />
        <limit lower="-0.175" upper="0.175" effort="100" velocity="100" />
    </joint>

    <link name="slider">
        <visual>
            <origin xyz="0 0 0" rpy="0 0 0" />
            <geometry>
                <box size="0.1 0.1 0.02" />
            </geometry>
            <material name="red"/>
        </visual>
    </link>

    <joint name="slider_TO_first_arm" type="fixed">
        <parent link="slider" />
        <child link="first_arm" />
        <origin xyz="0 0 0.12" rpy="0 0 0" />
    </joint>

    <link name="first_arm">
        <visual>
            <origin xyz="0 0 0" rpy="0 0 0" />
            <geometry>
                <cylinder radius="0.02" length="0.2" />    
            </geometry>
            <material name="green"/>
        </visual>
    </link>

    <joint name="first_arm_TO_second_arm" type="revolute">
        <parent link="first_arm" />
        <child link="second_arm" />
        <origin xyz="0 0 0.1" rpy="0 0 0" />
        <axis xyz="0 1 0" />
        <limit lower="0.0" upper="1.57" effort="100" velocity="100" />
    </joint>

    <link name="second_arm">
        <visual>
            <origin xyz="0 0 0.1" rpy="0 0 0" />
            <geometry>
                <cylinder radius="0.02" length="0.2" />    
            </geometry>
            <material name="red"/>
        </visual>
    </link>
</robot>
```
</details>

#### Adım 2:

<div align="center">
    <img src="./images/practices/uygulama-0-2.gif">
</div>  

Yaptığınız robot kola, görselde gözüktüğü gibi bir adet tutucu ekleyin (resources klasörünün altında gripper.stl mesh'ini kullanabilirsiniz.)

<details>
    <summary>Çözümü görmek için tıklayın</summary>

```xml
<?xml version="1.0"?>

<robot name="robot_kol">

    <material name="red">
        <color rgba="1 0 0 1" />
    </material>

    <material name="green">
        <color rgba="0 1 0 1" />
    </material>

    <material name="blue">
        <color rgba="0 0 1 1" />
    </material>

    <material name="yellow">
        <color rgba="1 1 0 1" />
    </material>

    <link name="base_link">
    </link>

    <joint name="base_link_TO_rail" type="fixed">
        <parent link="base_link" />
        <child link="rail" />
        <origin xyz="0 0 0" rpy="0 0 0" />
    </joint>

    <link name="rail">
        <visual>
            <origin xyz="0 0 0" rpy="0 0 0" />
            <geometry>
                <box size="0.4 0.2 0.05" />
            </geometry>
            <material name="blue"/>
        </visual>
    </link>

    <joint name="rail_TO_slider" type="prismatic">
        <parent link="rail" />
        <child link="slider" />
        <origin xyz="0 0 0.035" rpy="0 0 0" />
        <axis xyz="1 0 0" />
        <limit lower="-0.175" upper="0.175" effort="100" velocity="100" />
    </joint>

    <link name="slider">
        <visual>
            <origin xyz="0 0 0" rpy="0 0 0" />
            <geometry>
                <box size="0.1 0.1 0.02" />
            </geometry>
            <material name="red"/>
        </visual>
    </link>

    <joint name="slider_TO_first_arm" type="fixed">
        <parent link="slider" />
        <child link="first_arm" />
        <origin xyz="0 0 0.12" rpy="0 0 0" />
    </joint>

    <link name="first_arm">
        <visual>
            <origin xyz="0 0 0" rpy="0 0 0" />
            <geometry>
                <cylinder radius="0.02" length="0.2" />    
            </geometry>
            <material name="green"/>
        </visual>
    </link>

    <joint name="first_arm_TO_second_arm" type="revolute">
        <parent link="first_arm" />
        <child link="second_arm" />
        <origin xyz="0 0 0.1" rpy="0 0 0" />
        <axis xyz="0 1 0" />
        <limit lower="0.0" upper="1.57" effort="100" velocity="100" />
    </joint>

    <link name="second_arm">
        <visual>
            <origin xyz="0 0 0.1" rpy="0 0 0" />
            <geometry>
                <cylinder radius="0.02" length="0.2" />    
            </geometry>
            <material name="red"/>
        </visual>
    </link>

    <joint name="second_arm_TO_gripper" type="fixed">
        <parent link="second_arm" />
        <child link="gripper" />
        <origin xyz="0 0 0.2" rpy="0 0 0" />
    </joint>

    <link name="gripper">
    </link>

    <joint name="gripper_TO_gripper_right" type="revolute">
        <parent link="gripper" />
        <child link="gripper_right" />
        <origin xyz="0 0 0" rpy="0 0 0" />
        <axis xyz="-1 0 0" />
        <limit lower="0.0" upper="0.7" effort="100" velocity="100" />
    </joint>

    <link name="gripper_right">
        <visual>
            <origin xyz="0.015 -0.00 0.06" rpy="0 -1.57 0" />
            <geometry>
                <mesh filename="file:///home/meren/Projects/btkamr_edu/alistirma/gripper.stl" scale="0.005 0.005 0.005"/>
            </geometry>
            <material name="yellow"/>
        </visual>
    </link>

    <joint name="gripper_TO_gripper_left" type="revolute">
        <parent link="gripper" />
        <child link="gripper_left" />
        <origin xyz="0 0 0" rpy="0 0 0" />
        <axis xyz="1 0 0" />
        <limit lower="0.0" upper="0.7" effort="100" velocity="100" />
    </joint>

    <link name="gripper_left">
        <visual>
            <origin xyz="-0.015 0.00 0.06" rpy="0 -1.57 3.1415" />
            <geometry>
                <mesh filename="file:///home/meren/Projects/btkamr_edu/alistirma/gripper.stl" scale="0.005 0.005 0.005"/>
            </geometry>
            <material name="yellow"/>
        </visual>
    </link>


</robot>
```

</details>


<h1 id="hid-1">1. Robot Modelinin Çıkarımı </h1>

Diferansiyel sürüşe uygun bir robot tasarlayın. İstediğiniz şekilde olabilir. Yeterki diferansiyel sürüş dinamiğine uygun olsun.

<details>
    <summary>Çözümü görmek için tıklayın</summary>

    ayıp :(
</details>