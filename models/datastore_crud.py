import sys
import traceback

from google.cloud import datastore

class DataStoreCRUD():
    def __init__(self,client=None):
        self.client = datastore.Client()
    def insert_datastore(self,kind_name,insert_data):
        """ Insert DataStore"""
        try:
            key = self.client.key(kind_name)
            entity = datastore.Entity(key)
            entity.update(insert_data)
            result = self.client.put(entity)
            return result
        except Exception as e:
            print('Error Insert table:' + kind_name )
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def search_datastore(self,kind_name,search):
        """ Search DataStore"""
        try:
            result = []
            query = self.client.query(kind=kind_name)
            if search:
               # Set Condition
               keylist= [i for i in search.keys()]
               valuelist = [ j for j in search.values()]
               for k,v in zip(keylist,valuelist):
                   query.add_filter(k, "=", v )
               result = list(query.fetch())
            else:
                # All Data 
                result = list(query.fetch())
            return result
        except Exception as e:
            print('Error Search Data')
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def get_datastore_id(self,searchresult):
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
    def update_datastore(self,kind_name,target_id,prop):
        """ Update Datastore  """
        try:
            key = self.client.key(kind_name,target_id)
            data = self.client.get(key)
            data.update(prop)
            result = self.client.put(data)
            return result
        except Exception as e:
            print('Error Update Kind:'+kind_name)
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def delete_datastore(self,kind_name,target_id):
        """ Delete Datastore  """
        try:
            key = self.client.key(kind_name,target_id)        
            result = self.client.delete(key)
            return result
        except Exception as e:
            print('Error Delete Kind:'+kind_name)
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def get_kainds_list(self):
        try:
            query = self.client.query(kind='__kind__')
            query.keys_only()
            kinds = [entity.key.id_or_name for entity in query.fetch()]
            return kinds
        except Exception as e:
            print('Error Get KindList')
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
