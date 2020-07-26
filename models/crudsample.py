import sys
import traceback

from google.cloud import datastore

# クライアントの設定
client = datastore.Client()

def InsertDatastore(keyname,data):
    """ Insert DataStore"""
    try:
        key = client.key(keyname)
        entity = datastore.Entity(key)
        entity.update(data)
        client.put(entity)
        return True
    except Exception as e:
        print('Error Insert table:' + keyname )
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
        return False

def SearchDataStore(kind_name,search):
    """ Search DataStore"""
    try:
        query = client.query(kind=kind_name)
        keylist= [i for i in search.keys()]
        valuelist = [ j for j in search.values()]
        for k,v in zip(keylist,valuelist):
            query.add_filter(k, "=", v )
        result = list(query.fetch())
        return result
    except Exception as e:
        print('Error Search Data')
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
        return False

def main():
    keyname = "Tasks"
    data = {
             'status': 'Doing',
             'date': '20191231',
             'value':'SampleSSSS'
    }

    r = InsertDatastore(keyname,data)

    search = {
                   'value':'SampleValues'
    }

    kname = 'Tasks'
    r = SearchDataStore(kname,search)
    print(r)


if __name__ == '__main__':
   main()


