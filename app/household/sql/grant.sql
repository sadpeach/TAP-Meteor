USE meteor;
INSERT INTO Grant_Tb
    (name,householdMaxIncome,householdTypeCriteria,householdMemberOccupationCriteria,householdMemberMaxAge,householdMemberMinAge,qualifyMemberAge)
VALUES
    ("Student Encouragement Bonus",200000,NULL,"Student",16,NULL,16),
    ("Multigeneration Scheme",150000,NULL,NULL,18,NULL,NULL),
    ("Multigeneration Scheme",150000,NULL,NULL,NULL,55,NULL),
    ("Elder Bonus",NULL,'HDB',NULL,NULL,55,NULL),
    ("Baby Sunshine Grant",NULL,NULL,NULL,0.8,NULL,0.8),
    ("YOLO GST Grant",100000,'HDB',NULL,NULL,NULL,NULL);
