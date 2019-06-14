# SENSORES-DHT
Desarrollo python para sensores DHT 11/22

By Arturo Ledezma


19/01/2018 ACTUALIZACION

Ha pasado bastante tiempo desde que este proyecto se publicó por primera vez y muchas cosas han cambiado durante este tiempo.  algunos de los paquetes han cambiado en el camino y eso ha estado causando algunos problemas para terminar este instructivo. Decidí dar una actualización para todo el instructivo con el fin de poner todo en orden nuevamente.

El cambio más grande es que el sistema operativo ahora está cambiando de Wheezy anterior a Raspbian Stretch Lite. Todo lo demás, sigue mas o menos igual.


14/06/2019 ACTUALIZACION

Sensores DataCenter. El código utilizado para recopilar datos del sensor en la base de datos y para el envío de correo, ha pasado por una seria modificacion. Esto se hizo para agregar algunas características y para corregir algunos errores menores.

Si ha terminado este instructivo antes de esta actualización, pero desea actualizar el código. descargue de nuevo el código del registrador DHT22, configure config.json revisado y estará listo.

Algunos ejemplos sobre lo que cambió:

Se agrega creacion de Loggs. La ejecución del código ahora crea loggs en Datacenter/Debugger/Logs/. Práctico en caso de que algo salga mal.

Añadido soporte para sensores 1-n. La primera versión solo admitía 1-2 sensores, ahora puede haber tantos como Raspberry pi tenga gpios. Conecte el sensor a RPI y agregue la configuración del sensor a config.json y se tendrá en cuenta cuando se ejecute.

Configuraciones renombradas y reorganizadas para una comprensión más sencilla, por ejemplo, la verificación de la conexión ahora es promedios semanales, ya que en realidad envía temperaturas promedio semanales (la intención es que rpi informa semanalmente que aún está vivo)

Se agregó tiempo de espera configurable para el envío de correo, de modo que el usuario pueda decidir cuánto espera el registrador antes de enviar las advertencias después del correo enviado previamente. Anteriormente, se usó un valor codificado y resultó poco factible

El Backup de seguridad del SQL ya no es diario, el usuario establece el día en que se realiza el . 0 es diario, 1-7 es de lunes a domingo.

Las temperaturas medias semanales de envío ahora también son configurables. Funciona con el mismo patrón que el volcado de SQL anterior. 0 es diario, 1-7 es de lunes a domingo. Tenga en cuenta que siempre contará 7 días atrás y enviará el promedio de esos.

Posibilidad de elegir entre Fahrenheits o Celsius

Y algunos retoques más menores y arreglos.


---------------------------------------------------------------------------------------

Este es un almacenador de temperatura y humedad basado en Raspberry Pi que usa sensores Adafruit DHT11/22 para las mediciones. Es posible que hayas visto instrucciones similares antes, pero esta tiene un giro. No solo lee la temperatura y la humedad de los sensores, sino que almacena datos en la base de datos y proporciona medios para leer esos datos de temperatura con cualquier dispositivo web (computadora, teléfono, tableta) con navegador web. Este registrador también le permite establecer límites para las temperaturas y puede enviar correos electrónicos si la temperatura o la humedad del sensor exceden los límites establecidos ... esta característica ingeniosa se puede usar, por ejemplo, para avisar cuando es el momento de encender el clima en su casa /invernadero/lo que sea.

Para el desarrollo, necesitarás lo siguiente

- Raspberry PI (Utilicé Raspberry PI 2 modelo B +, pero también se puede con cualquier modelo)

- Fuente de poder. (Ulilice un adaptador de 5v 2a para mejor funcionamiento)

- Una memoria SD. Quiza podras utilizar un adaptador. (En este caso utilizamos una memoria de 8GB)

- Sensores DHT11/22 Resistencias de  4.7 kOhm . El desarrollo puede utilizar N cantidad de sensores. https://troxino.com/collections/sensores/products/sensor-de-humedad-y-temperatura-dht-22

Paso 1 conectaremos los sensores a la rasperry
    En este caso el pin 1 del sensor se conecta al pin de 3.3v de la raspberry
    El pin 2 al GPI de la raspberry(en mi caso el sensor 1 en el gpio 22 y el 2 en el gpio 23)






Cuando la conexion este lista, prepare la tarjeta SD y vaya al siguiente paso.
Step 2: Sistema Operativo de la raspnerry


