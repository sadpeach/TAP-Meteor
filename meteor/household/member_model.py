from meteor import ma, db
from sqlalchemy.orm import declarative_base, relationship

class Member(db.Model):
    __tablename__ = "Member"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    householdId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    maritalStatus = db.Column(db.String(10))
    occupationType = db.Column(db.String(10))
    annualIncome = db.Column(db.Integer, default=0)
    dob =  db.Column(db.DateTime)
    spouseId = db.Column(db.Integer,nullable=True)

    def __repr__(self):
        return '<Member %s>' % self.name

class MemberSchema(ma.Schema):

    spouse = ma.Nested(lambda: MemberSchema(exclude=("spouse","spouseId")))

    class Meta:
        fields = ("id", "householdId","name","maritalStatus","maritalStatus","spouseId","occupationType","annualIncome","dob","spouse")
        model = Member

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
    