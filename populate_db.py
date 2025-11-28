from website import create_app, db
from sqlalchemy import text
from werkzeug.security import generate_password_hash

app = create_app()

insert_users=f"""
INSERT INTO user (
    id,
    employee_id,
    email,
    password,
    first_name,
    last_name,
    role,
    date_created
) VALUES
    (1001,'RBU-1001','jane.doe@RBU.com','{generate_password_hash("sillyPassword101")}','Jane','Doe','owner','2025-10-26 10:30:00'),
    (1002,'RBU-1002','marc.m@RBU.com','{generate_password_hash("totallyRe@l")}','Marc','M','admin','2025-10-27 11:45:00'),
    (1003,'RBU-1003','audible.gulp@RBU.com','{generate_password_hash("p@ssw0rd!")}','Audible','Gulp','employee','2025-10-28 09:15:00')
"""

insert_customers= """
INSERT INTO customer (
    customerNum,
    customerFirst,
    customerLast,
    address,
    balance,
    creditScore,
    bankNumR,
    bankNumA,
    SSN
) VALUES
(10001,'James','Smith','123 Oak Street',15420.5,720,123456789,'987654321098',123456789),
(10002,'Mary','Johnson','456 Maple Ave',8950.25,680,234567890,'876543210987',234567890),
(10003,'Robert','Williams','789 Pine Road',22340.8,750,345678901,'765432109876',345678901),
(10004,'Patricia','Brown','321 Elm Court',5670,625,456789012,'654321098765',456789012),
(10005,'Michael','Jones','654 Cedar Lane',31250.8,785,567890123,'543210987654',567890123),
(10006,'Linda','Garcia','987 Birch Way',12890.4,695,678901234,'432109876543',678901234),
(10007,'William','Martinez','147 Walnut St',19500.6,740,789012345,'321098765432',789012345),
(10008,'Barbara','Rodriguez','258 Ash Drive',7320.9,655,890123456,'210987654321',890123456),
(10009,'David','Wilson','369 Spruce Blvd',28750.2,770,901234567,'109876543210',901234567),
(10010,'Elizabeth','Anderson','741 Poplar Path',4580.35,610,112345678,'998765432109',112345678),
(10011,'Richard','Taylor','852 Hickory Ln',16840.7,705,223456789,'887654321098',223456789),
(10012,'Susan','Thomas','963 Willow Rd',11230.2,670,334567890,'776543210987',334567890),
(10013,'Joseph','Hernandez','159 Cherry Ave',24560.4,760,445678901,'665432109876',445678901),
(10014,'Jessica','Moore','357 Beech St',6890.8,640,556789012,'554321098765',556789012),
(10015,'Thomas','Martin','753 Sycamore Dr',33420.9,795,667890123,'443210987654',667890123),
(10016,'Sarah','Jackson','951 Magnolia Ct',9760.3,685,778901234,'332109876543',778901234),
(10017,'Charles','Thompson','135 Dogwood Way',18290.6,730,889012345,'221098765432',889012345),
(10018,'Karen','White','246 Redwood Blvd',5120.65,620,990123456,'110987654321',990123456),
(10019,'Daniel','Lopez','468 Fir Lane',27630.4,775,101234567,'999876543210',101234567),
(10020,'Nancy','Lee','579 Cypress Path',8340.2,660,212345678,'888765432109',212345678),
(10021,'Matthew','Gonzalez','680 Alder Road',14950.8,715,323456789,'777654321098',323456789),
(10022,'Lisa','Harris','791 Laurel St',21470.5,745,434567890,'666543210987',434567890),
(10023,'Mark','Clark','802 Hazel Ave',6230.75,635,545678901,'555432109876',545678901),
(10024,'Betty','Lewis','913 Juniper Dr',29890.3,780,656789012,'444321098765',656789012),
(10025,'Donald','Robinson','124 Acacia Ct',10560.9,690,767890123,'333210987654',767890123),
(10026,'Dorothy','Walker','235 Olive Way',17780.4,725,878901234,'222109876543',878901234),
(10027,'Steven','Perez','346 Aspen Blvd',4920.6,615,989012345,'111098765432',989012345),
(10028,'Sandra','Hall','457 Cottonwood',25340.2,765,100234567,'100987654321',100234567),
(10029,'Paul','Young','568 Basswood St',7650.35,650,211345678,'989876543210',211345678),
(10030,'Ashley','Allen','679 Locust Ave',32100.7,790,322456789,'878765432109',322456789),
(10031,'Kenneth','Sanchez','780 Mesquite Rd',13420.2,700,433567890,'767654321098',433567890),
(10032,'Donna','Wright','891 Pecan Lane',19870.8,735,544678901,'656543210987',544678901),
(10033,'Joshua','King','902 Chestnut Dr',5480.5,630,655789012,'545432109876',655789012),
(10034,'Kimberly','Scott','113 Sequoia Ct',28190.9,785,766890123,'434321098765',766890123),
(10035,'Brian','Green','224 Buckeye Way',9120.4,675,877901234,'323210987654',877901234),
(10036,'Michelle','Baker','335 Hemlock Blvd',16540.7,720,988012345,'212109876543',988012345),
(10037,'Edward','Adams','446 Mulberry St',22910.2,755,109345678,'101098765432',109345678),
(10038,'Amanda','Nelson','557 Palmetto Ave',6780.85,645,220456789,'990987654321',220456789),
(10039,'George','Carter','668 Boxwood Rd',30560.5,800,331567890,'889876543210',331567890),
(10040,'Carol','Mitchell','779 Yew Lane',11890.8,695,442678901,'778765432109',442678901),
(10041,'Ronald','Perez','880 Tamarack Dr',18230.3,730,553789012,'667654321098',553789012),
(10042,'Melissa','Roberts','991 Larch Ct',5340.6,625,664890123,'556543210987',664890123),
(10043,'Anthony','Turner','102 Ironwood Way',26780.9,770,775901234,'445432109876',775901234),
(10044,'Helen','Phillips','213 Tupelo Blvd',8920.45,665,886012345,'334321098765',886012345),
(10045,'Kevin','Campbell','324 Sumac St',15670.2,710,997123456,'223210987654',997123456),
(10046,'Deborah','Parker','435 Teak Ave',23450.7,750,108234567,'112109876543',108234567),
(10047,'Jason','Evans','546 Mahogany Rd',7010.35,655,219345678,'101098765432',219345678),
(10048,'Laura','Edwards','657 Bamboo Lane',31890.8,795,330456789,'990987654321',330456789),
(10049,'Gary','Collins','768 Rosewood Dr',12340.2,700,441567890,'889876543210',441567890),
(10050,'Emily','Stewart','879 Ebony Court',20150.5,740,552678901,'778765432109',552678901);
"""

with app.app_context():
    db.session.execute(text(insert_users))
    db.session.execute(text(insert_customers))
    db.session.commit()
    print("Inserted data!")