# DynamiKontrol

## Plug and Spin It

**If you want to buy this module, please email us matrix.ai.solution@gmail.com**

DynamiKontol(DK) is Python API for controlling motors and hardware modules. You can integrate into your Python code such as TensorFlow, PyTorch or OpenCV with hardwares easily.

Also you can control multiple DK modules on your PC, Raspberry Pi or NVIDIA Jetson.

- Easy USB Interface
- Easy Python API
- Block-Based Programming
- Support All Devices and OS

| Model | Image | Control Method |
| --- | --- | --- |
| DK Angle | <img src="docs/source/_static/07.jpg" width="270px"> | Controlling rotation angle (Degree) |
| DK Speed | <img src="docs/source/_static/DK_Speed_210511.png" width="270px"> | Controlling rotation speed (RPM) |

## Getting Started

```
pip install -U DynamiKontrol
```

```python
from dynamikontrol import Module

module = Module()

module.motor.angle(angle=0)
time.sleep(2)

while True:
    # move 45 degree in clockwise
    module.motor.angle(angle=45)
    module.led.on(color='r')
    time.sleep(2)

    # move 45 degree in counter clockwise during 5 seconds
    module.motor.angle(angle=-45, period=5)
    module.led.on(color='g')
    time.sleep(5)
```

## Examples

| Example | Demo | Source Code |
| --- | --- | --- |
| Face Tracking Camera | [YouTube](https://youtu.be/xrxD-G6Nlk0) | [Link](https://dynamikontrol.readthedocs.io/en/latest/face_tracking_camera.html) |
| A.I. Parking Barrier Gate | <img src="docs/source/_static/ai_parking_barrier_gate.gif" width="270px"> | [Link](https://github.com/kairess/ANPR-with-Yolov4) |
| Finger Volume Controller | <img src="docs/source/_static/finger_volume_controller.gif" width="270px"> | [Link](https://github.com/TheMatrixGroup/DynamiKontrol/blob/master/examples/finger_volume_controller.py) |
| Robot Arm | <img src="docs/source/_static/robot_arm.gif" width="270px"> | [Link](https://cafe.naver.com/dynamikontrol/57) |
| Dial GUI | ![](docs/source/_static/dial_gui.gif) | [Link](https://dynamikontrol.readthedocs.io/en/latest/dial_gui.html) |
| IoT Door Lock | <img src="docs/source/_static/iot_door_lock.gif" width="270px"> | [Link](https://dynamikontrol.readthedocs.io/en/latest/iot_door_lock.html) |

## Documentation

| Language | URL |
| --- | --- |
| English | https://dynamikontrol.readthedocs.io/en/latest/ |
| Korean | https://dynamikontrol.readthedocs.io/ko/latest/ |

## Supported Devices

- PC/Laptop
- Raspberry Pi
- NVIDIA Jetson
- and all devices which support serial communication

### Operating System

- Windows
- MacOS
- Linux
- Ubuntu

## DynamiKontrol Toolbox

You can test the module before writing the code.

[Download](https://github.com/TheMatrixGroup/DynamiKontrol/releases/tag/0.3.4)

<img src="docs/source/_static/dk_toolbox.png" width="540px">

## Block-Based Coding

Google's Blockly library makes it easier. Have fun with DynamiKontrol using interlocking blocks. (Support MacOS and Linux only. Windows comming soon)

<img src="docs/source/_static/coding_block.png" width="270px">

https://thematrixgroup.github.io/?lang=en

---

- DynamiKontrol website https://dk.m47rix.com
- 구매 링크 https://smartstore.naver.com/dynamikontrol
- 네이버 카페 (질문과답변, 예제) https://cafe.naver.com/dynamikontrol

Developed and designed by [The Matrix](https://www.m47rix.com) (c) 2021

matrix.ai.solution@gmail.com
