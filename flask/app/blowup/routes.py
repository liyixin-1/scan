from app.blowup.schema import BlowUpResultSchema
from flask import request
from app.blowup import blowup_bp
from app.blowup.schema import BlowUpSchema
from app.blowup.models import BlowUpResult
from app.utils.responses import response_with
from app.utils import responses as resp
import urllib3
import queue

@blowup_bp.route('/task',methods=['POST'])
def create_blowup():
    try:
      data = request.get_json()
      dicts=data.get('dictionary')
      url=data.get('url')
      #print(dicts,url)
      dicts=dicts.replace(' ','\n')
      f=open('dictionary.txt','w')
      f.truncate()
      f.write(dicts)
      f.close()
      blowup_schema = BlowUpSchema()
      blowup = blowup_schema.load(data)
      results = blowup_schema.dump(blowup.create())
      #print(results)

      path_queue = queue.Queue()
      f = open('dictionary.txt', "r")
      for i in f.readlines():
        path = url +'/'+ i.strip()
        path_queue.put(path)
      f.close()
      #print(path_queue.get(1),path_queue.get(2))
      while not path_queue.empty():
        try:
          domain=path_queue.get()
          http=urllib3.PoolManager()
          response=http.request("GET",domain)
          #print(response.status,domain)
          if response.status == 200:
            #print("[%d] => %s" % (response.status, domain))
            str1 = "{ \"url\":\"" + url + "\",\"subdomain\":\"" + domain +  "\",\"task_id\":" + str(blowup.id) + " }"
            blow = eval(str1)
            #print(blow)
            blowupresult_schema = BlowUpResultSchema()
            blowupresult=blowupresult_schema.load(blow)
            res1=blowupresult_schema.dump(blowupresult.create())
            #print(res1)
        except:
          pass

      fetched = BlowUpResult.query.filter_by(task_id=blowup.id).all()
      result_schema = BlowUpResultSchema(many=True,
                                           only=['url','subdomain','task_id'])
      result = result_schema.dump(fetched)
      if len(result) == 0:
          return response_with(resp.INVALID_INPUT_422)
      else:
          return response_with(resp.SUCCESS_200,value={"results": result})
    except Exception as e:
        #print(e)
        return response_with(resp.INVALID_INPUT_422)
