# Bike Catalog

## Flask Application

This project uses [SQLAlchemy](http://www.sqlalchemy.org/) (the Python SQL toolkit) and [Flask](http://flask.pocoo.org/)
(a microframework for Python based on Werkzeug, Jinja 2) to create and maintain database ov various bikes. 
Users can view, create, update and delete existing information. 

  
## SETUP

- You'll need to use a virtual machine (VM) to run an SQL database server and a web app that uses it. 
- You'll need to user Vagrant and VirtualBox to install and manage the VM. 

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

- Inside the VM, change directory to `/vagrant` and look around with `ls`. Any file you create in one will be automatically shared to the other. 
This means that you can edit code in your favorite text editor, and run it inside the VM.

- Files in the VM's `/vagrant` directory are shared with the `vagrant` folder on your computer. But other data inside the VM is not. 
For instance, the PostgreSQL database itself lives only inside the VM.


### Creating Your Database

- Before you can run the code or create tables, you'll need to use the create database command in `psql` to create the database. Use the name tournament for your database.
Then you can connect psql to your new database and create your tables from the statements you've written in tournament.sql. 

Use the command `\i tournament.sql` to import the whole file into psql at once. 
Remember, if you get your database into a bad state you can always `drop` tables or the whole database to clear it out.


### Logging out and in
If you type `exit` (or `Ctrl-D`) at the shell prompt inside the VM, you will be logged out, and put back into your host computer's shell. To log back in, make sure you're 
in the same directory and type `vagrant ssh` again.

If you reboot your computer, you will need to run `vagrant up` to restart the VM.


### Running the database

The PostgreSQL database server will automatically be started inside the VM. You can use the `psql` command-line tool to access it and run SQL statements. Run `\c tournament` to connect to the database.

    ```
    vagrant@vagrant:/vagrant/tournament$ psql
    vagrant=> \c tournament
    You are now connected to database "tournament" as user "vagrant".
    tournament=>
    ```


### That's it you are ready to go! Feel free to make any changes to the provided code.


### CONTACT

Please send you feedback to

  max.savin3@gmail.com

