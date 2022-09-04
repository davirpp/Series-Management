import pandas as pd
from tabulate import tabulate
import psycopg2 as pg
from sqlalchemy import create_engine
import sys


match sys.platform:
    case "win32":
        cleaning = 'cls'
    case "linux":
        cleaning = "clear"

# String connection
engine = create_engine("postgresql://user:password@"
                       "host:port/database")
# The necessary things to do the connection
connection = pg.connect(user='',
                        password='',
                        host='',
                        port='',
                        database='')
curs = connection.cursor()


class Series:
    """ Class using CRUD among the series' DataFrames """

    def __init__(self):
        """ Constructor that instantiate the class reading the Database and putting into DataFrames """

        sql_final = "SELECT name FROM series WHERE finished = 'true' ORDER BY name;"
        self.__data_frame_final = pd.read_sql_query(sql_final, con=engine)

        sql_ongoing = "SELECT name, season, episode FROM series WHERE finished = 'false' ORDER BY name;"
        self.__data_frame_ongoing = pd.read_sql_query(sql_ongoing, con=engine)

    def show_final_df(self):
        """ Method to list the finished series """

        print("\nYour finished series: ")
        print(tabulate(self.__data_frame_final, headers=['Serie'], tablefmt='pretty'))

    def show_ongoing_df(self):
        """ Method to list the ongoing series """

        print("\nYour ongoing series: ")
        print(tabulate(self.__data_frame_ongoing, headers=['Serie', 'Season', 'Episode'], tablefmt='pretty'))

    def add_finished_serie(self):
        """ Method to add finished series being in ongoing series or not """

        # Input to know if the serie to be added is ongoing or not
        user_input = input(f"\nWas this serie an ongoing one?\n0) No\n1) Yes\nYour answer(digit): ")

        if user_input == '1':
            self.show_ongoing_df()
            u_input = int(input("\nType the digit of the serie: "))

            finished = self.__data_frame_ongoing['name'][u_input]
            sql_delete = f"UPDATE series SET finished = 'true' WHERE name LIKE '{finished}';"
            sql_delete += f"UPDATE series SET season = null WHERE name LIKE '{finished}';"
            sql_delete += f"UPDATE series SET episode = null WHERE name LIKE '{finished}';"

            curs.execute(sql_delete)
            connection.commit()

            print(f"\n'{finished}' updated in the database!")
            return

        elif user_input == '0':
            finished = input('What is the name of the finished serie: ').title()
            sql_insert = f"INSERT INTO series(name, finished) VALUES ('{finished}', 'true')"

            curs.execute(sql_insert)
            connection.commit()

        else:
            print('\nNot available option!')
            return

        send_message(finished, 'add')

    @staticmethod
    def add_ongoing_serie():
        """ Method to add ongoing series """

        serie_name = input('\nWhat is the name of the serie: ').title()
        serie_season = int(input('What is the season that you started(digit): '))
        serie_episode = int(input('What is the next episode(digit): '))

        sql_insert = f"INSERT INTO series(name, season, episode, finished) " \
                     f"VALUES('{serie_name}', {serie_season}, {serie_episode}, 'false')"

        curs.execute(sql_insert)
        connection.commit()

        send_message(serie_name, 'add')

    def update_serie(self):
        """ Method to update ongoing series """

        self.show_ongoing_df()
        user_input = input('\nType the number of the serie: ')

        if user_input == '':
            print('\nBacking to menu!')
            return

        user_input = int(user_input)
        try:
            serie = self.__data_frame_ongoing['name'][user_input]
        except KeyError:
            print("\nSerie's number not found!")
            return

        print('\nSelected:')
        print(tabulate([self.__data_frame_ongoing.iloc[user_input]], headers="keys", tablefmt='pretty'))

        u_input = input('\nDo you want to update:\n1) The season\n2) The episode\n3) Both\nYour option(digit): ')

        if u_input == '1':
            season_input = int(input('\nType the number of the new season: '))
            sql_update = f"UPDATE series SET season = {season_input} WHERE name LIKE '{serie}';"

        elif u_input == '2':
            episode_input = int(input('\nType the number of the new episode: '))
            sql_update = f"UPDATE series SET episode = {episode_input} WHERE name LIKE '{serie}';"

        elif u_input == '3':
            s_input = int(input('\nFirst, type the number of the new season(digit): '))
            e_input = int(input('Type the number of the new episode(digit): '))
            sql_update = f"UPDATE series SET season = {s_input} WHERE name LIKE '{serie}';"
            sql_update += f"UPDATE series SET episode = {e_input} WHERE name LIKE '{serie}';"

        else:
            print('\nNot available option!')
            return

        curs.execute(sql_update)
        connection.commit()

        send_message(serie, 'up')

    def delete_serie(self):
        """ Method to delete any serie """

        user_input = input("\nDo you want to delete:\n0) Finished serie\n1) Ongoing serie\n\nYour option(digit): ")

        if user_input == '0':
            self.show_final_df()
            u_input = int(input("\nType the digit of the serie to be deleted: "))

            try:
                serie = self.__data_frame_final['name'][u_input]
            except KeyError:
                print("\nSerie's number not found!")
                return

        elif user_input == '1':
            self.show_ongoing_df()
            u_input = int(input("\nType the digit of the serie to be deleted: "))

            try:
                serie = self.__data_frame_ongoing['name'][u_input]
            except KeyError:
                print("\nSerie's number not found!")
                return

        else:
            print('\nNot available option')
            return

        sql_delete = f"DELETE FROM series WHERE name LIKE '{serie}';"

        curs.execute(sql_delete)
        connection.commit()

        send_message(serie, 'del')

    @staticmethod
    def backup():
        sql = "SELECT * FROM series ORDER BY finished, name"
        df = pd.read_sql_query(sql, con=engine)
        df.to_excel("~/Documents/series_backup.xlsx", index=False)
        print('\nBackup done successfully!')


def send_message(serie, add_del_up):
    """Function that send the specific message of what is going on with the manipulation on the Database"""

    action = connector = None

    match add_del_up:
        case 'add':
            action, connector = 'added', 'to'
        case 'del':
            action, connector = 'deleted', 'from'
        case 'up':
            action, connector = 'updated', 'in'

    # Alternative way for who don't have python 3.10
    #
    # dict1 = {'add': ('added', 'to'),
    #          'del': ('deleted', 'from'),
    #          'up': ('updated', 'in')}
    #
    # action, connector = dict1[add_del_up]

    print(f"\n'{serie}' {action} {connector} the database!")
