from meteor import ma, db
from meteor.household.member_model import MemberSchema
from sqlalchemy.orm import declarative_base, relationship

class Household(db.Model):
    __tablename__ = "Household"

    householdType = db.Column(db.String(20))
    householdId = db.Column(db.Integer,primary_key=True)
    
    def __repr__(self):
        return '<Household %s>' % self.householdId

class HouseholdSchema(ma.Schema):

    #nested field
    householdMembers = ma.Nested('Member', many=True)
    
    class Meta:
        fields = ("householdType","householdId",'householdMembers')
        model = Household
        include_relationships = True

household_schema = HouseholdSchema()
households_schema = HouseholdSchema(many=True)

    