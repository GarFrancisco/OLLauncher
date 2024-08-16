# OLLauncher
 Minecraft launcher (Only for Windows) intended to facilitate the download of Mods to play on a server or individual. Developed in Python 3.12. Fully editable, open source.

[![LAUNCHER.png](https://i.postimg.cc/FHZ91Fc7/LAUNCHER.png)](https://postimg.cc/5XXcRVsV)

---------------
USE THE PROGRAM
---------------

1- Inside of "mods.zip", there are the necessary files for the forge 1.12.2 installation. If you want to change the Minecraft version, just remove all these files and zip the new ones.

2- The "mods.zip" file is intended for uploading the folder with the mods you want to use in your game. In addition, you can upload your game configuration file (options.txt) or the server configuration file (server.dat) so that anyone using the launcher will have a preset configuration and servers. 

3- The "program.exe" is the default application. If you have made any changes on the "mods.zip" or the multimedia directory you have to compile it again as follows (installing pyinstaller).:

In a console go to the path where you have saved the project:
pyinstaller --onefile --add-data "mods.zip;." --add-data "multimedia/background.png;multimedia" --add-data "multimedia/download.png;multimedia" --add-data "multimedia/img.ico;multimedia" --add-data "multimedia/play.png;multimedia" --add-data "multimedia/reinstall.png;multimedia" --add-data "multimedia/title.png;multimedia" -F -i multimedia/img.ico program.py

4- Once you have executed your "program.exe", the first time you open it, you will have “DOWNLOAD” as an option. Click on it to download the Forge with the world mod pack.

5- In case of error, there is the option to “REINSTALL MINECRAFT”, which removes the launcher files so you can click “DOWNLOAD” again. When you click on the option, 5 seconds will pass and the program will close, once you open it again, it will be ready to be downloaded again.

Before clicking on PLAY, you will have to choose a name (in this version, only the OFFLINE game is available, so if possible, choose the same name of your purchased account.

6- With the slider bar you can choose the RAM memory that the game will use. The minimum is 7GB, but it is recommended from 9GB to avoid performance problems (in case of big modpacks).

7- Once you click on PLAY, the game will load.

In "program.py" you will have the full code of the launcher.