En este caso utilizaremos Raspbian strech litte, ya que no utilizaremos el escritorio ni orogramas extras https://www.raspberrypi.org/downloads/raspbian/

Tambien utilizaremos Win32 Disk Imager http://sourceforge.net/projects/win32diskimager/

Iniciamos Win32 Disk Imager y le damos la ubicacion de la imagen descargada previamente(.img), seleccionamos el drive donde se instalara y presionamos "whrite"

Disk Imager le pide que confirme sobreescribir. Verifique que la unidad sea correcta y seleccione "Sí". Espera a que la escritura termine. Cuando Disk Imager le informa que la escritura se ha completado y que ha tenido éxito, presione "OK", cierre el Disk Imager y extraiga la tarjeta SD de la computadora.

Inserte la tarjeta SD en la raspberry y continuamos.
Step 3: Configurar la raspberry

Inserte la tarjeta SD en Raspberry Pi y enciéndala conectando la fuente de alimentación al micro-usb de Raspberry Pi. (Recuerde colocar el teclado y la pantalla antes de insertar la fuente de alimentación).

Rasperry Pi comienza a arrancar y le pedirá un nombre de usuario y contraseña.

Por default son estos:

username: pi

password: raspberry

Después de que el arranque haya terminado, inicie la herramienta de configuración escribiendo

sudo raspi-config

En la herramienta de configuración, haga lo siguiente:

1. Cambia tu contraseña y dale una nueva contraseña a Raspberry Pi

2. Abre network options -> 2.1 Change name if you want to -> 2.2 Enter wi-fi information (ssid, password)

3. MAsegúrese de que la Raspberry Pi se inicie en la consola seleccionando la opción 1, consola.

4.Esto es opcional, pero se recomienda que configure la información de configuración regional correctamente. Si desea cambiar las opciones de internacionalización, p. Ej. Disposición del teclado, zona horaria.

5. Desde las opciones de interfaz, seleccione P2 - SSH y habilítelo. Esto le permite conectarse a RPI con SSH desde su computadora. De esta manera no necesita pantalla ni teclado en RPI para usarlo


Finalmente, vaya a "Finalizar" y reinicie RPI escribiendo

sudo reboot

La configuración ya está lista. El siguiente paso es comprobar cómo se puede conectar de forma remota desde la PC.
Paso 4: Conectarse a la raspberry 


Raspberry Pi ahora está configurado y arrancado. Ahora deberías poder conectarlo a través de PuTTY desde tu PC. PuTTY se puede descargar desde http://www.chiark.greenend.org.uk/~sgtatham/putty

Cuando inicie el PuTTY, notará que se requiere el nombre de host o IP para poder conectarse a su Raspberry PI. Para obtener la dirección IP de la Raspberry pi. Escribe lo siguiente en Raspberry Pi y presiona enter

Ifconfig

Esto mostrará una lista de los adaptadores de red y la información de ellos (ver imagen). Si está conectado a Ethernet (como lo estaba en este punto), debería ver inet addr: xxx.xxx.xxx.xxx en eth0. al escribir esta dirección de entrada en la línea del nombre de host de PuTTY, debería poder conectar Raspberry Pi de forma remota.

Si configuró Wlan en el paso anterior, también debería ver la información de wlan0, inet addr: etc. También puede conectarse utilizando estos.

También hay forma manual de configurar WLAN. Se usó anteriormente con Wheezy OS y se describe en la página siguiente. Si ya tiene configurada la red, puede omitirla y continuar con la forma de conectarse con PuTTY.
Paso 5: Opcional: Configuración Wlan a Raspberry Pi
Imagen de Opcional: Configuración Wlan a Raspberry Pi

Manera manual de añadir configuraciones de WLAN de Raspberry Pi.

Debe configurar wlan ssid y la contraseña para que la Raspberry Pi pueda conectarse. Para comenzar, escriba lo siguiente y presione enter.

sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

Agregue la sección de red y las configuraciones al final del archivo (verifique la imagen de arriba para referencia):

Network={

ssid="yourssid"

psk="passwordtoyourwlan"

}

Guardar con Ctrl+X y seleccionamos "Y" para confirmar y guardar.

Ahora reiniciamos la Raspberry.

sudo reboot

Despues de que inicie tecleamos lo siguente para ver si se comecto a la red.

Ifconfig

