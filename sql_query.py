import kivy

kivy.require('1.9.1')

import popup
import log
import sql_connect

# args passing structure
# args[0] = SELECT {0} FROM {1} WHERE name='{2}'
# number of inputs required above by sql command is passed successively to args
# args[1] = column_name ({0} = column_name)
# args[2] = table_name ({1} = table_name)
# args[3] = field_name ({2} = field_name)
# args[4] = db (passed from sql_connect)
# args[5] = cursor (db cursor passed from sql_connect)
# args[6] = valid_database_flag (passed from sql_connect)
# args[7] = number_of_var_in_sql_cmd (in this case it is 3)
# finally this is combined as
# "SELECT {0} FROM {1} WHERE name='{2}'".format(column_name, table_name, field_name, db, cursor, valid_database_flag,
#   number_of_var_in_sql_cmd)
# which is basically
# args[0].format(args[1], args[2], args[3])

# merging method of the command is crude at the moment which will be made better using regex


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
