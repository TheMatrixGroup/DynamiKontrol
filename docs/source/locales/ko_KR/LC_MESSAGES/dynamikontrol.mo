Þ    .                    ü  !   ý  /     ,   O  2   |  D   ¯     ô  8     R   @       C   !     e  c   |     à     ü  w   
  u        ø               3  (   S  -   |     ª  *   Ã     î     w  
             ¦  (   Å     î     
	     	     6	  $   ¹	     Þ	  Y   î	     H
     _
  /   v
     ¦
     À
  1   Ö
          $  ~  :  $   ¹  3   Þ  /     ,   B  G   o     ·  (   Æ  S   ï     C  3   Ô       ¦      !   Ç     é  ¥   ý  ¥   £     I     e     s  '     2   ·  <   ê  +   '  5   S  Ñ        [     x             *   µ  !   à       %     å   9  2        R  a   m     Ï     Þ  /   í          <  1   T        $   §   Blink the LED light periodically. Call the callback function after specific time. Call the callback function at specific time. Callback delay time in seconds. Defaults to ``0``. Callback function when motor has been stopped. Defaults to ``None``. Callback function. Callback interval time in seconds. Defaults to ``None``. Callback time in datetime str. e.g) ``2021-03-04 21:57:30``. Defaults to ``None``. Close the connection of the module. Must include ``module.disconnect()`` at the end of the code so that module can close connection properly. Color of the LED light. ``r``, ``y`` or ``g``. Defaults to ``all``. Connect to the module. Control period. ``period`` must be between ``0`` to ``65535`` in millisecond. Defaults to ``None``. Control the angle of motor. Data to send. Delay time for turned-off status. ``off_delay`` must be between ``0`` to ``65535`` in millisecond. Defaults to ``256``. Delay time for turned-on status. ``on_delay`` must be between ``0`` to ``65535`` in millisecond. Defaults to ``256``. Device firmware version. Device time. General timer class. Get ID of the connected module. Get device time of the connected module. Get firmware version of the connected module. Get offset of the motor. Get serial number of the connected module. If ``angle > 0`` moves along clockwise, otherwise moves along counter clockwise. ``angle`` must be between ``-85`` to ``85`` in degrees. LED submodule class. Module ID. Module object. Offset of the motor in degree. Offset of the motor in degree. e.g) 17.5 Send the data to the module Serial number. Servo motor submodule class. Set offset of the motor. If the motor angle is inclined slightly even angle set to 0, you can adjust offset of the motor manually. Specify serial number of the module. Stop the timer. Toggle the LED light. Turn off while the light on status and turn on while the light off. Turn off the LED light Turn on the LED light. args for callback function. Defaults to ``()``. args. Defaults to ``()``. dynamikontrol package kwargs for callback function. Defaults to ``{}``. kwargs. Defaults to ``{}``. print debug messages. Project-Id-Version: DynamiKontrol 
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2021-04-15 16:51+0900
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language: ko_KR
Language-Team: ko_KR <LL@li.org>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.9.0
 LEDë¥¼ ì£¼ê¸°ì ì¼ë¡ ê¹ë¹¡ì¸ë¤. ì¼ì  ìê° íì ì½ë°± í¨ìë¥¼ í¸ì¶íë¤. í¹ì  ìê°ì ì½ë°± í¨ìë¥¼ í¸ì¶íë¤. ì½ë°± ëê¸° ìê° (ì´). ê¸°ë³¸ê° ``0``. ëª¨í°ê° ë©ì¶ìì ë ì¤íí  ì½ë°± í¨ì. ê¸°ë³¸ê° ``None``. ì½ë°± í¨ì. ì½ë°± ì£¼ê¸° (ì´). ê¸°ë³¸ê° ``None``. ì½ë°± ìê° datetime ë¬¸ìì´. ì) ``2021-03-04 21:57:30``. ê¸°ë³¸ê° ``None``. ëª¨ëê³¼ ì°ê²°ì ëëë¤. ì½ëì ë§ì§ë§ì ë°ëì ``module.disconnect()`` ë¥¼ í¸ì¶í´ì¼ ì ìì ì¼ë¡ ì°ê²°ì´ ì¢ë£ëë¤. LED ìì. ``r``, ``y``, ``g``. ê¸°ë³¸ê° ``all``. ëª¨ëì ì°ê²°íë¤. ëª¨í°ê° ìì§ì´ë ìê°ì ì ìíë¤, ë¨ì ë°ë¦¬ì¸ì»¨ë. ``period`` ë ë°ëì ``0`` ìì ``65536`` ì¬ì´ì ê°ì ê°ëë¤. ê¸°ë³¸ê° ``None``. ëª¨í°ì ê°ëë¥¼ ì¡°ì íë¤. ì ì¡í  ë°ì´í° LEDê° êº¼ì§ ìíë¡ ì ì§ëë ìê°, ë¨ì ë°ë¦¬ì¸ì»¨ë. ``on_delay`` ë ë°ëì ``0`` ìì ``65536`` ì¬ì´ì ê°ì ê°ëë¤. ê¸°ë³¸ê° ``256``. LEDê° ì¼ì§ ìíë¡ ì ì§ëë ìê°, ë¨ì ë°ë¦¬ì¸ì»¨ë. ``on_delay`` ë ë°ëì ``0`` ìì ``65536`` ì¬ì´ì ê°ì ê°ëë¤. ê¸°ë³¸ê° ``256``. ëª¨ëì íì¨ì´ ë²ì . ê¸°ê¸° ìê° ê¸°ë³¸ íì´ë¨¸ í´ëì¤. ì°ê²°ë ëª¨ëì IDë¥¼ ê°ì ¸ì¨ë¤. ì°ê²°ë ëª¨ëì ê¸°ê¸° ìê°ì ê°ì ¸ì¨ë¤. ì°ê²°ë ëª¨ëì ê¸°ê¸° íì¨ì´ ë²ì ì ê°ì ¸ì¨ë¤. ëª¨í°ì ì¤íì ê°ëë¥¼ ê°ì ¸ì¨ë¤. ì°ê²°ë ëª¨ëì ìë¦¬ì¼ ë²í¸ë¥¼ ê°ì ¸ì¨ë¤. ë§ì½ ``angle > 0`` ì´ë©´ ìê³ë°©í¥ì¼ë¡ ìì§ì´ê³ , ``angle < 0`` ì´ë©´ ìê³ë°ëë°©í¥ì¼ë¡ ìì§ì¸ë¤, ë¨ì ë. ``angle`` ê°ì ë°ëì ``-85`` ìì ``85`` ì¬ì´ì ê°ì ê°ëë¤. LED ìë¸ ëª¨ë í´ëì¤. ëª¨ëì ID. Module ê°ì²´ ëª¨í°ì ì¤íì, ë¨ì ë. ëª¨í°ì ì¤íì, ë¨ì ë. ì) 17.5 ëª¨ëì ë°ì´í°ë¥¼ ë³´ë¸ë¤. ìë¦¬ì¼ ë²í¸ ìë³´ ëª¨í° ìë¸ ëª¨ë í´ëì¤ ëª¨í°ì ì¤íì ê°ëë¥¼ ì¡°ì íë¤. ë§ì½ ëª¨í°ì ê°ëë¥¼ 0ì¼ë¡ ì¤ì íëë°ë ë¶êµ¬íê³  ëª¨í°ì ê°ëê° ì´ë í ìª½ì¼ë¡ ê¸°ì¸ì´ì ¸ ìì¼ë©´ ìëì¼ë¡ ì¤íì ê°ëë¥¼ ì¡°ì í  ì ìë¤. í¹ì  ìë¦¬ì¼ ë²í¸ì ëª¨ëì ì ì´íë¤. íì´ë¨¸ë¥¼ ì¤ì§íë¤. LED ì¼ì§/êº¼ì§ ìíë¥¼ í ê¸íë¤. ë§ì½ êº¼ì ¸ìë¤ë©´ ì¼ê³ , ì¼ì ¸ ìë¤ë©´ ëë¤. LEDë¥¼ ëë¤. LEDë¥¼ ì¼ ë¤. ì½ë°± í¨ìì args ì¸ì. ê¸°ë³¸ê° ``()``. args ì¸ì. ê¸°ë³¸ê° ``()``. dynamikontrol í¨í¤ì§ ì½ë°± í¨ìì kwargs ì¸ì. ê¸°ë³¸ê° ``{}``. kwargs ì¸ì. ê¸°ë³¸ê° ``{}``. ëë²ê·¸ ë©ìì§ë¥¼ ì¶ë ¥íë¤. 