Paso 5: Instalamos las librerias de los sensores

Empezemos por actualizar nuestro sistema.

sudo apt-get update

Con esto actualizaremos nuestro software.

sudo apt-get upgrade

Esto nos instalara las versiones nuevas. Presionamos "Y".

Cuando se terminen, es hora de instalar el código Python de Adafruit. Necesitará este código para obtener lecturas de los sensores DHT22. Esto también le permitirá probar que su ensamblaje funciona en primer lugar.

Al principio, consigue el compilador y la biblioteca de python. Para ese tipo sigue y pulsa enter.

sudo apt-get install build-essential python-dev python-openssl

Luego, asegúrese de que está en la carpeta donde desea instalar el código de Adafruit, sugeriría por defecto /home/. Para ese tipo sigue y pulsa enter.

cd /home/pi

En stretch lite, también es necesario instalar Git por separado, ya que no está incluido de forma predeterminada. Para ello, escriba:

sudo apt-get install git


Ahora clona el repositorio de git. Escribe lo siguiente y pulsa enter.

git clone https://github.com/adafruit/Adafruit_Python_DHT.git

Ir a la carpeta. Escribe a continuación y presiona enter.

cd Adafruit_Python_DHT

Y finalmente instalar la biblioteca de Adafruit. Escribe lo siguiente y pulsa enter.

sudo python setup.py install

Ahora es tiempo de probar nuestros sensores...
Paso 6: Probando los DHT22's


Ahora que la instalación ha finalizado, puede probar los sensores conectados y ver que obtiene lecturas de ellos. Vaya a la carpeta donde clonó el Adafruit_Python_DHT y luego a la carpeta de ejemplos. Escribe lo siguiente y pulsa enter.

cd /home/pi/Adafruit_Python_DHT/examples

¿Recuerdas las gpio/s donde conectaste los sensores? Ok, escriba sudo ./AdafruitDHT.py y presione enter. Tuve gpio 22 y 23 así que probé con

sudo ./AdafruitDHT.py 22 22

sudo ./AdafruitDHT.py 22 23



NOTA:

 
Si ve "Failed to get reading. Try again!",, Vuelva a intentarlo varias veces.

Si todavía no hay nada, vuelva a verificar que escribió el GPIO correcto.

Si es seguro que gpio está correcto, revise su ensamblaje nuevamente. P.ej. El DHT22 recibe energía, tierra y la resistencia está conectada correctamente.

Si todo lo anterior es correcto, intente conectar su sensor a otro GPIO y vea si obtiene lectura de eso

