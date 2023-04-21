# Apex_AimTrain
Make a visualize UI to read your input(mouse or another command) to start the recoil visualize to many rings like music game. 

# How to setup requirement
1. Download python 3.9 (https://www.python.org/downloads/release/python-3913), you can only download windows installer which is the easist method to download python.
2. Using Powershell or CMD to start command line operation and check python download yet.
    * `python --version`
3. You can directly open powershell in Apex_AimTrain directory or run powershell and use cd to Apex_AimTrain (key in following command)
    * `cd [yourFilePosition]/Apex_AimTrain`
4. After previous step, use pip to install the modules which program needed
    * `pip install -r requirement.txt`
5. Run main program
    * `python ./aim_train_v2.py`
    
# How to start
0. Setting your Apex to Borderless windows. (If you are using Multiple screen device, you can ignore it.)
1. Default recoil pattern is Flatline(VK-47).
2. Keys to switch your recoil pattern or another operations :
    * F1 Flatline(VK-47)
    * F2 R301
    * F3 Nemesis
    * F4 R99
    * F5 Car
    * F6 Volt
    * F7 RE45
    * F11 Hide GUIs(you can press F1 or another keys to show UI again)
    * F12 Shotdown this program
    > **Note**
    > Following guns have not add yet : **Spitfire、Rampage、Lstar、Havoc、Devotion、Alternator**
    
    > **Note**
    > If your nemesis charged, recoil pattern WPM still maintain heighest , then you need press F3 to reset RPM after your guns energy is zero.
    
    > **Warning**
    > If switch guns not success, you should shotdown this program and restart
    
# Other programs
* **aim_train.py** : Version 1 of AimTrain, only give you now direction that hardly reacting that.
* **bullet_locate.py** : Helping developer to locating the bullets's position, you can modify the pictures in guns folder and do following commands
   * Run program and use Redirect command : `python bullet_locate.py > ./location/(name).txt`
   * I am using Geogebra to list all position and following order to sort positions

# Assets
Images, audio fragments, weapon names and behavior come from Apex Legends game or from websites created and owned by Electronic Arts Inc. or Respawn Entertainment, who hold the copyright of Apex Legends.

Some reference(like RPM) come from Apex Legends Wiki.

Recoil path reference from https://github.com/metaflow/apex-recoil?fbclid=IwAR38fJOLpx0Nqij6AZDjc7xtebDdx4_deLto0EAp3jR6Kr-3tlN_cTmztnw
