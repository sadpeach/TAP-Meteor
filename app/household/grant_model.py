from household.household_model import Household, HouseholdMemberAssociation, HouseholdMemberAssociationSchema, HouseholdSchema
from household.member_model import Member, MemberSchema
from household import ma, db, app
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import text
import os

class Grant(db.Model):
    __tablename__ = "Grant_Tb"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))

    householdMaxIncome = db.Column(db.Integer,nullable=True) #
    householdMemberOccupationCriteria = db.Column(db.String(40),nullable=True) #
    householdMemberMaxAge = db.Column(db.Integer,nullable=True) 
    householdMemberMinAge = db.Column(db.Integer,nullable=True) 
    householdTypeCriteria = db.Column(db.String(20),nullable=True) #

    qualifyMemberAge = db.Column(db.Integer,nullable=True)

    def __repr__(self):
        return '<Grant %s>' % self.name

class GrantSchema(ma.Schema):

    class Meta:
        fields = ("id", "name","householdMaxIncome","householdMemberOccupationCriteria","householdMemberMaxAge","householdMemberMinAge","householdTypeCriteria")
        model = Grant

class GrantFilteredSchema(ma.Schema):
    
    household = ma.Nested(HouseholdSchema)
    member = ma.Nested(MemberSchema)
    householdMember = ma.Nested(HouseholdMemberAssociationSchema)

    class Meta:
        fields = ("id", "name","household","member","householdMember")
        model = Grant

grant_schema = GrantSchema()
grants_schema = GrantSchema(many=True)
grantFiltered_schema = GrantFilteredSchema(many=True)


        
#import sql
# with open("./household/sql/grant.sql") as file:
#         query = text(file.read())
#         db.session.execute(query)
    