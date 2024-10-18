import management
import json
import marshal

def use_dict_as_arg():
    read_args = management.readJson("main/resources/opt_arguments.json")
    # print(marshal.loads(read_args['sma_p_short']))

use_dict_as_arg()
print(marshal.dumps("range(2,3,1)"))
