<?xml version="1.0" encoding="UTF-8"?>
<tileset name="objects" tilewidth="32" tileheight="32" tilecount="128" columns="8">
 <image source="images/objects.png" width="256" height="512"/>
 <tile id="0">
  <properties>
   <property name="OnCollision">AddCoins(1)
RemoveCollidedObject()</property>
   <property name="name" value="coin"/>
  </properties>
 </tile>
 <tile id="8">
  <properties>
   <property name="Name" value="door-up"/>
  </properties>
 </tile>
 <tile id="9">
  <properties>
   <property name="Name" value="door-down"/>
  </properties>
 </tile>
 <tile id="10">
  <properties>
   <property name="Name" value="door-left"/>
  </properties>
 </tile>
 <tile id="11">
  <properties>
   <property name="Name" value="door-right"/>
  </properties>
 </tile>
</tileset>
