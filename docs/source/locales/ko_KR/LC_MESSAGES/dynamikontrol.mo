��    *      l              �  !   �  /   �  ,     2   <     o  8   �  R   �  #     C   2     v     �     �     �     �     �     �  (     *   8  �   c     �  #        %  
   D     O  O   ^  9   �  \   �     E     a     p  $   �     �  Y   �  4        Q  3   h     �     �     �     �     �  ~  	  $   �
  3   �
  /   �
  ,        J  (   Y  S   �     �  3   �     )  !   A  #   c     �     �     �  '   �  2   �  5      �   V     )  9   F     �     �     �  q   �  K   +  s   w  !   �       %     2   D     w  a   �  V   �     K  W   Z     �     �     �      �  $      Blink the LED light periodically. Call the callback function after specific time. Call the callback function at specific time. Callback delay time in seconds. Defaults to ``0``. Callback function. Callback interval time in seconds. Defaults to ``None``. Callback time in datetime str. e.g) ``2021-03-04 21:57:30``. Defaults to ``None``. Close the connection of the module. Color of the LED light. ``r``, ``y`` or ``g``. Defaults to ``all``. Connect to the module. Control the angle of motor. Data from the module. Data to send. Device time. General timer class. Get ID of the connected module. Get device time of the connected module. Get serial number of the connected module. If ``angle > 0`` moves along clockwise, otherwise moves along counter clockwise. ``angle`` must be between ``-85`` to ``85`` in degrees. LED submodule class. Length of bytes. Defaults to ``1``. Length of the data to receive. Module ID. Module object. Pause receiving thread, send/receive data manually and resume receiving thread. Read the data from the module using serial communication. Receive data from the module. It runs on single thread for waiting response from the module. Send the data to the module Serial number. Servo motor submodule class. Specify serial number of the module. Stop the timer. Toggle the LED light. Turn off while the light on status and turn on while the light off. Turn off delay in milliseconds. Defaults to ``256``. Turn off the LED light Turn on delay in milliseconds. Defaults to ``256``. Turn on the LED light. args. Defaults to ``()``. dynamikontrol package kwargs. Defaults to ``{}``. print debug messages. Project-Id-Version: DynamiKontrol 
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2021-03-07 19:47+0900
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language: ko_KR
Language-Team: ko_KR <LL@li.org>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.9.0
 LED를 주기적으로 깜빡인다. 일정 시간 후에 콜백 함수를 호출한다. 특정 시간에 콜백 함수를 호출한다. 콜백 대기 시간 (초). 기본값 ``0``. 콜백 함수. 콜백 주기 (초). 기본값 ``None``. 콜백 시간 datetime 문자열. 예) ``2021-03-04 21:57:30``. 기본값 ``None``. 모듈과 연결을 끊는다. LED 색상. ``r``, ``y``, ``g``. 기본값 ``all``. 모듈에 연결한다. 모터의 각도를 조절한다. 모듈로부터 수신한 데이터 전송할 데이터 기기 시간 기본 타이머 클래스. 연결된 모듈의 ID를 가져온다. 연결된 모듈의 기기 시간을 가져온다. 연결된 모듈의 시리얼 번호를 가져온다. 만약 ``angle > 0`` 이면 시계방향으로 움직이고, ``angle < 0`` 이면 시계반대방향으로 움직인다. ``angle`` 값은 반드시 ``-85`` 에서 ``85`` 사이의 값을 갖는다 (단위: 도) LED 서브 모듈 클래스. 수신한 데이터의 길이(바이트). 기본값 ``1`` 수신할 데이터의 길이 모듈의 ID Module 객체 수신 쓰레드를 잠시 멈추고, 송/수신을 수동으로 진행한 후 다시 수신 쓰레드를 켠다. 시리얼 통신을 사용하여 모듈로부터 데이터를 수신한다. 모듈로부터 데이터를 받는다. 단일 쓰레드를 사용하여 모듈로부터의 응답을 기다린다. 모듈에 데이터를 보낸다. 시리얼 번호 서보 모터 서브 모듈 클래스 특정 시리얼 번호의 모듈을 제어한다. 타이머를 중지한다. LED 켜짐/꺼짐 상태를 토글한다. 만약 꺼져있다면 켜고, 켜져 있다면 끈다. LED가 꺼진 상태로 유지되는 시간, 단위 밀리세컨드. 기본값 ``256`` LED를 끈다. LED가 켜진 상태로 유지되는 시간, 단위 밀리세컨드. 기본값 ``256``. LED를 켠다. args 인자. 기본값 ``()``. dynamikontrol 패키지 kwargs 인자. 기본값 ``{}``. 디버그 메시지를 출력한다. 