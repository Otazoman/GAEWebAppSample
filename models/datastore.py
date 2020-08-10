import json
import os
import re
import sys
import traceback

from datastore_crud import DataStoreCRUD

class DataStoreOperate:
    """ Table Storage Operate Class """
    def __init__(self):
        self.kindname = self
    def insert_data(self,file,kindname):
        """ Create Table and Upsert Table"""
        try:
            dc = DataStoreCRUD()
            #ファイル読込
            with open(file, "r") as test_data:
                 for l in test_data:
                     if re.search('{*}',l):
                        s = l.strip().rstrip(",")
                        insert = json.loads(s)
                        dc.insert_datastore(kindname,insert)
            return True
        except Exception as e:
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def select_records(self,condition,kindname):
        """ Set Condition and Select"""
        try:
            dc = DataStoreCRUD()
            sr = dc.search_datastore(kindname,condition)
            return sr
        except Exception as e:
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def delete_records(self,condition,kindname):
        """ Set Condition and Delete"""
        try:
            dc = DataStoreCRUD()
            sr = dc.search_datastore(kindname,condition)
            ids = dc.get_datastore_id(sr)
            for i in ids:
                dc.delete_datastore(kindname,i)
            return True
        except Exception as e:
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def get_kinds_list(self):
        """ All kinds list """
        try:
            dc = DataStoreCRUD()
            tl = dc.get_kainds_list()
            return tl
        except Exception as e:
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def get_default_table(self,listtables):
        """ Avail Record Table """
        try:
            conditions=""
            dc = DataStoreCRUD()
            for lt in listtables:
                tc0 = ro.getvalue_table(account=self.account,tablename=lt,conditions=conditions)
                for r in tc0:
                    if r:
                       return lt
        except Exception as e:
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
