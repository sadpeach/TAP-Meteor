from cmath import inf
from flask import Flask, request, jsonify, Blueprint
from household import db, app
from household.household_model import Household, household_schema, households_schema, HouseholdMemberAssociation, householdMemberAssociation_schema
from household.member_model import Member, member_schema
from household.grant_model import Grant, grant_schema, grants_schema, grantFiltered_schema
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
            housingUnit = data['housingUnit'],
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
        housingUnit = request.args.get('housingUnit')
        spouseId = data.get('spouseId')
        memberSpouse = None

        #get spouse
        if spouseId:
            memberSpouse = Member.query.get_or_404(spouseId)
        app.logger.info("spouse name is:")
        app.logger.info(memberSpouse)

        #add new member
        newMember = Member(
            name = data['name'],
            maritalStatus = data['maritalStatus'],
            spouseId = data.get('spouseId'),
            occupationType = data['occupationType'],
            annualIncome = data['annualIncome'],
            dob =  data['dob'],

            #add spouse
            spouse = memberSpouse
        )

        db.session.add(newMember)
        db.session.commit()
        db.session.refresh(newMember)

        #add member to household
        houseHoldMember = HouseholdMemberAssociation(
            housingUnit = housingUnit,
            memberId =  newMember.id,

            #add member
            member = newMember
        )

        db.session.add(houseHoldMember)
        db.session.commit()
        db.session.refresh(houseHoldMember)

        #format for display
        household = Household.query.get_or_404(housingUnit)
        res =  household_schema.dump(household)

        return jsonify({
                "message" : "Successfully added new member",
                "data" : json.loads(json.dumps(res,default=str))
            }), 200

    @household_blueprint.route('/getAllHouseholds',methods=['GET'])
    def getAllHousehold():

        households = Household.query.all()
        res =  households_schema.dump(households)

        return jsonify({
                "message" : "Successfully retrieved all houseHolds",
                "data" : json.loads(json.dumps(res,default=str))
            }), 200
    
    @household_blueprint.route('/getHouseholdById',methods=['GET'])
    def getHouseholdById():

        householdId = request.args.get('householdId')
        household = Household.query.get_or_404(householdId)
        res =  household_schema.dump(household)

        return jsonify({
                "message" : "Successfully retrieved houseHolds",
                "data" : json.loads(json.dumps(res,default=str))
            }), 200

    @household_blueprint.route('/getFundEligibleHouseholds',methods=['GET'])
    def getFundEligibleHouseholds():

        #get all households
        households = Household.query.all()
        households =  households_schema.dump(households)
        result = defaultdict(dict)

        #get annual household income
        for household in households:

            householdAnnualIncome = 0
            for member in household['householdMembers']:
                householdAnnualIncome += member['annualIncome']

            household['annualHouseholdIncome'] = householdAnnualIncome
            
        for household in households:

            bsg = 0
            result[household['housingUnit']] = {}
            result[household['housingUnit']]['Student Encouragement Bonus'] = []
            result[household['housingUnit']]['Elder Bonus'] = []
            result[household['housingUnit']]['Baby Sunshine Grant'] = []
            result[household['housingUnit']]['YOLO GST Grant'] = []
            result[household['housingUnit']]['Multigeneration Scheme'] = []

            for member in household['householdMembers']:
                age  =  datetime.fromisoformat(member['dob']).year

                if household['annualHouseholdIncome'] < 2000000 and member["occupationType"] == "student" and age < 16:
                    result[household['housingUnit']]['Student Encouragement Bonus'].append(member)

                if household['annualHouseholdIncome'] < 150000 and ( age < 18 or age > 55):
                    bsg = 1

                if household['householdType'] == 'HDB' and age > 55:
                    result[household['housingUnit']]['Elder Bonus'].append(member)
                
                if age < 1:
                    result[household['housingUnit']]['Baby Sunshine Grant'].append(member)

            if household['annualHouseholdIncome'] < 100000:
                result[household['housingUnit']]['YOLO GST Grant'] += household['householdMembers']

            if bsg:
                result[household['housingUnit']]['Multigeneration Scheme'] += household['householdMembers']

        return jsonify({
                "message" : "Successfully retrieved all houseHolds",
                "data" : json.loads(json.dumps(result,default=str))
            }), 200

            # query = "SELECT `Household`.`householdType` AS `Household_householdType`, `Household`.`housingUnit` AS `Household_housingUnit`, `HouseholdMemberAssociation`.`housingUnit` AS `HouseholdMemberAssociation_housingUnit`, `HouseholdMemberAssociation`.`memberId` AS `HouseholdMemberAssociation_memberId`, `Member`.id AS `Member_id`, `Member`.name AS `Member_name`, `Member`.`maritalStatus` AS `Member_maritalStatus`, `Member`.`occupationType` AS `Member_occupationType`, `Member`.`annualIncome` AS `Member_annualIncome`, `Member`.dob AS `Member_dob`, `Member`.`spouseId` AS `Member_spouseId`, sum(`Member`.`annualIncome`) AS `HouseholdAnnualIncome` \
            #         FROM `Household` LEFT OUTER JOIN `HouseholdMemberAssociation` ON `HouseholdMemberAssociation`.`housingUnit` = `Household`.`housingUnit` LEFT OUTER JOIN `Member` ON `Member`.id = `HouseholdMemberAssociation`.`memberId` \
            #         WHERE `Household`.`householdType` IN (" + householdTypeCriteria + ") GROUP BY `Household`.`housingUnit` \
            #         HAVING sum(`Member`.`annualIncome`) < "+str(grant['householdMaxIncome'])+" ;"




                    # grantType = request.args.get('grantType')
        # res = {}

        # #if no filtering, display all 
        # grants = Grant.query.all()
        # grants = grants_schema.dump(grants)

        # #get current year
        # current_year = date.today().year

        # #get all households
        # households = Household.query.all()
        # households =  households_schema.dump(households)

        # #search eligible households based on the grant type
        # for grant in grants:
        #     household = None

        #     #filter householdType
        #     if not grant['householdMaxIncome']:
        #         grant['householdMaxIncome'] = sys.maxsize
        
        #     householdTypeCriteria = [grant['householdTypeCriteria']]
        #     if not grant['householdTypeCriteria']:
        #         householdTypeCriteria = ['HDB','Landed','Condominium']

        #     for household in households:

        #         #check for householdtype
        #         if household['householdType'] in householdTypeCriteria:
        #             if grant['name'] not in res:
        #                 res[grant["name"]] = [household]
        #             else:
        #                 res[grant["name"]].append(household)
        #         else:
        #             break

        #         #check for annual income
        #         occupationCheck = 0 if grant["householdMemberOccupationCriteria"] else 1
        #         ageCheck = 0 if grant["householdMemberMaxAge"] else 1
                    
        #         householdAnnualIncome = 0
        #         for member in household['householdMembers']:
        #             age  = datetime.strptime(member['dob'], '%d/%m/%y').year
        #             householdAnnualIncome += member["annualIncome"]
                    
        #             if householdAnnualIncome > grant['householdMaxIncome']:
        #                 break
                
        #             if grant["householdMemberOccupationCriteria"] and member['occupation'] == grant["householdMemberOccupationCriteria"]:
        #                 occupationCheck = 1
                    
        #             if grant["householdMemberMaxAge"] and age > grant["householdMemberMaxAge"]