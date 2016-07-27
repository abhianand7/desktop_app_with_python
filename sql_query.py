import kivy

kivy.require('1.9.1')

import popup
import log
import sql_connect


def query_sql(*args):
    # print exec_cmd, pwd
    exec_cmd = args[0]
    db, cursor, flag = args[-4], args[-3], args[-2]
    number_of_arguments = len(args)
    number_of_var_in_sql_cmd = [args[-1] for i in range(1) if args[-1] != args[0]][0]
    valid_database_flag = args[-2]
    if valid_database_flag:

        # here rows gives the number of rows available in the output after executing the command
        if number_of_var_in_sql_cmd == 0:
            rows = cursor.execute(exec_cmd)
        elif number_of_var_in_sql_cmd == 1:
            rows = cursor.execute(exec_cmd.format(args[1]))
        elif number_of_var_in_sql_cmd == 2:
            rows = cursor.execute(exec_cmd.format(args[1], args[2]))
        elif number_of_var_in_sql_cmd == 3:
            rows = cursor.execute(exec_cmd.format(args[1], args[2], args[3]))
        elif number_of_var_in_sql_cmd == 4:
            rows = cursor.execute(exec_cmd.format(args[1], args[2], args[3], args[4]))
        elif number_of_var_in_sql_cmd == 5:
            rows = cursor.execute(exec_cmd.format(args[1], args[2], args[3], args[4], args[5]))
        elif number_of_var_in_sql_cmd == 6:
            rows = cursor.execute(exec_cmd.format(args[1], args[2], args[3], args[4], args[5], args[6]))
    return cursor, rows
