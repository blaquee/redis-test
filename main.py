import redis
import json
import datetime
import time
import random


redis_server = redis.Redis(db=1)
date_format = "%Y%m%d"


def get_prev_day_malware(malware):
    prev_date = datetime.date.today() - datetime.timedelta(1)
    prev_date = prev_date.strftime(date_format)

    key = malware+prev_date
    ret = redis_server.get(key)

    return (key,ret)


'''def get_malware(malware):

    if redis_server.exists(malware):
        return [malware, redis_server.get(malware)]
    else:
        return ()
'''


def load_config():
    fin = open("mlw.json","rb")
    data = json.load(fin)
    fin.close()
    return data

def add_malware():

    pipe = redis_server.pipeline()
    malwares = load_config()
    dict_list = {}

    for m in malwares["family"]:
        key = m + "-" + datetime.date.today().strftime(date_format)
        total = random.randint(0,2000000)
        unique = random.randint(0,50000)
        dict_list[key] = (total, unique)

    for k,v in dict_list.items():
        print "v[0]:{}{} \t v[1]:{}{}".format(v[0], type(v[0]), v[1], type(v[1]))
        pipe.rpush(k, v[0])
        pipe.rpush(k, v[1])

    pipe.execute()


def get_malware():

    #pipe = redis_server.pipeline()
    #keys = redis_server.keys('*')
    #for key in keys:
     #   print "Key types: {}".format(redis_server.type(key))

    prev_mal = []
    malwares = load_config()
    for m in malwares["family"]:
        if redis_server.exists(m):
            v = redis_server.lrange(m,0,-1)

            prev_mal.append = [m,r. v]

    print_data(prev_mal)

    return prev_mal



def print_data(data):
    print "Malware Data"
    for i in data:
        print "{}".format(i)


def sorted_list(data):

    sorted_dict = sorted(data.items(), key=lambda k: k[1][1], reverse=True)
    return sorted_dict

def main():

    add_malware()

    mal = get_malware()
    #new_mal = sorted_list(mal)
'''
    print "Sorted List"
    for i in new_mal:
        print "{}".format(i)
        for k,v in new_mal.items():
        print "{}:{}".format(k,v)
'''


if __name__ == '__main__':
    redis_server.flushall()
    main()