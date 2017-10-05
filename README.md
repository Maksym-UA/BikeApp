# Bike Catalog

## Flask Application

This project uses [SQLAlchemy](http://www.sqlalchemy.org/) (the Python SQL toolkit) and [Flask](http://flask.pocoo.org/)
(a microframework for Python based on [Werkzeug](http://werkzeug.pocoo.org/), [Jinja 2](http://jinja.pocoo.org/docs/2.9/))
to create and maintain database ov various bikes. 
Users can view, create, update and delete existing information. 

  
## SETUP

- You'll need to use a virtual machine (VM) to run an SQL database server and a web app that uses it. 
- You'll need to use Vagrant and VirtualBox to install and manage the VM. 
- You'll need to install Flask and SQLAlchemy which will have all the tools for buidling the web app.


### Installing Flask

In order to install Flask type in the Terminal:

	
    $ pip install Flask
    

### Installinf SQLAlchemy

In order to install SQLAlchemy type in the Terminal:

	
    $ pip install SQLAlchemy
   

### Installing VirtualBox

VirtualBox is the software that actually runs the virtual machine. You can download it from [virtualbox.org](https://www.virtualbox.org/) 
- Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not 
need to launch VirtualBox after installing it; Vagrant will do that.

    *Ubuntu users: If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. 
Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.*


### Installing Vagrant

Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. 
- Download it from [vagrantup.com](https://www.vagrantup.com/) Install the version for your operating system.

    *Windows users: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.*

   *If Vagrant is successfully installed, you will be able to run vagrant `--version`in your terminal to see the version number.
The shell prompt in your terminal may differ. Here, the `$` sign is the shell prompt.*

    ```
    $ vagrant --version
    ```

- You need to download [tournament folder](https://github.com/Maksym-UA/tournament). It configures your VM settings. The file may be located inside your Downloads folder. Change to this directory in your terminal with `cd`. Inside, you will find another directory called vagrant. Change directory to the vagrant directory.

    ```
    $cd Downloads/tournament
    $ ls
    Vagrantfile  tournament.py  tournament.sql  tournament_test.py  readme.md
    ```

- Start the virtual machine
- From your terminal, inside the vagrant subdirectory, run the command `vagrant up`. This will cause Vagrant to download the Linux 
operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

    ```
    $ vagrant up
    ```

- When vagrant up is finished running, you will get your shell prompt back. At this point, you can run `vagrant ssh` to log in to your newly installed Linux VM!

    ```
    $ vagrant ssh
    ```

- Inside the VM, change directory to `/vagrant/final_project` and look around with `ls`. Any file you create in one will be automatically shared to the other. 
This means that you can edit code in your favorite text editor, and run it inside the VM. Feel free to look through and edit all the files.
	
	```
    $cd /vagrant/final_project
    $ ls
    bikesdatabase.py  database_setup.py   project.py  readme.md  pg_config  fb_client_secrets.json  client_secrets.json templates static
    ```

- Files in the VM's `/vagrant` directory are shared with the `vagrant` folder on your computer. But other data inside the VM is not. 

- You can edit database_setup.py or bikesdatabase.py in any editor you prefer. When you finish simply run

	```
    $ python database_setup.py
    ```
	or
	
	```
    $ python bikesdatabase.py
    ```
	This will either setuo empty database or add bikes to the data accordingly.
	

- When you are ready to run the app, simply type in `/vagrant/final_project` directory at the shell prompt:

	```
    $ python project.py
    ```	
This will run the app on the specified address. At this very setup the app will run on `http://0.0.0.0:5000/login`. Now you can navigate through the app.

- To close connection you can simply type `exit` (or `Ctrl-C`) at the shell prompt.
	
	
	### Logging in and out from Vagrant
If you type `exit` (or `Ctrl-D`) at the shell prompt inside the VM, you will be logged out, and put back into your host computer's shell. To log back in, make sure you're 
in the same directory and type `vagrant ssh` again.

If you reboot your computer, you will need to run `vagrant up` to restart the VM.



### That's it you are ready to go! Feel free to make any changes to the provided code.


### CONTACT

Please send you feedback to

  max.savin3@gmail.com
