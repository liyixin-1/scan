from app import db
import nmap



class PortScan(db.Model):
    __tablename__ = 'portscan'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IP = db.Column(db.String(20))
    port = db.Column(db.String(100))
    argument = db.Column(db.String(30))

    def __init__(self,IP,port,argument):
        self.IP = IP
        self.port = port
        self.argument = argument

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    def nmapscan(self):
        nm = nmap.PortScanner()
        nm.scan(hosts=self.IP,ports=self.port,arguments=self.argument+' -T5 --min-parallelism 100')
        return nm.csv()

class PortScanResult(db.Model):
  __tablename__= 'portscanresult'
  result_id = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False)
  host=db.Column(db.String(20))
  protocol=db.Column(db.String(20))
  port=db.Column(db.Integer)
  name=db.Column(db.String(20))
  state=db.Column(db.String(20))
  reason=db.Column(db.String(20))
  task_id=db.Column(db.Integer,db.ForeignKey('portscan.id'))

  def __init__(self,host,protocol,port,name,state,reason,task_id=None):
    self.host=host
    self.protocol=protocol
    self.port = port
    self.name=name
    self.state=state
    self.reason=reason
    self.task_id=task_id

  def create(self):
    db.session.add(self)
    db.session.commit()
    return self
