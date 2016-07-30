import json
"""
JSON data Structure for sql_server.json
{ "login_db":   this is database identifier and below are the credentials stored for that
{"id": "login",
"database": "database_name",
"table": "table_name"
},
"india_db":
{"id":"",
"database": "",
"table": ""}
"server":
{"host": "host_address",
"user": "username",
"password": "pwd"
}
"""


# pass filename of the json file as the first argument and what do you need as the next arguments
def parse_json(filename, *args):
    with open(filename, 'r') as fobj:
        data = json.load(fobj)
    arg_len = len(args)
    # print 'arg_len:{0}'.format(arg_len)
    # var is the list that will be returned
    var = []
    if len(args) > 0:
        for i in range(0, arg_len-1):
            var.append(data[args[-1]][args[i]])
        if len(var) > 1:
            return var
        else:
            return var[0]
    else:
        return data
