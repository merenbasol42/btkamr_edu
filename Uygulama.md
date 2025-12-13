<h1>Uygulamalar</h3>

**0. [Robotik Kol Modeli](#hid-0)**
**1. [Robot Modelinin Çıkarımı](#hid-1)**
**2. [Gazebo Launcher'ı Oluşturumu](#hid-2)**
**3. [Diferansiyel Sürüş Plugini Eklenmesi](#hid-3)**
**4. [Klavye Kontrol (teleop keyboard)](#hid-4)**
**5. [Lidar Sensörünün Eklenmesi](#hid-5)**
**6. [Dünya Ve Model Ekleme](#hid-6)**
**7. [Odometri Plugini ve ROS2 Entegrasyonu](#hid-7)**
**8. ['slam_toolbox' İle Haritalama]()**
**9. ['nav2' İle Haritalama Çalışması]()**
**10. ['nav2' İle Basit Uygulama]()**

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

<div align="center">
    <img src="./images/practices/uygulama-1.png">
</div>  


Diferansiyel sürüşe uygun bir robot tasarlayın. İstediğiniz şekilde olabilir. Yeterki diferansiyel sürüş dinamiğine uygun olsun.

>* Workspace oluşturun 
>* İçine modelini taşıyacak bir paket açın
>* Paketin içine modelinizi oluşturun
>* Ayrıca modeli kontrol etmek için basit bir launch file oluşturun

<details>
    <summary>Çözümü görmek için tıklayın</summary>  

<br/>

Workspace oluşturun (Eğer yoksa)

```bash
mkdir btkamr_ws
mkdir btkamr_ws/src
```

Robot modeli için paket oluşturun

```bash
cd btkamr_ws/src
ros2 pkg create btkamr_description
```

Gereksiz klasörleri silebilirisiniz

```bash
rm -rf btkamr_description/src btkamr_description/include 
```

Paketin içine robot modelini ve launcherları taşıyacak klasörleri oluşturun

```bash
mkdir btkamr_description/urdf btkamr_description/launch
```

Şimdi Visual Studio Code'da çalışabiliriz.

Workspace dizinine gelelim ve Visual Studio Code'u başlatalım.

```bash
cd ..
code .
```

`CMakeList.txt` dosyasını düzenleyelim. Bundan sonra `urdf` ve `launch` klasörlerini de `share` dizinine taşısın.

```cmake
# ament_package() satırının hemen üstüne yapıştıralım

install(
    DIRECTORY urdf launch
    DESTINATION share/${PROJECT_NAME}/
)
```

Artık modeli oluşturmaya geçelim.

`urdf` klasörünün içine `main.urdf.xacro` isminde bir dosya oluşturalım.

Temel bir başlangıç yapalım.

```xml
<?xml version="1.0"?>

<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="btkamr">

    <link name="base_link"/>

</robot>
```

Renkleri ekleyelim.
```xml
<material name="red">
    <color rgba="1 0 0 1"/>
</material>

<material name="green">
    <color rgba="0 1 0 1"/>
</material>

<material name="blue">
    <color rgba="0 0 1 1"/>
</material>

<material name="gray">
    <color rgba="0.7 0.7 0.7 1"/>
</material>
```

Şasemizi ekleyelim

```xml
<xacro:property name="chasis_len_x" value="0.6"/>
<xacro:property name="chasis_len_y" value="0.4"/>
<xacro:property name="chasis_len_z" value="0.2"/>
<xacro:property name="base_chasis_offset" value="0.08"/>
<xacro:property name="chasis_mass" value="2.0"/>

<joint name="base_TO_chasis" type="fixed">
    <origin xyz="0.0 0.0 ${base_chasis_offset}" rpy="0.0 0.0 0.0"/>
    <parent link="base_link"/>
    <child link="chasis"/>
</joint>

<link name="chasis">
    <inertial>
        <mass value="${chasis_mass}"/>
        <inertia 
            ixx="${chasis_mass * (chasis_len_y * chasis_len_y + chasis_len_z * chasis_len_z) / 12.0}"
            iyy="${chasis_mass * (chasis_len_x * chasis_len_x + chasis_len_z * chasis_len_z) / 12.0}"
            izz="${chasis_mass * (chasis_len_x * chasis_len_x + chasis_len_y * chasis_len_y) / 12.0}"
            ixy="0" ixz="0" iyz="0"
        />
    </inertial>

    <visual>
        <geometry>
            <box size="${chasis_len_x} ${chasis_len_y} ${chasis_len_z}"/>
        </geometry>
        <material name="green"/>
    </visual>

    <collision>
        <geometry><box size="${chasis_len_x} ${chasis_len_y} ${chasis_len_z}"/></geometry>
    </collision>
</link>

```


Tahrik tekerleri için bir makro oluşturalım

```xml
<xacro:property name="wh_radius" value="0.1"/>
<xacro:property name="wh_thick" value="0.04"/>
<xacro:property name="wh_chasis_gap" value="0.001"/>
<xacro:property name="wh_mass" value="1.0"/>



<xacro:macro name="create_wh" params="postfix yfact">

    <joint name="base_TO_wh_${postfix}" type="continuous">
        <origin xyz="0.0 ${yfact * (chasis_len_y / 2.0 + wh_thick / 2.0 + wh_chasis_gap)} 0.0" rpy="0.0 0.0 0.0"/>
        <parent link="base_link"/>
        <child link="wh_${postfix}"/>
        <axis xyz="0.0 1.0 0.0"/>
    </joint>

    <link name="wh_${postfix}">
        <inertial>
            <origin xyz="0.0 0.0 0.0" rpy="${pi / 2.0} 0.0 0.0"/>

            <mass value="${wh_mass}"/>
            <inertia 
                ixx="${wh_mass * (3*wh_radius*wh_radius + wh_thick*wh_thick) / 12.0}"
                iyy="${wh_mass * (3*wh_radius*wh_radius + wh_thick*wh_thick) / 12.0}"
                izz="${wh_mass * (wh_radius*wh_radius) / 2.0}"
                ixy="0" ixz="0" iyz="0"
            />
        </inertial>

        <visual>
            <origin xyz="0.0 0.0 0.0" rpy="${pi / 2.0} 0.0 0.0"/>
            <geometry>
                <cylinder radius="${wh_radius}" length="${wh_thick}"/>
            </geometry>
            <material name="gray"/>
        </visual>

        <collision>
            <origin xyz="0.0 0.0 0.0" rpy="${pi / 2.0} 0.0 0.0"/>
            <geometry>
                <cylinder 
                    radius="${wh_radius}" 
                    length="${wh_thick}"/>
            </geometry>
        </collision>
    </link>

</xacro:macro>

```

Bu makroları kullanalım

``` xml
<xacro:create_wh postfix="l" yfact="1.0"/>
<xacro:create_wh postfix="r" yfact="-1.0"/>
```

Şimdi de avare tekerler için makro oluşturalım

```xml
<xacro:property name="cwh_chasis_offset_xy" value="0.1"/>
<!-- yarı çapı diğer niteliklere göre ayarlayalım -->
<xacro:property name="cwh_radius" value="${(wh_radius - (chasis_len_z / 2.0 - base_chasis_offset)) / 2.0}"/>
<xacro:property name="cwh_mass" value="0.00001"/>


<xacro:macro name="create_cwh" params="postfix xfact yfact">

    <!-- Yaw joint: x ekseni etrafında dönme -->
    <joint name="chasis_TO_cwh_${postfix}" type="fixed">
        <origin xyz="${xfact * (chasis_len_x / 2.0 - cwh_chasis_offset_xy)} 
                    ${yfact * (chasis_len_y / 2.0 - cwh_chasis_offset_xy)} 
                    ${-1 * (chasis_len_z / 2.0 + cwh_radius)}" rpy="0 0 0"/>
        <parent link="chasis"/>
        <child link="cwh_${postfix}"/>
    </joint>

    <!-- BALL CASTER LINK -->
    <link name="cwh_${postfix}">

        <!-- Çok hafif top (dönüşlerde robotu tutmaması için) -->
        <inertial>
            <mass value="0.01"/>
            <origin xyz="0 0 0"/>
            <inertia
                ixx="1e-5" ixy="0" ixz="0"
                iyy="1e-5" iyz="0"
                izz="1e-5"/>
        </inertial>

        <!-- Görsel -->
        <visual>
            <origin xyz="0 0 0" rpy="0 0 0"/>
            <geometry>
                <sphere radius="${cwh_radius}"/>
            </geometry>
            <material name="gray"/>
        </visual>

        <!-- Çarpışma ve sürtünme ayarları -->
        <collision>
            <origin xyz="0 0 0" rpy="0 0 0"/>
            <geometry>
                <sphere radius="${cwh_radius}"/>
            </geometry>
            <material name="gray"/>
        </collision>
    </link>

    <!-- gazebo için sürtünme değerlerini azaltıyoruz -->
    <gazebo reference="cwh_${postfix}">
        <collision>
            <surface>
                <friction>
                    <ode>
                        <mu>0.001</mu>    <!-- temel sürtünme -->
                        <mu2>0.001</mu2>  <!-- ikinci eksen sürtünmesi -->
                        <slip1>1.0</slip1>
                        <slip2>1.0</slip2>
                    </ode>
                </friction>
                <bounce>
                    <restitution_coefficient>0.0</restitution_coefficient>
                </bounce>
            </surface>
        </collision>
    </gazebo>

</xacro:macro>
```

Bu makroyu kullanalım

```xml
<xacro:create_cwh postfix="lf" xfact="1.0" yfact="1.0"/>
<xacro:create_cwh postfix="lb" xfact="-1.0" yfact="1.0"/>
<xacro:create_cwh postfix="rf" xfact="1.0" yfact="-1.0"/>
<xacro:create_cwh postfix="rb" xfact="-1.0" yfact="-1.0"/>
```

<br/>
<br/>
<br/>

Artık herşeyi yaptık. İsteğinize göre urdf kodlarını konumlandırıp `main.urdf.xacro` dosyasında include ederek kullanabilirsiniz.  

> Örneğin tekerler ile ilgili olan kodlar `wheels.urdf.xacro` isimli bir dosyada, şasi başka bir dosyada ve en son hepsi `main.urdf.xacro` dosyasında include edilerek kullanılabilir.  

Sonuç olarak şu şekilde toplam kodu şu şekilde özetleyebiliriz

`wheels.urdf.xacro`: 

```xml
<?xml version="1.0"?>

<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="btkamr">

    <!-- Tahrik Teker Nitelikleri  -->

    <xacro:property name="wh_radius" value="0.1"/>
    <xacro:property name="wh_thick" value="0.04"/>
    <xacro:property name="wh_chasis_gap" value="0.001"/>
    <xacro:property name="wh_mass" value="1.0"/>



    <!-- Avare Teker Nitelikleri -->

    <xacro:property name="cwh_chasis_offset_xy" value="0.1"/>
    <!-- yarı çapı diğer niteliklere göre ayarlayalım -->
    <xacro:property name="cwh_radius" value="${(wh_radius - (chasis_len_z / 2.0 - base_chasis_offset)) / 2.0}"/>
    <xacro:property name="cwh_mass" value="0.00001"/>



    <!-- Tahrik Tekerleği Makrosu -->
    <xacro:macro name="create_wh" params="postfix yfact">

        <joint name="base_TO_wh_${postfix}" type="continuous">
            <origin xyz="0.0 ${yfact * (chasis_len_y / 2.0 + wh_thick / 2.0 + wh_chasis_gap)} 0.0" rpy="0.0 0.0 0.0"/>
            <parent link="base_link"/>
            <child link="wh_${postfix}"/>
            <axis xyz="0.0 1.0 0.0"/>
        </joint>

        <link name="wh_${postfix}">
            <inertial>
                <origin xyz="0.0 0.0 0.0" rpy="${pi / 2.0} 0.0 0.0"/>

                <mass value="${wh_mass}"/>
                <inertia 
                    ixx="${wh_mass * (3*wh_radius*wh_radius + wh_thick*wh_thick) / 12.0}"
                    iyy="${wh_mass * (3*wh_radius*wh_radius + wh_thick*wh_thick) / 12.0}"
                    izz="${wh_mass * (wh_radius*wh_radius) / 2.0}"
                    ixy="0" ixz="0" iyz="0"
                />
            </inertial>

            <visual>
                <origin xyz="0.0 0.0 0.0" rpy="${pi / 2.0} 0.0 0.0"/>
                <geometry>
                    <cylinder radius="${wh_radius}" length="${wh_thick}"/>
                </geometry>
                <material name="gray"/>
            </visual>

            <collision>
                <origin xyz="0.0 0.0 0.0" rpy="${pi / 2.0} 0.0 0.0"/>
                <geometry>
                    <cylinder 
                        radius="${wh_radius}" 
                        length="${wh_thick}"/>
                </geometry>
            </collision>
        </link>

    </xacro:macro>



    <!-- Tahrik Tekerlekleri Oluşturumu -->

    <xacro:create_wh postfix="l" yfact="1.0"/> <!-- sol -->
    <xacro:create_wh postfix="r" yfact="-1.0"/> <!-- sağ -->



    <!-- Avare Teker Makrosu -->

    <xacro:macro name="create_cwh" params="postfix xfact yfact">

        <!-- Yaw joint: x ekseni etrafında dönme -->
        <joint name="chasis_TO_cwh_${postfix}" type="fixed">
            <origin xyz="${xfact * (chasis_len_x / 2.0 - cwh_chasis_offset_xy)} 
                        ${yfact * (chasis_len_y / 2.0 - cwh_chasis_offset_xy)} 
                        ${-1 * (chasis_len_z / 2.0 + cwh_radius)}" rpy="0 0 0"/>
            <parent link="chasis"/>
            <child link="cwh_${postfix}"/>
        </joint>

        <!-- BALL CASTER LINK -->
        <link name="cwh_${postfix}">

            <!-- Çok hafif top (dönüşlerde robotu tutmaması için) -->
            <inertial>
                <mass value="0.01"/>
                <origin xyz="0 0 0"/>
                <inertia
                    ixx="1e-5" ixy="0" ixz="0"
                    iyy="1e-5" iyz="0"
                    izz="1e-5"/>
            </inertial>

            <!-- Görsel -->
            <visual>
                <origin xyz="0 0 0" rpy="0 0 0"/>
                <geometry>
                    <sphere radius="${cwh_radius}"/>
                </geometry>
                <material name="gray"/>
                  
            </visual>

            <!-- Çarpışma ve sürtünme ayarları -->
            <collision>
                <origin xyz="0 0 0" rpy="0 0 0"/>
                <geometry>
                    <sphere radius="${cwh_radius}"/>
                </geometry>
            </collision>
        </link>

        <!-- gazebo için sürtünme değerlerini azaltıyoruz -->
        <gazebo reference="cwh_${postfix}">
            <collision>
                <surface>
                    <friction>
                        <ode>
                            <mu>0.001</mu>    <!-- temel sürtünme -->
                            <mu2>0.001</mu2>  <!-- ikinci eksen sürtünmesi -->
                            <slip1>1.0</slip1>
                            <slip2>1.0</slip2>
                        </ode>
                    </friction>
                    <bounce>
                        <restitution_coefficient>0.0</restitution_coefficient>
                    </bounce>
                </surface>
            </collision>
        </gazebo>

    </xacro:macro>



    <!-- Avare Tekerlerin Kullanımı -->

    <xacro:create_cwh postfix="lf" xfact="1.0" yfact="1.0"/>
    <xacro:create_cwh postfix="lb" xfact="-1.0" yfact="1.0"/>
    <xacro:create_cwh postfix="rf" xfact="1.0" yfact="-1.0"/>
    <xacro:create_cwh postfix="rb" xfact="-1.0" yfact="-1.0"/>

</robot>
```

`main.urdf.xacro`:

```xml
<?xml version="1.0"?>

<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="btkamr">

    <!-- Renk Tanımlamaları -->
    <material name="red">
        <color rgba="1 0 0 1"/>
    </material>

    <material name="green">
        <color rgba="0 1 0 1"/>
    </material>

    <material name="blue">
        <color rgba="0 0 1 1"/>
    </material>

    <material name="gray">
        <color rgba="0.7 0.7 0.7 1"/>
    </material>



    <!-- Şase Nitelikleri -->

    <xacro:property name="chasis_len_x" value="0.6"/>
    <xacro:property name="chasis_len_y" value="0.4"/>
    <xacro:property name="chasis_len_z" value="0.2"/>
    <xacro:property name="base_chasis_offset" value="0.08"/>
    <xacro:property name="chasis_mass" value="2.0"/>



    <!-- Dosyaları Dahil Etme -->
    
    <xacro:include filename="./wheels.urdf.xacro" />
    <xacro:include filename="./g_plugins.xacro" />



    <!-- Base Link -->

    <link name="base_footprint"/>
    
    <link name="base_link"/>

    <joint name="base_TO_footprint" type="fixed">
        <origin xyz="0.0 0.0 ${wh_radius}" rpy="0.0 0.0 0.0"/>
        <parent link="base_footprint"/>
        <child link="base_link"/>
    </joint>



    <!-- Şase Oluşturumu -->

    <joint name="base_TO_chasis" type="fixed">
        <origin xyz="0.0 0.0 ${base_chasis_offset}" rpy="0.0 0.0 0.0"/>
        <parent link="base_link"/>
        <child link="chasis"/>
    </joint>

    <link name="chasis">
        <inertial>
            <mass value="${chasis_mass}"/>
            <inertia 
                ixx="${chasis_mass * (chasis_len_y * chasis_len_y + chasis_len_z * chasis_len_z) / 12.0}"
                iyy="${chasis_mass * (chasis_len_x * chasis_len_x + chasis_len_z * chasis_len_z) / 12.0}"
                izz="${chasis_mass * (chasis_len_x * chasis_len_x + chasis_len_y * chasis_len_y) / 12.0}"
                ixy="0" ixz="0" iyz="0"
            />
        </inertial>

        <visual>
            <geometry><box size="${chasis_len_x} ${chasis_len_y} ${chasis_len_z}"/></geometry>
        </visual>

        <collision>
            <geometry><box size="${chasis_len_x} ${chasis_len_y} ${chasis_len_z}"/></geometry>
        </collision>
    </link>

</robot>
```
<br/>
<br/>
<br/>

Şimdi robot modelimizi oluşturduğumuza göre artık RViz'de görüntüleyelim. Bunun için bir launch dosyası yazalım.

`launch` klasörünün altına `display.launch.py` isminde bir python betiği oluşturalım.

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

PKG_NAME: str = "btkamr_description"

def generate_launch_description():
    pkg_share = get_package_share_directory(PKG_NAME)
    urdf_path = os.path.join(pkg_share, "urdf", "main.urdf.xacro")
    robot_desc = ParameterValue(Command(["xacro ", urdf_path]), value_type=str) # boşluk önemli xacro' '

    return LaunchDescription([
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description": robot_desc}]
        ),
        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui"
        ),
        Node(
            package="rviz2",
            executable="rviz2"
        ),
    ])
```

Artık build edelim

```bash
# workspace dizininde olduğumuzdan emin olalım
colcon build
```

Çalıştıralım

```bash
# workspace dizininde olduğumuzdan emin olalım
source install/setup.bash
ros2 launch btkamr_description display.launch.py
```

Bir hata görünüyorsa düzeltelim ve adımları tekrarlayalım.

Uygulama 1 tamamlanmıştır.

</details>

<h1 id="hid-2">2. Gazebo Launcher'ı Oluşturumu </h1>

Gazebo'yu başlatacak ve robotu spawn edecek bir launcher ayarlayın. Robot'un RViz'de doğru göründüğünden emin olun.

* gazebo.launch.py dosyası oluştur
* gazeboyu başlat
* robotu gazeboda spawn et
* plugin ekle joint state pbulisher
* köprü yaml dosyası yaz
* köprüyü çalıştır

<details> 
    <summary>
        İpucu için tıklayın.
    </summary>

    Jointler görünmüyor çünkü jointi publishleyen yok :(

</details>

<!-- <details> 
    <summary>
        Çözümü görmek için tıklayın.
    </summary> -->

Önceki launch dosyamızı kopyalayıp yapıştıralım. İsmini ise `gazebo.launch.py` olarak değiştirelim.

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

PKG_NAME: str = "btkamr_description"

def generate_launch_description():
    pkg_share = get_package_share_directory(PKG_NAME)
    urdf_path = os.path.join(pkg_share, "urdf", "main.urdf.xacro")
    robot_desc = ParameterValue(Command(["xacro ", urdf_path]), value_type=str) # boşluk önemli xacro' '

    return LaunchDescription([
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description": robot_desc}]
        ),
        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui"
        ),
        Node(
            package="rviz2",
            executable="rviz2"
        ),
    ])
```

`joint_state_publisher_gui` düğümünü başlatan kodu silelim. Çünkü artık joint durumlarını biz belirlemeyeceğiz simülasyonda ne ise onu kabul edeceğiz.

Launch dosyamızdan şu kod bloğunu çıkarıyoruz:

```python
Node(
    package="joint_state_publisher_gui",
    executable="joint_state_publisher_gui"
),
```

<br/>

Şimdi bizden istenenleri yapmaya başlayabiliriz.

Gazeboyu başlatmamız lazım. Bunun için `ros_gz_sim` paketinin `gz_sim.launch.py` ismindeki launcher'ını kullanabiliriz.

Launch dosyamızın import bölümüne şunu ekleyelim.

```python
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
```
<br/>

Launch dosyamızın diğer düğümleri başlattığımız yere şunu ekleyelim.

```python
IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
        os.path.join(
            get_package_share_directory('ros_gz_sim'),
            'launch',
            'gz_sim.launch.py'
        )
    ),
    launch_arguments={
        'gz_args': ['-r -v 4 ', "empty.sdf"] #cli'dan çalışırken de verebileceğimiz argümanlar
    }.items()
),
```

<br/>

Şimdi bir test edelim. Bir sıkıntı yoksa devam edelim.

Robotumuzu simülasyonda spawn etmemiz gerekiyor. Bunun için `ros_gz_sim` paketinin `create` executable'ını kullanabiliriz.

Launch dosyamıza şunu ekleyelim.

```python
Node(
    package='ros_gz_sim',
    executable='create',
    parameters=[{'topic': 'robot_description'}],
),
```
<br/>

Şimdi bir test edelim. Bir sıkıntı yoksa devam edelim.

Joint state publisher plugin'i eklememiz gerekiyor. 

`urdf` klasörümüze, `g_plugins.urdf.xacro` isminde bir dosya açalım. Bundan sonra pluginlerimizi bu dosyada ekleyeceğiz.

Bu dosyanın içeriğini oluşturalım:

```xml
<?xml version="1.0"?>

<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="btkamr">

    <gazebo>
        <plugin 
            filename="gz-sim-joint-state-publisher-system"
            name="gz::sim::systems::JointStatePublisher"
        >
            <!-- Tüm jointlerin yayımlanmasını istediğimizden joint_name belirtmedik -->
            
            <!-- Yayınlanacak topic ismi -->
            <topic>btkamr/joint_states</topic>
        </plugin>  
    </gazebo>

</robot>
```

<br/>

Bu dosyayı `main.urdf.xacro` dosyamızda `include` edelim.

```xml
<xacro:include filename="./g_plugins.urdf.xacro" />
```

<br/>

Şimdi bir daha test edelim. Launcher'ımızı çalıştırdıktan sonra terminalimizden Gazebo topic'lerini kontrol edelim

```bash
gz topic -l
```

Eğer `/btkamr/joint_states` isminde bir çıktı göremiyorsak bir şeyleri yanlış yapmışız demektir. Yoksa devam edelim.

Artık Gazebo joint durumlarını `/btkamr/joint_states` topic'inden yayımlıyor. Ancak bizim buna ROS2 tarafında ihtiyacımız var. O yüzden bir köprü oluşturmamız lazım.

Bunun için `ros_gz_bridge` paketinin `parameter_bridge` executable'ını kullanabiliriz. Bunun için de önce bir konfigürasyon dosyası oluşturalım.

`config` isminde bir klasör açalım. Bu klasörü de `CMakeList.txt` dosyasında share klasörüne taşınması için ayarlama yapalım.

`config` klasörünün içine `gz_bridge.yaml` isminde bir dosya açalım ve içine şunu yazalım.

```yaml
# - ros_topic_name: "<ROS tarafındaki topic ismi>"
#   gz_topic_name: "<Gazebo tarafındaki topic ismi>"
#   ros_type_name: "<verinin ROS tarafındaki tipi>"
#   gz_type_name: "<verinin Gazebo tarafındaki tipi>"
#   direction: <köprünün yönü>

- ros_topic_name: "joint_states"
  gz_topic_name: "btkamr/joint_states"
  ros_type_name: "sensor_msgs/msg/JointState"
  gz_type_name: "gz.msgs.Model"
  direction: GZ_TO_ROS 
```

<br/>

Launcher'da bu dosyayı referans vererek köprüyü başlatalım.

Dosyanın yolunu bulup bir değişkene atalım.

```python
gz_bridge_cfg_file = os.path.join(
    get_package_share_directory(),
    "config",
    "gz_bridge.yaml"
)
```

<br/>

Şu düğümü de başlatalım

```python
Node(
    package='ros_gz_bridge',
    executable='parameter_bridge',
    parameters=[{'config_file': gz_bridge_cfg_file}],
),
```

<br/>

Şimdi test edelim. RViz'de robot modeli görünümünde herhangi bir sıkıntı yoksa köprümüz doğru çalışıyordur.


Dosyaların son halleri:

`gazebo.launch.py`


<!-- </details> -->

<h1 id="hid-3">3. Diferansiyel Sürüş Plugininin Eklenmesi</h1>

Robotunuzun URDF dosyasına diferansiyel sürüş plugini ekleyin ve Gazebo'da test edin

<details> 
    <summary>
        Çözümü görmek için tıklayın.
    </summary>

    ayıp :(

</details>

<h1 id="hid-4">4. Klavye Kontrol (teleop)</h1>

Robotunuzu, ROS2 ile yazılmış bir klavye kontrol düğümü ile hızını kontrol edin.

<details> 
    <summary>
        Çözümü görmek için tıklayın.
    </summary>

    ayıp :(

</details>

<h1 id="hid-5">5. Lidar Sensörünün Eklenmesi</h1>

Robotunuza bir LiDAR sensörü ekleyin ve RViz'de görüntüleyin

<details> 
    <summary>
        Çözümü görmek için tıklayın.
    </summary>

    ayıp :(

</details>



<h1 id="hid-6">6. Odometri Plugini ve ROS2 Entegrasyonu</h1>

Robotunuzun URDF'ine bir odometry publisher plugini ekleyin ve RViz'de gözlemleyin.

<details> 
    <summary>
        Çözümü görmek için tıklayın.
    </summary>

    ayıp :(

</details>

<h1 id="hid-6">7. Dünya Ve Model Ekleme</h1>


Kendimize ait bir model ve dünya oluşturalım.

* `worlds` ve `models` isminde klasör oluşturun.

* `CMakeLists.txt` dosyasını düzenleyin, bu klasörlerin de `share` klasörüne taşınmasını sağlayın.

* `models` klasörünün içine `my_model` isminde bir model oluşturun.

* `worlds` klasörünün içinde `my_world.sdf` isminde bir dünya oluşturun. 

* Oluşturduğunuz dünyada, oluşturduğunuz modeli kullanın.

* Launch dosyanızı düzenleyin.

* Çalıştırıp deneyimleyin.

<details> 
    <summary>
        Çözümü görmek için tıklayın.
    </summary>

    ayıp :(

</details>
