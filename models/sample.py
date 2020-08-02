import sys
import traceback
from datastore_crud  import DataStoreCRUD

def main():
    try:
        ds_crud =  DataStoreCRUD()

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
            ds_crud.insert_datastore(keyname,rec)

        # Search
        search = {
                    'test_key1':'value2'
        }
        searchresult = ds_crud.search_datastore(keyname,search)
        gid = ds_crud.get_datastore_id(searchresult)
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
        preud = ds_crud.search_datastore(keyname,updatekey)
        uid = ds_crud.get_datastore_id(preud)
        for u in uid:
            ds_crud.update_datastore(keyname,u,update_value)
        
        # All
        #search = ''
        #searchresult = ds_crud.search_datastore(keyname,search)
        #for s in searchresult:
        #    print(s)

        # Delete
        for d in gid:
            rtn = ds_crud.delete_datastore(keyname,d)

        print('Done')

        lt = ds_crud.get_kainds_list()
        print(lt)

    except Exception as e:
        print('Error')
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))


if __name__ == '__main__':
   main()
