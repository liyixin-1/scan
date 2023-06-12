from flask import request
from app.attack import attack_bp
from app.attack.schema import AttackSchema
from app.attack.models import AttackResult,Attack
from app.utils.responses import response_with
from app.attack.schema import AttackResultSchema
from app.utils import responses as resp

@attack_bp.route('/task',methods=['POST'])
def create_attack():
    try:
        data = request.get_json()
        attack_schema = AttackSchema()
        attack = attack_schema.load(data)
        result = attack_schema.dump(attack.create())
        if (attack.attacktype=='syn'):
          #print('1111111111')
          res=attack.syn_attack()
          #print(res)
          if (res==attack.attacknum):
            str2 = "{ \"destination\":\""+str(attack.destination)+"\",\"attacknum\":"+str(attack.attacknum)+",\"attacktype\":\"SYN\""+",\"result\":\"success\",\"task_id\":" + str(attack.id) + " }"
          else:
            str2 = "{ \"destination\":\"" + str(attack.destination) + "\",\"attacknum\":" + str(attack.attacknum) +",\"attacktype\":\"SYN\""+ ",\"result\":\"fail\",\"task_id\":" + str(attack.id) + " }"
            #str2 = "{ \"result\":\"fail\",\"task_id\":" + str(attack.id) + " }"
          att = eval(str2)
          attackresult_schema = AttackResultSchema()
          attackresult = attackresult_schema.load(att)
          resultss = attackresult_schema.dump(attackresult.create())
          #print(resultss)
        elif (attack.attacktype=='fin'):
          res = attack.fin_attack()
          if (res == attack.attacknum):
            str2 = "{ \"destination\":\"" + str(attack.destination) + "\",\"attacknum\":" + str(
              attack.attacknum) +",\"attacktype\":\"FIN\""+ ",\"result\":\"success\",\"task_id\":" + str(attack.id) + " }"
            #print(str2)
          else:
            str2 = "{ \"destination\":\"" + str(attack.destination) + "\",\"attacknum\":" + str(
              attack.attacknum)+",\"attacktype\":\"FIN\"" + ",\"result\":\"fail\",\"task_id\":" + str(attack.id) + " }"
          att = eval(str2)
          #print(att)
          attackresult_schema = AttackResultSchema()
          attackresult = attackresult_schema.load(att)
          resultss = attackresult_schema.dump(attackresult.create())
          #print(resultss)
        elif (attack.attacktype=='icmp'):
          res = attack.icmp_attack()
          if (res == attack.attacknum):
            str2 = "{ \"destination\":\"" + str(attack.destination) + "\",\"attacknum\":" + str(
              attack.attacknum) +",\"attacktype\":\"ICMP\""+ ",\"result\":\"success\",\"task_id\":" + str(attack.id) + " }"
          else:
            str2 = "{ \"destination\":\"" + str(attack.destination) + "\",\"attacknum\":" + str(
              attack.attacknum) +",\"attacktype\":\"ICMP\""+ ",\"result\":\"fail\",\"task_id\":" + str(attack.id) + " }"
          att = eval(str2)
          attackresult_schema = AttackResultSchema()
          attackresult = attackresult_schema.load(att)
          resultss = attackresult_schema.dump(attackresult.create())
          #print(resultss)
        else:
          res = attack.mac_attack()
          if (res == attack.attacknum):
            str2 = "{ \"destination\":\"" + str(attack.destination) + "\",\"attacknum\":" + str(
              attack.attacknum)+",\"attacktype\":\"MAC\"" + ",\"result\":\"success\",\"task_id\":" + str(attack.id) + " }"
          else:
            str2 = "{ \"destination\":\"" + str(attack.destination) + "\",\"attacknum\":" + str(
              attack.attacknum) +",\"attacktype\":\"MAC\""+ ",\"result\":\"fail\",\"task_id\":" + str(attack.id) + " }"
          att = eval(str2)
          attackresult_schema = AttackResultSchema()
          attackresult = attackresult_schema.load(att)
          resultss = attackresult_schema.dump(attackresult.create())
          #print(resultss)
        if len(resultss) == 0:
          return response_with(resp.INVALID_INPUT_422)
        else:
          return response_with(resp.SUCCESS_200, value={"results": resultss})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)
@attack_bp.route('/result/<string:atype>',methods=['GET'])
def get_ipscan_detail(atype):
    fetched = AttackResult.query.filter_by(attacktype=atype).all()
    result_schema = AttackResultSchema(many=True,only=['destination','attacknum','attacktype','result'])
    results = result_schema.dump(fetched)
    #print(results)
    return response_with(resp.SUCCESS_200,value={"results":results})
