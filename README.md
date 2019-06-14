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

Se agregó tiempo de espera configurable para el envío de correo, de modo que el usuario pueda decidir cuánto espera el registrador antes de enviar las advertencias después del correo enviado previamente. Anteriormente, se usó un valor codificado y resultó poco inconveniente

El volcado de copia de seguridad del SQL ya no es diario, el usuario establece el día en que se realiza el volcado. 0 es diario, 1-7 es de lunes a domingo.

Las temperaturas medias semanales de envío ahora también son configurables. Funciona con el mismo patrón que el volcado de SQL anterior. 0 es diario, 1-7 es de lunes a domingo. Tenga en cuenta que siempre contará 7 días atrás y enviará el promedio de esos.

Posibilidad de elegir entre Fahrenheits o Celsius

Y algunos retoques más menores y arreglos.


---------------------------------------------------------------------------------------

This is an Raspberry Pi based temperature and humidity logger that uses Adafruit DHT22 sensors for measurements. You might have seen similar kind of instructions before, but this one has a twist. It doesn't just read temperature and humidity from sensors, but it stores data to database and provides means to read that temperature data with any web enabled device (computer, phone, tablet) web browser. This logger also allows you to set limits for temperatures and is able to send email if sensor temperature or humidity exceeds set limits...this neat feature can be for example used to alarm when it is time to set heating on in your house / carage / greenhouse / you name it.

To complete this instructable, you will need following:

- Raspberry PI (I used Raspberry PI 1 model B+, but should be doable with other models as well)

- Power supply for the pi. (I used old Nokia microusb telephone charger which gives about 880mA)

- SD memory card. Note that you might need adapter. (I used 8Gb and had 4.1Gb available after installing everything)

- Ethernet cable or USB wlan dongle that is supported by Raspberry Pi (google can help with this)

- DHT22 sensor/s and 4.7 kOhm resistors. Instructable supports 1-n sensors. https://www.adafruit.com/products/385

- Cables and breakout for connection https://www.adafruit.com/products/914

- Computer where you set up the SD card for the raspberry PI and from where you can connect and do the configurations. (NOTE: this instruction uses PC)

- Optional: Breadboard. Test assembly is easier to be created on this, than by connecting wires directly to sensors: http://thepihut.com/products/raspberry-pi-breadbo...

Internet connection is also require in location where you are going to set the raspberry logger. Either via ethernet or wlan dongle.

Keyboard + display are needed as well while installing and configuring the Wheezy OS. But once installations are finished, network is up and SSH enabled, it is possible to use connect raspberry pi remotely from PC and keyboard + display can be put aside.
Step 1: Sensor and RPI Assembly
Picture of Sensor and RPI Assembly
Picture of Sensor and RPI Assembly

Create assembly as instructed in attached image. Image instructs how you can connect two DHT22's to the Raspberry Pi, but if you have only one available just ignore another one and add one. And vice versa, if you have more sensors add them to free ground, power and gpio pins.

Notable here is that you can connect sensors to any GPIO you like. I had mine connected in GPIO22 and GPIO23. Both sensors also need +3.3Volts and ground. Resistor is set between +3.3V line and GPIO line.

When assembly is ready, prepare SD card and go to next step.
Step 2: OS for the RPI
Picture of OS for the RPI

Previously Wheezy was selected OS for this instructable. But that has long since changed and the link was dead as well. Instead, get Raspbian-Stretch-Lite image from here to your computer https://www.raspberrypi.org/downloads/raspbian/

And get also Win32 Disk Imager http://sourceforge.net/projects/win32diskimager/

Start Win32 Disk Imager and set the location of the downloaded Os image (.img file) to "Image File". Select the drive where your SD card is and select "Write".

Imager asks to Confirm Overwrite. Double check that drive is correct and select "Yes". Wait for write to finish. When Disk Imager informs that write is completed and successful press "OK", close the Disk Imager and eject the SD card from computer.

Place the card to your Raspberry Pi and go to next step.
Step 3: Setting Up Raspberry Pi

