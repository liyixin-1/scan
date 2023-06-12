from app import db

class BlowUp(db.Model):
  __tablename__ = 'blowup'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  url = db.Column(db.String(20))
  dictionary = db.Column(db.String(100))

  def __init__(self, url,dictionary):
    self.url = url
    self.dictionary=dictionary

  def create(self):
    db.session.add(self)
    db.session.commit()
    return self



class BlowUpResult(db.Model):
  __tablename__ = 'blowupresult'
  result_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  url = db.Column(db.String(20))
  subdomain = db.Column(db.String(100))
  task_id = db.Column(db.Integer, db.ForeignKey('blowup.id'))

  def __init__(self, url,subdomain,task_id=None):
    self.url = url
    self.subdomain = subdomain
    self.task_id=task_id

  def create(self):
    db.session.add(self)
    db.session.commit()
    return self
