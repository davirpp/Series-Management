# Series Management
 
## A simple Python (like)CLI Program using PostgreSQL database for management of serie's progress

### How to use it

* First of all you need a database to make the connection and save your progress and [ElephantSQL](https://www.elephantsql.com/) is an amazing service site where you can host your PostgreSQL database for free;

* Then you have to use [requirements.txt](https://github.com/davirpp/Series-Management/blob/main/requirements.txt), doing on the terminal ```pip install -r requirements.txt```

* After you build your database with the SQL script [serie_query.sql](https://github.com/davirpp/Series-Management/blob/main/serie_query.sql), you can go to [treatment.py](https://github.com/davirpp/Series-Management/blob/main/treatment.py) to edit the initial part of the python file to put the database credentials and edit in line [185](https://github.com/davirpp/Series-Management/blob/main/treatment.py#L185) a path where you want to save the local backup file;

* Finally you can go to [main.py](https://github.com/davirpp/Series-Management/blob/main/main.py) and run the program;

* __IMPORTANT NOTE__: If you don't want to use IDE or something like that to use the program, if you use Windows you can make a .bat file like [here](https://github.com/davirpp/Series-Management/blob/main/Series_Management.bat) to use it smoothly

* Inside the program you can make an Excel backup file with the same configuration as the database;
	* You can find an example on [series_backup.xlsx](https://github.com/davirpp/Series-Management/blob/main/series_backup.xlsx);
	
### Examples

* Main Menu

	![Main_Menu](https://github.com/davirpp/Series-Management/blob/main/using-images/Main_Menu.png)
	
	
* Option 1

	![Option_1](https://github.com/davirpp/Series-Management/blob/main/using-images/Option_1.png)
	
* Option 2
	
	![Option_2](https://github.com/davirpp/Series-Management/blob/main/using-images/Option_2.png)