Set SD card to Raspberry Pi and power it up by plugging the power supply to Raspberry Pi's micro-usb. (Remember to attach keyboard and display before you insert power supply).

Rasperry Pi starts to boot up and will prompt for username and password.

By default those are:

username: pi

password: raspberry

After boot up finished start the configuration tool by typing

sudo raspi-config

In configuration tool, do the following:

1. Change your password and give new password to Raspberry Pi

2. Open network options -> 2.1 Change name if you want to -> 2.2 Enter wi-fi information (ssid, password)

3. Make sure that Raspberry Pi boots to console by selecting option 1, console.

4.This is optional, but it is advised that you set up locale information correctly. If you want to change internationalization options e.g. keyboard layout, timezone.

5. From interfacing options, select P2 - SSH and enable it This allows you to connect to RPI with SSH from your computer. This way you don't need display or keyboard on RPI to use it

6.Don't do anything

7. Open advanced options -> 7.1 Expand filesystem

8. Optional

Finally go to "Finish" and restart RPI by typing

sudo reboot

Configuration is now ready. Next step is to check how it can be connected remotely from PC.
Step 4: Connect Your Raspberry Pi From PC Part 1
Picture of Connect Your Raspberry Pi From PC Part 1
Picture of Connect Your Raspberry Pi From PC Part 1

Raspberry Pi is now configured and booted up. You should be able connect it via PuTTY from your PC now. PuTTY can be downloaded from http://www.chiark.greenend.org.uk/~sgtatham/putty...

When you start up the PuTTY you will notice that Host name or IP is required in order to connect to your Raspberry PI. To obtain the Raspberry Pi's IP address. Type the following to Raspberry Pi and press enter

Ifconfig

This will list you network adapters and information from them (check image). If you are connected with Ethernet (like I was at this point) you should see inet addr:xxx.xxx.xxx.xxx in eth0. by typing this inet address to PuTTY's host name line you should be able to connect Raspberry Pi remotely.

If you set up Wlan in previous step, you should also see wlan0 information, inet addr: etc. You can connect using those as well.

There is also manual way to configure WLAN. It was used earlier with Wheezy OS and it is described in next page. If you have network setup already, you can skip it and continue with how to connect with PuTTY.
Step 5: Optional: Wlan Configuration to Raspberry Pi
Picture of Optional: Wlan Configuration to Raspberry Pi

Manual way of adding Raspberry Pi WLAN settings.

You need to set wlan ssid and password to configuration so that Raspberry Pi can connect it.To start type following and press enter.

sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

Add network section and configurations to the end of the file (check above image for reference):

Network={

ssid="yourssid"

psk="passwordtoyourwlan"

}

Save with Ctrl+X and select "Y" to confirm save.

Now restart Raspberry Pi. Type following and press enter.

sudo reboot

Once booted up and logged in, type following and press enter.

Ifconfig

You should now see that also wlan0 has inet addr available.
Step 6: Connect Your Raspberry Pi From PC Part 2
Picture of Connect Your Raspberry Pi From PC Part 2
Picture of Connect Your Raspberry Pi From PC Part 2
Picture of Connect Your Raspberry Pi From PC Part 2

Now the IP (ethernet or wlan) address is known. You can now connect via PuTTY from your windows desktop. To do so, open putty, type in IP address and port 22 and select open.

Say yes to security alert and command line opens up in PuTTY.

Type in login name and password and now you should be in pi's command prompt. This means that you can now disconnect keyboard and display from Raspberry Pi and do all the rest of the steps from your pc via PuTTY. To shutdown pi (just in case when disconnecting keyboard and display) type following and press enter.

sudo shutdown -h now

Raspberry Pi will shut down. Once you have disconnected keyboard and display disconnect power supply and put it back in to boot up the Raspberry Pi. Wait for a moment (so Raspberry Pi boots up) and then try to connect again via PuTTY, if everything works like it should you should be now able to login...if you get timeout at first, wait for a moment and try again.