Si nada de lo anterior funciona, siempre es posible que su DHT22 esté roto.:(

Las bibliotecas para los sensores DHT22 ahora están instaladas y puede obtener las lecturas de los sensores. Es hora de configurar la base de datos para mantener esos datos.

Paso 6: Configuración de MySql para almacenar los datos de temperatura


Obtenga Mysql / MariaDb y los complementos necesarios para ello. Para hacer ese tipo sigue y pulsa enter.

sudo apt-get install mysql-server python-mysqldb

Nota: no se le solicitará la contraseña del usuario ROOT durante la instalación. Esto está vacío por defecto.

Después de la instalación completada. Es hora de configurar la base de datos real y las tablas para almacenar los datos. Esto debe hacerse en la consola mysql. Para ingresar a la consola escriba lo siguiente y presione enter.

sudo mysql -u root -p -h localhost

Presione enter (vacío) para la contraseña y debería estar en la consola de MariaDb

En consola

Primero, crea una base de datos llamada temperatures. Escribe siguiente y pulsa enter.

CREATE DATABASE temperatures;

Seleccinamos la base de datos de la siguiente manera.

USE temperatures;

A continuación, debe crear un usuario de base de datos y otorgar acceso a la base de datos. (Cambie la contraseña a otra cosa si lo desea). Para hacer ese tipo, escriba las siguientes líneas por separado y después de cada presine enter
CREATE USER 'logger'@'localhost' IDENTIFIED BY 'password';

GRANT ALL PRIVILEGES ON temperatures.* TO 'logger'@'localhost';

FLUSH PRIVILEGES;

Ahora el usuario ha sido creado y los privilegios añadidos. Es hora de cambiar de usuario de root a este nuevo registrador. Cierre la sesión escribiendo a continuación y presionando enter.

quit

Y vuelva a iniciar sesión con este nuevo usuario escribiendo siguiente y presionando enter

sudo mysql -u logger -p -h localhost

Y proporcione la contraseña que asignó después de IDENTIFIED BY al crear el usuario (de forma predeterminada, era password).
Ahora es el momento de crear dos tablas. La temperatura para almacenar la información del sensor y el tiempo de medición y también el registro de correo que contiene información cuando se han enviado avisos de límite de temperatura. Mailsendlog se usa en el código para verificar cuándo se envió la última advertencia y se ha restringido que la advertencia solo se puede enviar dentro del límite de tiempo de espera de envío de correo establecido en las configuraciones. Esta restricción es necesaria para que el buzón no se inunde en los casos en que las mediciones se realizan con frecuencia, por ejemplo. Cada minuto y cada medida provoca una advertencia.

Sin embargo, hay pocas excepciones cuando se ignora esta verificación y es en los casos en que la temperatura o la humedad aumentan o disminuyen más de lo que permiten los límites del sensor entre las mediciones. Piense en el caso cuando está registrando la temperatura del hogar a través de este registrador y de repente hay una enorme caída de temperatura entre las mediciones, sería bueno obtener información sobre eso, incluso si el tiempo de espera establecido para el envío de correo aún no ha pasado.

Algunas advertencias, como el sensor no se puede leer, o la inserción de la base de datos falla, se envían cada vez que ocurren. Estas advertencias indican que hay algo mal con la Raspberry Pi o los sensores y se deben revisar de inmediato.

Para comenzar a crear tablas, escriba lo siguiente y presione enter.

USE temperatures;

Cree la primera tabla con columnas de datos, tiempo, sensor, temperatura y humedad. Para hacer eso escribe lo siguiente y pulsa enter.

CREATE TABLE temperaturedata (dateandtime DATETIME, sensor VARCHAR(32), temperature DOUBLE, humidity DOUBLE);

Cree la segunda tabla con las columnas dateandtime, triggedsensor, triggedlimit y lasttemperature. Para hacer eso escribe lo siguiente y pulsa enter.

CREATE TABLE mailsendlog (mailsendtime DATETIME, triggedsensor VARCHAR(32), triggedlimit VARCHAR(10), lasttemperature VARCHAR(10));
Puede confirmar que los conjuntos vacíos están presentes escribiendo lo siguiente y presionando enter.

SELECT * FROM mailsendlog;

SELECT * FROM temperaturedata;

Si existen tablas, deberías ver "Empty Set (0.00 sec)"

La base de datos y las tablas ahora están configuradas, salga de la consola MySql escribiendo lo siguiente y presione Entrar.

quit

Luego reinicie mysql para que los cambios surtan efecto. Para hacer eso escribe lo siguiente y presiona enter.

sudo /etc/init.d/mysql restart

Eso es todo, mysql y la base de datos está lista. Lo siguiente es descargar Lectura de sensores para leer sensores e insertar datos en estas nuevas tablas.
Paso 7: Configuramos el lector de sensores


El código Python de DatCenter también se puede encontrar en github, al igual que en los códigos DHT22 de Adafruit.

NOTA: Si es la primera vez que lo hace, puede saltar a "Configuración" algunas líneas a continuación. Pero si ya ha realizado este paso anteriormente y ahora hay arreglos / actualizaciones en github que también desea en su configuración, debe recuperar el código nuevamente.

La carpeta puede eliminarse y clonarse nuevamente o recuperarse y restablecerse con Git. De cualquier manera, primero haga una copia de seguridad de las configuraciones del archivo json, haga una copia de seguridad también de las copias de seguridad de SQL de la carpeta DHT22-TemperatureLogger / Backups, luego elimine la carpeta DHT-TemperatureLogger.

Para eliminar y volver a clonar la carpeta, asegúrese de estar en la carpeta que contiene DHT22-TemperatureLogger. p.ej. tipo:

cd /home/pi

y eliminar la carpeta escribiendo

sudo rm -r DataCenter/

Ahora puede volver a clonar desde GIT y restablecer las configuraciones con los pasos que se mencionan a continuación en "Configuración". Notable es que si hubo cambios también en las configuraciones del archivo json (por ejemplo, nuevas configuraciones), no puede copiar el archivo antiguo respaldado tal como está.

Para Git buscar y restablecer

Vamos a l folder DataCenter/

tecleamos git remote -v y nos mostrara la version que tenemos instalada:

origin https://github.com/jjpFin/DHT22-TemperatureLogger... (fetch)
origin https://github.com/jjpFin/DHT22-TemperatureLogger....(push)

Para obtener la ultima version de git fetch --all

and reset folder to match latest version with git reset --hard

If Git approach didn't work, you can always just delete and re-clone as mentioned above.


Setting up.

Make sure that you are in folder where you want to install the DHT22-TemperatureLogger, by default i would suggest /home/pi/. Type in the folder and press enter.

cd /home/pi

Now clone git repository by typing

git clone https://github.com/jjpFin/DHT22-TemperatureLogger....

Type

ls

and press enter. And you should see that TemperatureLogger is unpacked to new DHT22-TemperatureLogger folder (image attached). Now to get this to work with Adafruit code and your MySql database that was just created, some configurations are needed. Start by editing the settings. To do this go to DHT22-TemperatureLogger folder by typing following and pressing enter

cd /home/pi/DHT22-TemperatureLogger

Now open config.json in editor. Type in the following and press enter.

sudo nano config.json

Configuration file opens up in editor (reference image attached).

Start going through the configurations and make them match your configurations.

mysql: Change mysql part to match what was created in mysql creation phase.

sensors: Create configurations for sensors attached to your RPI. Notable is that each sensor need to have own configuration line.

name: Set names for your sensors, e.g. outside, inside, livingroom, kitchen and so on. Where that sensor is going to be located or how you want to name it in log. Also add GPIO from where sensor is found. Other values are triggerlimits.

SensorType: Keep this as 22 with dht22 sensor, this is here in case that i will later add support for other sensors as well. (However I think that DHT11 should work, but haven't tested it. Try it out...)

Temperature low and high are limits for triggering email warnings. E.g. if sensor low liimit is 0 and temperature on that location drops below 0, you will receive warning to email address that you assign later. Same goes with high limit. If temperature gets higher than set limit. Warning is sent.

Humidity limits works exactly like temperature limits, but send warnings if humidity received from sensor doesn't fit between the limits

Threshold is used for measuring if temperature or humidity drops more than set limit between 2 measurements. As example, TemperatureThreshold is set to 5, last measurement was 10 and on next measurement you get 0. This means that 5 or 15 would be ok, but anything below or above that is more than threshold and email warning is triggered. Use case for this is to follow if temperature raises or drops too quickly in monitored location.

NOTE: There is two example rows here for two sensors. If you want to attach more, just copy and paste more lines and edit values.

mailInfo: This is for sending those email warnings. (I created new gmail just for this purpose) NOTE CURRENTLY ONLY GMAIL IS SUPPORTED

Senderaddress: This is shown in receivers inbox as sender

Receiveraddress: Where do you want to sent these warnings

Username: username for sender email

Password: password for sender email

subjectMessage: Can be changed if you want to, this is subject of the sended email in normal case

subjectWarning: This can also be changed, this is sended in case that warning is triggered (e.g. temperature is below triggerlimit)

sqlBackupDump: Backup dumps are either once a week or daily now.

BackupDumpEnabled y/n indicates if backup dumps are wanted in first place.

backupDay is day of the week when dump is taken. 1-7 (Monday to Sunday) 0 daily.

backupHour is the hour of the day when dump is taken- 0-24

backupDumpPath is the path where dump is stored. By default it is in Backups folder.

Every dump is automatically created to own datetime folder in this directory. Note that this folder isn't automatically backed up to any location. You need to copy it manually every now and then.

weeklyAverages: Used to define if weekly average temperatures are sent and on which day. This is done in order that you can be sure that logger is up and running even though warnings haven't been sent recently.

weeklyAveragesSendingEnabled: y means enabled, anything else means it is disabled.

weekDayForSendingAverages: is day of the week when dump is taken. 1-7 (Monday to Sunday)

hourOfTheDayForSendingAverages: is the hour of the day when dump is taken 0-24.

useFahrenheits: y enabled, n disabled. Note that if you change to fahrenheits and back to celsius "on the fly", you might get some warning mails about exceeded threshold limits or broke limits.

mailSendingTimeoutInFullHours: 0-x

Used to reduce spam. If set to 0, logger will send mail from every warning. Bigger values allow it to send warnings only once per hour. Used so that mailbox doesn't get flooded in case that measurements are done frequently and every measurement causes mail notification to be sent.

adafruitPath: This is the path where Adafruit_Python_DHT was downloaded from Git in beginning. By default it was /home/pi/Adafruit_Python_DHT/ Script AdafruitDHT.py This is important as it is used to get readings from each connected sensor.

Once settings are set, press Ctrl+x and save when prompted with "Y". Now test that readings are written to database correctly In DHT22-TemperatureLogger folder, type following and press enter.

python DHT22logger.py

If everything goes as planned, Raspberry executes the python script, gets readings from sensor/s and writes them to database. If you cant see any errors, all seems to be working. Now check database that data is inserted. Go to mysql console by typing following and pressing enter.

sudo mysql -u logger -p -h localhost

And log in with your password. In mysql console type following and press enter.

use temperatures;

And then type (and press enter)

select * from temperaturedata;

And check that readings were saved to table (reference image)

If everything seems to be in order and you can see the readings, exit mysql by typing following and pressing enter

quit

Note that mailsendlog table is empty at this point as no warning mails have been send. However, if you have only one sensor attached, but in configs sensor amount setting is more than 1, you will get email indicating that sensor couldn't be read. These kind of warnings are send always if they occur and are not logged.
Step 11: Automatical Sensor Reading
Picture of Automatical Sensor Reading

Now that temperature logger seem to be working, you probably want to take measurements automatically every n minutes all the time when Raspberry is powered on. To do so add timed event to crontab scheduler

Type following and press enter.

crontab -e

Rpi will prompt that "no crontab for pi - using empty one" and gives options to selecting editor.

Select option 2. /bin/nano and crontab should open up.

Add the following line at the end of the file (check reference image). This will run the script every 15 minutes.

*/15 * * * * python /home/pi/DHT22-TemperatureLogger/DHT22logger.py

More information about setting the crontab job can be found from here http://www.thesitewizard.com/general/set-cron-job...

Quit and save with Ctrl+x and select "Y" when prompted

Wait for 15-20 minute (or reduce time to wait less) and check that new inserts are done to mysql table. If yes, everything is now set up…and logger is working automatically and inserting data to MySql & sending mails.

Next thing thing is to set up LAMP (Linux, Apache, MySQL, PHP) and serve MySql information to web page. This way you can check the current readings with any web enabled device.
Step 12: LAMP (Linux, Apache, MySQL, PHP) and Data to Web Page
Picture of LAMP (Linux, Apache, MySQL, PHP) and Data to Web Page
Picture of LAMP (Linux, Apache, MySQL, PHP) and Data to Web Page
Picture of LAMP (Linux, Apache, MySQL, PHP) and Data to Web Page

First type in

sudo apt-get update

to update again. After update finished. Install apache2 web-server (and addons) so that you can serve temperaturelogger web page to client.

sudo apt-get install
apache2 php7.0 php7.0-curl php7.0-gd php7.0-imap php7.0-json php7.0-mcrypt php7.0-mysql php7.0-opcache php7.0-xmlrpc libapache2-mod-php7.0

After install finished restart apache server by typing

sudo /etc/init.d/apache2 restart

Now the web server is ready and can serve your first web-page.

On your PC web-browser type in the IP address of the raspberrypi and you shdould see the apache landing page. (same as in attached picture)

Good, now change html page to PHP and get data for the page from temperatures database. Go to location from where the index.html page is served. Type

cd /var/www/html/

Note: location used to be /var/www/ but has since changed to /var/www/html/

Check that you are in correct folder and actually have the index.html in this folder by typing

ls

You should see that there is index.html in this page (attached reference image 2)

Create the index.php page and copy following code section to it. Type in.

sudo nano index.php

Editor opens up. Copy the code from attached index.php.txt file to the editor. Remember to change settings to match your MySql settings. And you can also change how many hours backwards temperatures are seen in web page by editing $hours variable.

When ready Exit with Ctrl+X and save with "Y" when prompted

Now remove the index.html, so that next time page is loaded index.php is used by typing

sudo rm index.html

Then once again, on your PC web-browser type in the IP address of the raspberrypi and you should see the page, but this time with temperature information from your MySql database (attached image as reference).

Good, you are almost finished. Last thing to do is installing dynamic DNS so that you can connect this page with www. instead of IP.




Thanks and best regards,

JJ
