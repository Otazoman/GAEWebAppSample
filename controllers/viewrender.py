from datetime import datetime as dt
import sys
import traceback

class HtmlRender():
    """
    検索条件とテーブルを描画して返す
    """
    def __init__(self,data=None):
        self.data = data
    def get_keys(self,data):
        """ Make Titele"""
        try:
            keys = []
            for i,rs in enumerate(data):
                if type(rs) is str:
                   rs = dict(data)                 
                if i == 0:
                    keys = [ j for j in rs.keys()]
                else:
                    break
            return keys
        except Exception as e:
            print('Error get_keys')
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def conditionrender(self,data,mode):
        """ Make Html Tag """
        try:
            conditions = self.get_keys(data)
            body = '<p>SearchKey:<select name = "'+ mode + '_key_name">'
            conditions.sort()
            for c in conditions:
                body +='<option value="'  + str(c) +'">'   + str(c) + '</option>'
            body += '</select></p>'
            body +='<p>Value: <input type="text" name="'+ mode + '_value" size="10"></input></p>' 
            return body
        except Exception as e:
            print('Error Render')
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def tablerender(self,data):
        """ Body Table Render"""
        try:
            t = self.get_keys(data)
            t.sort()
            ohtml = self.make_table_html(t,data)
            return ohtml
        except Exception as e:
            print('Error TableRendermain' )
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def make_table_html(self,titles,data):
        """ Make Html Tag """
        try:
            body = """
            <div id = content>
            <style type="text/css">
                    th, td {
                            width: 100px ;
                    }
                    thead, tbody {
                    display: block;
                    }
                    tbody {
                    overflow-x: hidden;
                    overflow-y: scroll;
                    height: 600px;
                    }
            </style>
            <table border=1>
                    <thead>
                        <tr>
            """
            flg = 0
            for t in titles:
                if t != 'etag':
                    body += '<th>' + t + '</th>'
            body += '</tr></thead>'
            body += '<tbody>'
            for r in data:
                if type(r) is str:
                   r = dict(data)
                   flg = 1
                body += '<tr>'
                for k in titles:
                    if k != 'etag':
                        if type(r[k]) is str:
                            body += '<td>' + r[k] + '</td>'
                        elif isinstance(r[k],dt):
                            v = r[k].strftime('%Y-%m-%d %H:%M:%S')
                            body += '<td>' + v + '</td>'
                        else:
                            body += '<td>－</td>'
                body += '</tr>'
                if flg == 1 :
                   break
            body += """
                    </tbody>
                </table>
                </div>
                """   
            return body
        except Exception as e:
            print('Error Render')
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def make_selectbox(self,data,name):
        """ Make SelectBox Html Tag"""
        try:
            body = '<select name = "table_name">'
            for sb in data:
                if name == sb:
                   body += '<option value="' + sb + '" selected >' + sb +'</option>'
                else:
                   body += '<option value="' + sb + '">' + sb +'</option>'
            body += '</select>'
            return body
        except Exception as e:
            print('Error gmake_selectbox')
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False