NOTE: IP address can change if your routers DHCP gives new IP address to the Raspberry Pi during bootup / reset and therefore you should know the new IP in order to connect again via PuTTY.

To avoid this problem, you have option to set in static ip address for the Raspberry Pi…there is few guides how to do that. E.g. try this http://www.modmypi.com/blog/tutorial-how-to-give-...

Or then you can do like I did (if your router allows it), add address reservation to Raspberry Pi's wlan adapter MAC address in router configurations. I have tplink router so i added MAC address and reserved currently assigned IP address for it. For this trick, you need both, IP address and MAC. Againy type following and press enter.

ifconfig

Take note from hwaddr (this is the Mac and inet addr which is the IP)Then create address reservation to your DHCP / address reseravtion list. Check your routers user guide to see how this can be done in your own router. I have TPLink so Address Reservation looks exactly like in attached image.

Now everything is set up and we can get to the fun part.
Step 7: Installing DHT22 Sensor Libraries

Start by updating and upgrading the Raspberry Pi. Type following and press enter.

sudo apt-get update

This updates software sources then type following and press enter.

sudo apt-get upgrade

This updates to everything to latest version. If prompted to continue press "Y".

When these are finished, it is time to install Adafruit Python code. You will need this code in order to get readings from DHT22 sensors. This will also allow you to test that your assembly works in first place.

At first, get compiler and python library. For that type following and press enter

sudo apt-get install build-essential python-dev python-openssl

Then, make sure that you are in folder where you want to install the Adafruit code, by default i would suggest /home/. For that type following and press enter.

cd /home/pi

In stretch lite, you also need to install Git separately as it is not included by default. To do so, type:

sudo apt-get install git


Now clone the git repository. Type following and press enter.

git clone https://github.com/adafruit/Adafruit_Python_DHT.g...

Go to folder.Type following and press enter.

cd Adafruit_Python_DHT


And finally install the Adafruit library. Type following and press enter.

sudo python setup.py install

Then it is time to test your assembly...
Step 8: Testing the DHT22's
Picture of Testing the DHT22's

Now that installation is completed you can test the connected sensor/s and see that you get reading from them. Go to folder where you cloned the Adafruit_Python_DHT and then to examples folder. Type following and press enter.

cd /home/pi/Adafruit_Python_DHT/examples

You remember the gpio/s where you plugged the sensor/s? Good, then type sudo ./AdafruitDHT.py and press enter. I had gpio 22 and 23 so I tested with

sudo ./AdafruitDHT.py 22 22

sudo ./AdafruitDHT.py 22 23

If your sensor and assembly is ok, you should get back temperature and humidity from the sensor/s. Like seen in attached image.

NOTE:

If you see "Failed to get reading. Try again!", then try again few times.

If still nothing, re-check that you typed in the right GPIO.

If gpio is for sure right, check your assembly again. E.g. DHT22 gets power, ground and resistor is connected correctly.

If all above are right, try to connect your sensor to another GPIO and see if you get reading from that

