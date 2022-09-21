from cmath import inf
from flask import Flask, request, jsonify, Blueprint
from meteor import db, app
from meteor.household.household_model import Household, household_schema, households_schema
from meteor.household.member_model import Member, member_schema, members_schema
from functools import wraps
import json
from sqlalchemy import and_, or_, not_
from sqlalchemy.sql import func
from datetime import date,datetime
from collections import defaultdict

household_blueprint = Blueprint("household_blueprint",__name__)

class HouseholdRoutes():

    @household_blueprint.route('/healthCheck',methods=['GET'])
    def healthCheck():
        return jsonify({
                "status" : "Healthcheck Success",
            }), 200

    @household_blueprint.route('/createHousehold',methods=['POST'])
    def createHousehold():
        data = request.get_json()

        household = Household(
            householdType = data['householdType']
        )

        db.session.add(household)
        db.session.commit()
        db.session.refresh(household)

        res =  household_schema.dump(household)

        return jsonify({
                "message" : "Successfully created new houseHold",
                "data" : json.loads(json.dumps(res,default=str))
            }), 200

    @household_blueprint.route('/addMember',methods=['POST'])
    def addMember():
        data = request.get_json()
        householdId = request.args.get('householdId')
        spouseId = data.get('spouseId')

        #add new member
        newMember = Member(
            name = data['name'],
            maritalStatus = data['maritalStatus'],
            spouseId = data.get('spouseId'),
            occupationType = data['occupationType'],
            annualIncome = data['annualIncome'],
            dob =  data['dob'],
            householdId = householdId
        )

        db.session.add(newMember)
        db.session.commit()
        db.session.refresh(newMember)

        #update spouse
        if spouseId:
            db.session.query(Member).filter(
                and_(
                    Member.id == spouseId,
                    Member.householdId == householdId)
            ).update(
                {
                    "spouseId": newMember.id
                }
            )
            db.session.commit()

        #format for display
        household = Household.query.get_or_404(householdId)
        household =  household_schema.dump(household)

        #get all member from household
        members = db.session.query(Member).filter(Member.householdId == householdId).all()
        members = members_schema.dump(members)

        #all memberIds
        allMemberIds = []
        for member in members:
            allMemberIds.append(member['id'])

        #match spouse
        for member in members:
            
            if member['spouseId'] in allMemberIds:
                spouse = db.session.query(Member).filter(
                    and_(
                        Member.householdId == householdId,
                        Member.id == member['spouseId']
                        ) 
                ).one()
                spouse = member_schema.dump(spouse)
                member["spouse"] = spouse
        
        #match household with members
        household["householdMembers"] = members

        return jsonify({
                "message" : "Successfully added new member",
                "data" : json.loads(json.dumps(household,default=str))
            }), 200

    @household_blueprint.route('/getAllHouseholds',methods=['GET'])
    def getAllHousehold():

        households = Household.query.all()
        households =  households_schema.dump(households)

        for household in households:
            householdId = household['householdId']
            members = db.session.query(Member).filter(Member.householdId == householdId).all()
            members = members_schema.dump(members)

            #all memberIds
            allMemberIds = []
            for member in members:
                allMemberIds.append(member['id'])

            #match spouse
            for member in members:
                
                if member['spouseId'] in allMemberIds:
                    spouse = db.session.query(Member).filter(
                        and_(
                            Member.householdId == householdId,
                            Member.id == member['spouseId']
                            ) 
                    ).one()
                    spouse = member_schema.dump(spouse)
                    member["spouse"] = spouse
            
            #match household with members
            household["householdMembers"] = members


        return jsonify({
                "message" : "Successfully retrieved all houseHolds",
                "data" : json.loads(json.dumps(households,default=str))
            }), 200
    
    @household_blueprint.route('/getHouseholdById',methods=['GET'])
    def getHouseholdById():

        householdId = request.args.get('householdId')
        household = Household.query.get_or_404(householdId)
        household =  household_schema.dump(household)

        #get all member from household
        members = db.session.query(Member).filter(Member.householdId == householdId).all()
        members = members_schema.dump(members)

        #all memberIds
        allMemberIds = []
        for member in members:
            allMemberIds.append(member['id'])

        #match spouse
        for member in members:
            
            if member['spouseId'] in allMemberIds:
                spouse = db.session.query(Member).filter(
                    and_(
                        Member.householdId == householdId,
                        Member.id == member['spouseId']
                        ) 
                ).one()
                spouse = member_schema.dump(spouse)
                member["spouse"] = spouse
        
        #match household with members
        household["householdMembers"] = members


        return jsonify({
                "message" : "Successfully retrieved household by Id",
                "data" : json.loads(json.dumps(household,default=str))
            }), 200

    @household_blueprint.route('/getFundEligibleHouseholds',methods=['GET'])
    def getFundEligibleHouseholds():

        #get all households
        households = Household.query.all()
        households =  households_schema.dump(households)
        result = defaultdict(dict)

        #add member to household
        for household in households:
            householdId = household['householdId']
            household["householdMembers"] = []
            members = db.session.query(Member).filter(Member.householdId == householdId).all()
            members = members_schema.dump(members)
            household["householdMembers"] += members
        
        app.logger.info("adding member to household:",households)

        #get annual household income
        for household in households:
            householdAnnualIncome = 0
            for member in household['householdMembers']:
                householdAnnualIncome += member['annualIncome']

            household['annualHouseholdIncome'] = householdAnnualIncome
            
        for household in households:

            bsg = 0
            result[household['householdId']] = {}
            result[household['householdId']]['Student Encouragement Bonus'] = {"eligibleMembers":[]}
            result[household['householdId']]['Elder Bonus'] = {"eligibleMembers":[]}
            result[household['householdId']]['Baby Sunshine Grant'] = {"eligibleMembers":[]}
            result[household['householdId']]['YOLO GST Grant'] = {"eligibleMembers":[]}
            result[household['householdId']]['Multigeneration Scheme'] = {"eligibleMembers":[]}

            for member in household['householdMembers']:
                age  =  datetime.fromisoformat(member['dob']).year

                if household['annualHouseholdIncome'] < 2000000 and member["occupationType"] == "student" and age < 16:
                    result[household['householdId']]['Student Encouragement Bonus']["eligibleMembers"].append(member)

                if household['annualHouseholdIncome'] < 150000 and ( age < 18 or age > 55):
                    bsg = 1

                if household['householdType'] == 'HDB' and age > 55:
                    result[household['householdId']]['Elder Bonus']["eligibleMembers"].append(member)
                
                if age < 1:
                    result[household['householdId']]['Baby Sunshine Grant']["eligibleMembers"].append(member)

            if household['annualHouseholdIncome'] < 100000:
                result[household['householdId']]['YOLO GST Grant']["eligibleMembers"] += household['householdMembers']

            if bsg:
                result[household['householdId']]['Multigeneration Scheme']["eligibleMembers"] += household['householdMembers']

        return jsonify({
                "message" : "Successfully retrieved all houseHolds",
                "data" : json.loads(json.dumps(result,default=str))
            }), 200
