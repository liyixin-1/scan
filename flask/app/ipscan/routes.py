from flask import request
import json
from app.ipscan import ipscan_bp
from app.ipscan.schema import IPScanSchema
from app.ipscan.models import IPScanResult
from app.utils.responses import response_with
from app.ipscan.schema import IPScanResultSchema
from app.utils import responses as resp


@ipscan_bp.route('/task',methods=['POST'])
def create_ipscan():
    try:
        data = request.get_json()
        #print(data)
        ipscan_schema = IPScanSchema()
        ipscan = ipscan_schema.load(data)
        result = ipscan_schema.dump(ipscan.create())
        #print(result)
        res=ipscan.nmapscan()
        #print(res['scan'])
        for i in res['scan']:
          ShowIP=""
          ShowMAC = ""
          ShowState = ""
          if res['scan'][i]['addresses']['ipv4']:
            ShowIP=res['scan'][i]['addresses']['ipv4']
          if 'mac' in res['scan'][i]['addresses']:
            ShowMAC = res['scan'][i]['addresses']['mac']
          if res['scan'][i]['status']['state']:
            ShowState = res['scan'][i]['status']['state']
          str1="{ \"ip\":\""+ShowIP+"\",\"mac\":\""+ShowMAC+"\",\"state\":\""+ShowState+"\",\"task_id\":"+str(ipscan.id)+" }"
          ip=eval(str1)
          ipscanresult_schema = IPScanResultSchema()
          ipscanresult=ipscanresult_schema.load(ip)
          result1=ipscanresult_schema.dump(ipscanresult.create())
        fetched = IPScanResult.query.filter_by(task_id=ipscan.id).all()
        result_schema = IPScanResultSchema(many=True,
                                             only=['ip','mac','state'])
        results = result_schema.dump(fetched)
        print(results,type(results))
        if len(results) == 0:
          return response_with(resp.INVALID_INPUT_422)
        else:
          return response_with(resp.SUCCESS_200, value={"results": results})
    except Exception as e:
        #print(e)
        return response_with(resp.INVALID_INPUT_422)

@ipscan_bp.route('/result/<int:id>',methods=['GET'])
def get_ipscan_detail(id):
    fetched = IPScanResult.query.filter_by(task_id=id).all()
    result_schema = IPScanResultSchema(many=True,only=['ip','mac','state'])
    results = result_schema.dump(fetched)
    if len(results) == 0:
      return response_with(resp.INVALID_INPUT_422)
    else:
      return response_with(resp.SUCCESS_200,value={"results":results})

