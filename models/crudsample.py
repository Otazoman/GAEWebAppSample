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
        result = client.put(entity)
        return result
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

def GetDataStoreId(searchresult):
    """ Get Datastore Record Key Id """
    try:
        result = []
        for entity in searchresult:   
            gid = entity.id
            result.append(gid)
        return result
    except Exception as e:
        print('Error Get ID')
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
        return False

def UpdateDatastore(kind,target_id,prop):
    """ Update Datastore  """
    try:
        key = client.key(kind,target_id)
        data = client.get(key)
        data.update(prop)
        result = client.put(data)
        return result
    except Exception as e:
        print('Error Update Kind:'+kind)
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
        return False

def DeleteDatastore(kind,target_id):
    """ Delete Datastore  """
    try:
        key = client.key(kind,target_id)        
        result = client.delete(key)
        return result
    except Exception as e:
        print('Error Delete Kind:'+kind)
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
        return False


def main():
    keyname = "Tasks"

    datas = []
    i = 0
    while i < 5:
          data = dict()
          data['test_key1'] = 'value' + str(i)
          data['test_key2'] = 'value' + str(i)
          data['test_key3'] = 'value' + str(i)
          datas.append(data)
          i += 1
    
    # Insert
    for rec in datas:
        InsertDatastore(keyname,rec)

    # Search
    search = {
                   'test_key1':'value2'
    }
    searchresult = SearchDataStore(keyname,search)
    gid = GetDataStoreId(searchresult)
    for s in searchresult:
        print(s)
    
    # Update
    updatekey ={
                   'test_key1':'value3'
    }
    update_value ={
                   'test_key1':'AAA1',
                   'test_key2':'BBB2',
                   'test_key3':'CCC3',
                   'test_key4':'Done'
    }
    preud = SearchDataStore(keyname,updatekey)
    uid = GetDataStoreId(preud)
    for u in uid:
        UpdateDatastore(keyname,u,update_value)

    # Delete
    for d in gid:
        rtn = DeleteDatastore(keyname,d)

    print('Done')


if __name__ == '__main__':
   main()
