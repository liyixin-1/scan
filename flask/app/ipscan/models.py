from app import db
import nmap

class IPScan(db.Model):
  __tablename__ = 'ipscan'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  IPs = db.Column(db.String(20))

  def __init__(self, IPs):
    self.IPs = IPs

  def create(self):
    db.session.add(self)
    db.session.commit()
    return self

  def nmapscan(self):
    nm = nmap.PortScanner()
    res=nm.scan(hosts=self.IPs,arguments="-sP -T5")
    #print(res)
    return res


class IPScanResult(db.Model):
  __tablename__= 'ipscanresult'
  result_id = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False)
  ip=db.Column(db.String(20))
  mac=db.Column(db.String(20))
  state=db.Column(db.String(20))
  task_id=db.Column(db.Integer,db.ForeignKey('ipscan.id'))

  def __init__(self,ip,mac,state,task_id=None):
    self.ip=ip
    self.mac=mac
    self.state=state
    self.task_id=task_id

  def create(self):
    db.session.add(self)
    db.session.commit()
    return self
