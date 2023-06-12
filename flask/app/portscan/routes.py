from flask import request
from app.portscan import portscan_bp
from app.portscan.schema import PortScanSchema
from app.portscan.models import PortScanResult
from app.utils.responses import response_with
from app.portscan.schema import PortScanResultSchema
from app.utils import responses as resp

@portscan_bp.route('/task',methods=['POST'])
def create_portscan():
    try:
        data = request.get_json()
        print(type(data))
        portscan_schema = PortScanSchema()
        portscan = portscan_schema.load(data)
        result = portscan_schema.dump(portscan.create())
        lists=portscan.nmapscan().splitlines()
        for i in range(1,len(lists)):
          str1=''.join(lists[i])
          list1=str1.split(';')
          str2="{ \"host\":\""+list1[0]+"\",\"protocol\":\""+list1[3]+"\",\"port\":\""+list1[4]+"\",\"name\":\""+list1[5]+"\",\"state\":\""+list1[6]+"\",\"reason\":\""+list1[9]+"\",\"task_id\":"+str(portscan.id)+" }"
          port=eval(str2)
          portscanresult_schema = PortScanResultSchema()
          portscanresult=portscanresult_schema.load(port)
          result=portscanresult_schema.dump(portscanresult.create())

        fetched = PortScanResult.query.filter_by(task_id=portscan.id).all()
        result_schema = PortScanResultSchema(many=True,
                                             only=['host', 'protocol', 'port', 'name', 'state', 'reason', 'task_id'])
        results = result_schema.dump(fetched)
        if len(results) == 0:
          return response_with(resp.INVALID_INPUT_422)
        else:
          return response_with(resp.SUCCESS_200, value={"results": results})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)

@portscan_bp.route('/result/<int:id>',methods=['GET'])
def get_portscan_detail(id):
    fetched = PortScanResult.query.filter_by(task_id=id).all()
    result_schema = PortScanResultSchema(many=True,only=['host','protocol','port','name','state','reason','task_id'])
    results = result_schema.dump(fetched)
    if len(results) == 0:
      return response_with(resp.INVALID_INPUT_422)
    else:
      return response_with(resp.SUCCESS_200,value={"results":results})