If nothing from above works, it is always possible that your DHT22 is broken. :(

Libraries for DHT22 sensors are now installed and you can get the readings from sensor/s. Time to set up database for holding that data.
Step 9: Setting Up the MySql for Storing the Temperature Data
Picture of Setting Up the MySql for Storing the Temperature Data

Get Mysql/MariaDb and required addons for it. To do that type following and press enter.

sudo apt-get install mysql-server python-mysqldb

Note: You won't be queried for password for ROOT user anymore during the installation. This is empty by default.

After installation completed. It is time to set up the actual database and tables for storing the data. This need to be done in mysql console. To get into console type in the following and press enter.

sudo mysql -u root -p -h localhost

Hit enter (empty) for password and you should be in MariaDb console

In console

First, create database called temperatures. Type following and press enter.

CREATE DATABASE temperatures;

Select the created database by typing following and pressing enter.

USE temperatures;

Next you need to create database user and grant access to database . (Change password to something else if you like).To do that type in the following lines separately and after each press enter (check reference image 2).

CREATE USER 'logger'@'localhost' IDENTIFIED BY 'password';

GRANT ALL PRIVILEGES ON temperatures.* TO 'logger'@'localhost';

FLUSH PRIVILEGES;

Now the user has been created and privileges added. Time to change user from root to this new logger. Log out by typing following and pressing enter.

quit

And log back in with this new user by typing following and pressing enter

sudo mysql -u logger -p -h localhost

And give password that you assigned after IDENTIFIED BY when creating the user (by default it was password).

Now it is time to create two tables. Temperaturedata for storing sensor information and time of measurement and also mailsendlog that holds information when temperature limit trigged mail warnings have been sent. Mailsendlog is used in code to check when last warning was sent and it has been restricted that warning can be sent only within mail sending timeout limit set in configurations. This restriction is required so that mailbox is not flooded in cases where measurements are done frequently, e.g. every minute and every measurement causes warning.

However there is little exception when this check is ignored and that is in cases when temperature or humidity increases or decreases more than sensor limits allow, between measurements. Think of the case when you are logging home temperature via this logger and there is suddenly huge drop in temperature between measurements, it would be nice to get information about that even if set mail sending time out has not passed yet.

Some warnings, like sensor cannot be read, or database insert failed are send every time when they occur. These warning indicate that there is something wrong with Raspberry Pi or sensors and should be checked right away.

To start creating tables, type in the following and press enter.

USE temperatures;

Create first table with columns dateandtime, sensor, temperature and humidity. To do that type in the following and press enter.

CREATE TABLE temperaturedata (dateandtime DATETIME, sensor VARCHAR(32), temperature DOUBLE, humidity DOUBLE);

Create second table with columns dateandtime, triggedsensor, triggedlimit and lasttemperature. To do that type in the following and press enter.

CREATE TABLE mailsendlog (mailsendtime DATETIME, triggedsensor VARCHAR(32), triggedlimit VARCHAR(10), lasttemperature VARCHAR(10));

You can confim, that empty sets are present by typing in the following and pressing enter.

SELECT * FROM mailsendlog;

SELECT * FROM temperaturedata;

If tables exist, you should see "Empty Set (0.00 sec)"

Database and tables are now setup, exit the MySql console by typing in the following and pressing enter.

quit

Then restart mysql to changes take effect. To do that type in the following and press enter

sudo /etc/init.d/mysql restart

Thats it, mysql and database is ready. Next thing is to download the DHT22-TemperatureLogger for reading sensors, and inserting data to these new tables.
Step 10: Set Up the Temperature Logger Code
Picture of Set Up the Temperature Logger Code
Picture of Set Up the Temperature Logger Code
Picture of Set Up the Temperature Logger Code

TemperatureLogger Python code can also be found from github, just like the Adafruit DHT22 codes.

NOTE: If this is first time you are doing this, you can skip to "Setting up" few lines below. But if you already have done this step earlier and now there is fixes/update in github that is wanted on your setup as well, you need to fetch the code again.

Folder can either be removed and cloned again or fetched and reseted with Git. Either way, first backup configurations json file, backup also SQL backups from DHT22-TemperatureLogger/Backups folder, then remove DHT-TemperatureLogger folder.

To remove and re-clone the folder make sure you are on the folder that contains DHT22-TemperatureLogger. e.g. type:

cd /home/pi

and remove the folder by typing

sudo rm -r DHT22-TemperatureLogger/

Now you can re-clone from GIT and reset the configurations with the steps mentioned below in "Setting up". Notable is that if there were changes also to configurations json file (e.g. new configurations), you cannot copy the backed up old file back as is.

For Git fetch and reset

Go to DHT22-TemperatureLogger/ folder

type git remote -v and you should see something similar like this:

origin https://github.com/jjpFin/DHT22-TemperatureLogger... (fetch)
origin https://github.com/jjpFin/DHT22-TemperatureLogger....(push)

Fetch latest version with git fetch --all

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
