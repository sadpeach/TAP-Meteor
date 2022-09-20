from household import ma, db
from household.member_model import MemberSchema
from sqlalchemy.orm import declarative_base, relationship

class Household(db.Model):
    __tablename__ = "Household"

    householdType = db.Column(db.String(20))
    housingUnit = db.Column(db.String(10),primary_key=True)

    #relationship
    householdMembers = db.relationship("HouseholdMemberAssociation")
    
    def __repr__(self):
        return '<Household %s>' % self.housingUnit

class HouseholdMemberAssociation(db.Model):
    __tablename__ = "HouseholdMemberAssociation"

    housingUnit = db.Column(db.String(10), db.ForeignKey('Household.housingUnit'), primary_key=True)
    memberId = db.Column(db.Integer, db.ForeignKey('Member.id'), primary_key=True)

    # relationship
    member = relationship("Member")

    def __repr__(self):
        return '<Household Member Association %s>' % self.memberId

class HouseholdMemberAssociationSchema(ma.Schema):

    #relationship
    member = ma.Nested(MemberSchema)

    class Meta:
        fields = ("housingUnit","member")
        model = HouseholdMemberAssociation

class HouseholdSchema(ma.Schema):

    #nested field
    householdMembers = ma.Pluck('HouseholdMemberAssociationSchema', 'member', many=True)
    
    class Meta:
        fields = ("householdType","housingUnit",'householdMembers')
        model = Household
        include_relationships = True

household_schema = HouseholdSchema()
households_schema = HouseholdSchema(many=True)
householdMemberAssociation_schema = HouseholdMemberAssociationSchema()

    