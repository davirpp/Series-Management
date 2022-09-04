from treatment import *
import os


p_n = " SERIES ON CLOUD "
os.system(cleaning)
user_input = input(f"""{p_n.center(21, '=')}

What do you wanna do:

1) List finished series
2) List ongoing series
3) Add a finished serie
4) Add an ongoing serie
5) Update serie's episode
6) Delete a serie
0) Close the application and save changes

Your option(digit): """)

os.system(cleaning)
print('\nCONNECTING...')

while True:
    # Instantiating the class everytime to update the DB
    mySerie = Series()
    match user_input:
        case '0' | '':
            print('\nYou are closing the program... ')
            break
        case '1':
            mySerie.show_final_df()
        case '2':
            mySerie.show_ongoing_df()
        case '3':
            mySerie.add_finished_serie()
        case '4':
            mySerie.add_ongoing_serie()
        case '5':
            mySerie.update_serie()
        case '6':
            mySerie.delete_serie()
        case 'backup':
            mySerie.backup()
        case _:
            print('\nYour number is not an option. Try again...')

    print()
    input('Press any key to continue. . .')
    os.system(cleaning)
    user_input = input(f"""{p_n.center(21, '=')}
    
What do you wanna do:

1) List finished series
2) List ongoing series
3) Add a finished serie
4) Add an ongoing serie
5) Update serie's episode
6) Delete a serie
0) Close the application and save changes

Your option(digit): """)

print('\nYour changes have been saved!\n')
