#---------------------------------------#
#                                       #
#  This file defines a dictionary of    #
#  area codes in the United States      #
#  called areacodes                     #
#                                       #
#  Key (int):                           #
#    3 digit area code                  #
#  Value (list of strings):             #
#    [City, City, ... , State]          #
#                                       #
#  Since there can be more than one     #
#  city covered by an area code, the    #
#  strings of cities can be numerous    #
#  but the state can always be found    #
#  by taking element -1 from the value  #
#  portion of any dictionary index.     #
#                                       # 
#---------------------------------------#

# All areacodes taken from:
# http://www.areacode.org
# and based on the North American
# Numbering Plan (NANP)
areacodes = \
	{201: ['Union City', ' Jersey City', 'Bayonne', 'New Jersey'], \
	202: ['Washington', 'District Of Columbia'], \
	203: ['Meriden', ' Danbury', 'Bridgeport', 'Connecticut'], \
	204: ['Winnipeg', 'Brandon', 'Manitoba'], \
	205: ['Jasper', ' Clanton', 'Birmingham', 'Alabama'], \
	206: ['Seattle', 'Washington'], \
	207: ['Portland', 'Maine'], \
	208: ['Pocatello', ' Falls', 'Boise', 'Idaho'], \
	209: ['Modesto', ' Merced', 'Lodi', 'California'], \
	210: ['San Antonio', 'Texas'], \
	211: ['Health Services Number', 'Non-Geographic'], \
	212: ['New York City', 'New York'], \
	213: ['Los Angeles', 'California'], \
	214: ['Dallas', 'Texas'], \
	215: ['Philadelphia', 'Levittown', 'Pennsylvania'], \
	216: ['Lakewood', ' Euclid', 'Cleveland', 'Ohio'], \
	217: ['Springfield', ' Decatur', 'Champaign', 'Illinois'], \
	218: ['Moorhead', ' Ely', 'Duluth', 'Minnesota'], \
	219: ['Hammond', 'Gary', 'Indiana'], \
	224: ['Skokie', 'Evanston', 'Arlington Heights', 'Illinois'], \
	225: ['Baton Rouge', 'Louisiana'], \
	226: ['Windsor', ' London', 'Kitchener', 'Ontario'], \
	227: ['Spring', 'Maryland Silver'], \
	228: ['Gulfport', 'Biloxi', 'Mississippi'], \
	229: ['Bainbridge', ' Americus', 'Albany', 'Georgia'], \
	231: ['Grant', 'Michigan'], \
	234: ['Youngstown', ' Canton', 'Akron', 'Ohio'], \
	236: ['Vancouver', 'British Columbia'], \
	239: ['Cape Coral', 'Florida'], \
	240: ['Frederick', ' Bethesda', 'Aspen Hill', 'Maryland'], \
	242: ['Nassau', 'Freeport', 'The Bahamas'], \
	246: ['Bridgetown', 'Barbados'], \
	248: ['Rochester Hills', 'Pontiac', 'Farmington Hills', 'Michigan'], \
	249: ['Ontario', 'Sault Ste. Marie'], \
	250: ['Victoria', 'British Columbia'], \
	251: ['Mobile', 'Alabama'], \
	252: ['Rocky Mount', ' New Bern', 'Elizabeth City', 'North Carolina'], \
	253: ['Tacoma', 'Kent', 'Washington'], \
	254: ['Hamilton', 'Eastland', 'Texas'], \
	256: ['Huntsville', 'Decatur', 'Alabama'], \
	260: ['Fort Wayne', 'Indiana'], \
	262: ['Racine', 'Kenosha', 'Wisconsin'], \
	264: ["St. John's", 'Anguilla'], \
	267: ['Philadelphia', 'Levittown', 'Pennsylvania'], \
	268: ["St. John's", 'Antigua and Barbuda'], \
	269: ['Marshall', ' Battle Creek', 'Allegan', 'Michigan'], \
	270: ['Owensboro', ' Henderson', 'Bowling Green', 'Kentucky'], \
	274: ['Green Bay', 'Wisconsin'], \
	276: ['Danville', 'Virginia'], \
	278: ['Ann Arbor', 'Michigan'], \
	281: ['Missouri City', ' Houston', 'Baytown', 'Texas'], \
	283: ['Cincinnati', 'Ohio'], \
	284: ['Road Town', 'British Virgin Islands'], \
	289: ['Vaughan', ' Mississauga', 'Brampton', 'Ontario'], \
	301: ['Bowie', ' Bethesda', 'Hill', 'Maryland Aspen'], \
	302: ['Wilmington', ' Newark', 'Dover', 'Delaware'], \
	303: ['Denver', ' Boulder', 'Aurora', 'Colorado'], \
	304: ['Parkersburg', ' Huntington', 'Charleston', 'West Virginia'], \
	305: ['Beach', ' Miami', ' Miami', 'Hialeah', 'Florida'], \
	306: ['Saskatoon', 'Regina', 'Saskathcewan'], \
	307: ['Gillette', ' Cheyenne', 'Casper', 'Wyoming'], \
	308: ['Kearney', 'Nebraska'], \
	309: ['Rock Island', ' Pekin', 'Bloomington', 'Illinois'], \
	310: ['Los Angeles', 'California'], \
	311: ['Municipal Number Services', 'Non-Geographic'], \
	312: ['Chicago', 'Illinois'], \
	313: ['Detroit', 'Dearborn', 'Michigan'], \
	314: ['St. Louis', 'Florissant', 'Missouri'], \
	315: ['Utica', 'Syracuse', 'New York'], \
	316: ['Wichita', 'Kansas'], \
	317: ['Indianapolis', 'Indiana'], \
	318: ['Shreveport', ' Monroe', 'Bossier City', 'Louisiana'], \
	319: ['Iowa City', 'Cedar Rapids', 'Iowa'], \
	320: ['Little Falls', 'Alexandria', 'Minnesota'], \
	321: ['Palm Bay', 'Orlando', 'Melbourne', 'Florida'], \
	323: ['Los Angeles', 'California'], \
	325: ['San Angelo', 'Abilene', 'Texas'], \
	330: ['Youngstown', 'Canton', 'Akron', 'Ohio'], \
	331: ['Wheaton', ' Naperville', 'Aurora', 'Illinois'], \
	334: ['Montgomery', ' Dothan', 'Auburn', 'Alabama'], \
	336: ['Kernersville', 'High Point', 'Greensboro', 'North Carolina'], \
	337: ['Lake Charles', 'Lafayette', 'Louisiana'], \
	339: ['Medford', ' Malden', 'Lynn', 'Massachusetts'], \
	340: ['Charlotte Amalie', 'U.S. Virgin Islands'], \
	341: ['Oakland', 'California'], \
	343: ['Ottawa', 'Ontario'], \
	345: ['George Town', 'Cayman Islands'], \
	347: ['Queens', ' Brooklyn', 'Bronx', 'New York'], \
	351: ['Lowell', ' Lawrence', 'Haverhill', 'Massachusetts'], \
	352: ['Spring Hill', 'Gainesville', 'Florida'], \
	360: ['Vancouver', 'Bellingham', 'Washington'], \
	361: ['Victoria', 'Corpus Christi', 'Texas'], \
	364: ['Owensboro', 'Kentucky'], \
	369: ['Santa Rosa', 'California'], \
	380: ['Columbus', 'Ohio'], \
	385: ['Provo', ' Orem', 'Ogden', 'Utah'], \
	386: ['Daytona Beach', 'Florida'], \
	401: ['Providence', ' Pawtucket', 'Cranston', 'Rhode Island'], \
	402: ['Omaha', ' Lincoln', 'Columbus', 'Nebraska'], \
	403: ['Red Deer', ' Lethbridge', 'Calgary', 'Alberta'], \
	404: ['Sandy Springs', 'Atlanta', 'Georgia'], \
	405: ['Norman', ' Moore', 'MidWest City', 'Oklahoma'], \
	406: ['Helena', ' Bozeman', 'Billings', 'Montana'], \
	407: ['Kissimmee', 'Deltona', 'Altamonte Springs', 'Florida'], \
	408: ['Morgan Hill', ' Los Gatos', 'Gilroy', 'California'], \
	409: ['Galveston', 'Beaumont', 'Texas'], \
	410: ['Columbia', ' Baltimore', 'Annapolis', 'Maryland'], \
	411: ['Directory Assistance', 'Non-Geographic'], \
	412: ['Pittsburgh', 'Pennsylvania'], \
	413: ['Northampton', ' Holyoke', 'Chicopee', 'Massachusetts'], \
	414: ['West Allis', 'Milwaukee', 'Wisconsin'], \
	415: ['San Francisco', 'California'], \
	416: ['Toronto', 'Ontario'], \
	417: ['Springfield', 'Missouri'], \
	418: ['Quebec City', 'Levis', 'Quebec'], \
	419: ['Toledo', 'Ohio'], \
	423: ['Kingsport', 'Johnson City', 'Chattanooga', 'Tennessee'], \
	424: ['Compton', ' Carson', 'Beverly Hills', 'California'], \
	425: ['Renton', ' Everett', 'Bellevue', 'Washington'], \
	430: ['Tyler', 'Longview', 'Texas'], \
	432: ['Odessa', 'Midland', 'Texas'], \
	434: ['Lynchburg', 'Virginia'], \
	435: ['St. George', 'Cedar City', 'Utah'], \
	438: ['Montreal', 'Quebec'], \
	440: ['Lorain', 'Elyria', 'Cleveland', 'Ohio'], \
	441: ['Pembroke', 'Bermuda'], \
	442: ['Encinitas', 'Carlsbad', 'Apple Valley', 'California'], \
	443: ['Ellicott City', ' Dundalk', 'Baltimore', 'Maryland'], \
	445: ['Philadelphia', 'Pennsylvania'], \
	447: ['Champaign', 'Illinois'], \
	450: ['Repentigny', ' Laval', 'Brossard', 'Quebec'], \
	456: ['NANP Inbound Routing Call', 'Non-Geographic'], \
	458: ['Eugene', 'Oregon'], \
	464: ['Cicero', 'Illinois'], \
	469: ['Grand Prairie', ' Dallas', 'Carrollton', 'Texas'], \
	470: ['Atlanta', 'Georgia'], \
	473: ["St. George's", 'Grenada, Carriacou and Petite Martinique'], \
	475: ['Meriden', ' Danbury', 'Bridgeport', 'Connecticut'], \
	478: ['Macon', 'Georgia'], \
	479: ['Fort Smith', 'Fayetteville', 'Arkansas'], \
	480: ['Phoenix', ' Mesa', 'Chandler', 'Arizona'], \
	484: ['Reading', ' Bethlehem', 'Allentown', 'Pennsylvania'], \
	500: ['Personal Communication Sercives', 'Non-Geographic Personal'], \
	501: ['Little Rock', 'Arkansas'], \
	502: ['Louisville', 'Kentucky'], \
	503: ['Portland', ' Gresham', 'Beaver', 'Oregon'], \
	504: ['New Orleans', 'Metairie', 'Kenner', 'Louisiana'], \
	505: ['Santa Fe', ' Farmington', 'Albuquerque', 'New Mexico'], \
	506: ['St. John', 'Moncton', 'Fredricton', 'New Brunswick'], \
	507: ['Worthington', ' Mankato', 'Austin', 'Minnesota'], \
	508: ['Plymouth', 'Fall River', 'Cambridge', 'Massachusetts'], \
	509: ['Yakima', 'Spokane', 'Kennewick', 'Washington'], \
	510: ['Castro Valley', 'Berkeley', 'Alameda', 'California'], \
	511: ['Transportation, Traffic & Weather Info', 'Non-Geographic'], \
	512: ['Austin', 'Texas'], \
	513: ['Hamilton', 'Cincinnati', 'Ohio'], \
	514: ['Montreal', 'Quebec'], \
	515: ['Ames City', 'Iowa'], \
	516: ['Glen Cove', 'Garden City', 'Freeport', 'New York'], \
	517: ['Coldwater', 'Clinton', 'Charlotte', 'Michigan'], \
	518: ['Schenectady', 'Albany', 'New York'], \
	519: ['Windsor', 'London', 'Kitchener', 'Ontario'], \
	520: ['Tucson', 'Foothills', 'Catalina', 'Casas Adobes', 'Arizona'], \
	530: ['Placerville', 'Davis', 'Chico', 'California'], \
	531: ['Omaha', 'Nebraska'], \
	533: ['Personal Communication Services', 'Non-Geographic'], \
	534: ['Eau Claire', 'Wisconsin'], \
	540: ['Blacksburg', 'Harrisonburg', 'Fredericksburg', 'Virginia'], \
	541: ['Pendleton', 'Eugene', 'Bend', 'Oregon'], \
	551: ['Union City', 'Jersey City', 'Bayonne', 'New Jersey'], \
	555: ['Directory Assistance', 'Non-Geographic'], \
	557: ['St. Louis', 'Missouri'], \
	559: ['Visalia', ' Fresno', 'Clovis', 'California'], \
	561: ['Delray Beach', 'Boynton Beach', 'Boca Raton', 'Florida'], \
	562: ['Downey', ' Cerritos', 'Bellflower', 'California'], \
	563: ['Dubuque', 'Davenport', 'Iowa'], \
	564: ['Seattle', 'Washington'], \
	567: ['Toledo', 'Ohio'], \
	570: ['Scranton', 'Pennsylvania'], \
	571: ['Arlington', 'Annandale', 'Alexandria', 'Virginia'], \
	573: ['Columbia', 'Missouri'], \
	574: ['South Bend', 'Elkhart', 'Indiana'], \
	575: ['Roswell', 'Las Cruces', 'Alamogordo', 'New Mexico'], \
	579: ['Terrebone', 'Quebec'], \
	580: ['Lawton', 'Oklahoma'], \
	581: ['Quebec City', 'Levis', 'Quebec'], \
	585: ['Rochester', 'Arcade', 'New York'], \
	586: ['Warren', 'Sterling Heights', 'Michigan'], \
	587: ['Edmonton', 'Calgary', 'Alberta'], \
	600: ['Specialized Telecom Services', 'Non-Geographic'], \
	601: ['Meridian', ' Jackson', 'Hattiesburg', 'Mississippi'], \
	602: ['Phoenix', 'Arizona'], \
	603: ['Merrimack', 'Manchester', 'Dover', 'New Hampshire'], \
	604: ['Richmond', 'Coquitlam', 'Burnaby', 'British Columbia'], \
	605: ['Sioux Falls', 'Rapid City', 'South Dakota'], \
	606: ['Ashland', 'Kentucky'], \
	607: ['Oneonta', 'Norwich', 'Elmira', 'New York'], \
	608: ['Madison', 'La Crosse', 'Janesville', 'Wisconsin'], \
	609: ['Plainsboro', 'Atlantic City', 'Allentown', 'New Jersey'], \
	610: ['Reading', 'Bethlehem', 'Allentown', 'Pennsylvania'], \
	611: ['Special Applications', 'Non-Geographic'], \
	612: ['Minneapolis', 'Minnesota'], \
	613: ['Ottawa', 'Kingston', 'Ontario'], \
	614: ['Westerville', 'Columbus', 'Ohio'], \
	615: ['Nashville', 'Murfreesboro', 'Tennessee'], \
	616: ['Wyoming', 'Grand Rapids', 'Michigan'], \
	617: ['Newton', 'Cambridge', 'Boston', 'Massachusetts'], \
	618: ['Alton', 'Illinois'], \
	619: ['San Diego', 'Chula Vista', 'California'], \
	620: ['Dodge City', 'Kansas'], \
	623: ['Phoenix', 'Arizona'], \
	626: ['El Monte', ' Baldwin Park', 'Alhambra', 'California'], \
	627: ['Santa Rosa', 'California'], \
	628: ['San Francisco', 'California'], \
	630: ['Roselle', 'Oswego', 'Naperville', 'Illinois'], \
	631: ['Brookhaven', 'Brentwood', 'Babylon', 'New York'], \
	636: ['St. Peters', 'St. Charles', 'Missouri'], \
	641: ['Mason City', 'Iowa'], \
	646: ['New York City', 'New York'], \
	647: ['Toronto', 'Ontario'], \
	649: ['Providenciales', 'Cockburn Town', 'Turks and Caicos Islands'], \
	650: ['Palo Alto', 'Mountain View', 'Daly City', 'California'], \
	651: ['St. Paul', 'Minnesota'], \
	657: ['Santa Ana', 'Fullerton', 'Anaheim', 'California'], \
	659: ['Birmingham', 'Alabama'], \
	660: ['Marshall', 'Missouri'], \
	661: ['Palmdale', 'Lost Hills', 'Earlimart', 'California'], \
	662: ['Starkville', 'Mississippi'], \
	664: ['Brades Estate', 'Montserrat'], \
	667: ['Baltimore', 'Maryland'], \
	669: ['San Jose', 'California'], \
	670: ['Saipan', 'Commonwealth of the Northern Mariana Islands'], \
	671: ['Hagatna', 'Guam'], \
	678: ['Roswell', ' Marietta', 'Atlanta', 'Georgia'], \
	679: ['Detroit', 'Michigan'], \
	681: ['Huntington', 'Charleston', 'West Virginia'], \
	682: ['North Richland Hills', ' Fort Worth', 'Arlington', 'Texas'], \
	684: ['Tafuna', 'Pago Pago', 'American Samoa'], \
	689: ['Orlando', 'Florida'], \
	700: ['Interexchange Carriers', 'Non-Geographic'], \
	701: ['Stanley', 'Fargo', 'Bismarck', 'North Carolina'], \
	702: ['North Las Vegas', 'Las Vegas', 'Henderson', 'Nevada'], \
	703: ['Arlington', 'Annandale', 'Alexandria', 'Virginia'], \
	704: ['Gastonia', 'Concord', 'Charlotte', 'North Carolina'], \
	705: ['Sault Ste. Marie', 'Ontario'], \
	706: ['Dahlonega', 'Augusta', 'Athens', 'Georgia'], \
	707: ['Fairfield', 'Clearlake Oaks', 'Benicia', 'California'], \
	708: ['Oak Lawn', 'Cicero', 'Berwyn', 'Illinois'], \
	709: ["St. John's", 'New Foundland & Labrador'], \
	710: ['U.S. Federal Government Official Use', 'Non-Geographic'], \
	711: ['Telecommunications Service Relay', 'Non-Geographic'], \
	712: ['Sioux City', 'Council Bluffs', 'Iowa'], \
	713: ['Pasadena', 'Houston', 'Texas'], \
	714: ['Fullerton', 'Buena Park', 'Anaheim', 'California'], \
	715: ['Eau Claire', 'Chippewa Falls', 'Wisconsin'], \
	716: ['Niagara Falls', 'Chautauqua', 'Cattaraugus', 'New York'], \
	717: ['Lancaster', 'Pennsylvania'], \
	718: ['Brooklyn', 'Bronx', 'Bellerose', 'New York'], \
	719: ['Monte Vista', 'Leadville', 'Alamosa', 'Colorado'], \
	720: ['Lakewood', ' Denver', 'Boulder', 'Colorado'], \
	721: ['Philipsburg', 'Marigot', 'Sint Maarteen'], \
	724: ['New Castle', 'Pennsylvania'], \
	727: ['Palm Harbor', 'Largo', 'Clearwater', 'Florida'], \
	730: ['Alton', 'Illinois'], \
	731: ['Jackson', 'Tennessee'], \
	732: ['Toms River', 'Edison', 'Township', 'New Jersey Brick'], \
	734: ['Livonia', ' Canton', 'Arbor', 'Michigan Ann'], \
	737: ['Austin', 'Texas'], \
	740: ['Lancaster', 'Athens', 'Ohio'], \
	747: ['Glendale', 'Burbank', 'California'], \
	752: ['Anaheim', 'California'], \
	754: ['Hollywood', 'Fort Lauderdale', 'Coral Springs', 'Florida'], \
	757: ['Newport News', 'Hampton', 'Chesapeake', 'Virginia'], \
	758: ['Gros Islet', 'Castries', 'Saint Lucia'], \
	760: ['Encinitas', 'Carlsbad', 'Apple Valley', 'California'], \
	762: ['Columbus', 'Augusta', 'Athens', 'Georgia'], \
	763: ['Plymouth', 'Maple Grove', 'Brooklyn Park', 'Minnesota'], \
	764: ['Daly City', 'California'], \
	765: ['Marion', 'Lafayette', 'Kokomo', 'Indiana'], \
	767: ['Roseau', 'Commonwealth of Dominica'], \
	769: ['Natchez', 'Jackson', 'Hattiesburg', 'Mississippi'], \
	770: ['Roswell', 'Marietta', 'Atlanta', 'Georgia'], \
	772: ['Port St. Lucie', 'Florida'], \
	773: ['Chicago', 'Illinois'], \
	774: ['Plymouth', ' Framingham', 'Brockton', 'Massachusetts'], \
	775: ['Sparks', ' Reno', 'Carson City', 'Nevada'], \
	778: ['Vancouver', ' Surrey', 'Burnaby', 'British Columbia'], \
	779: ['Rockford', 'Joliet', 'Illinois'], \
	780: ['St. Albert', 'Edmonton', 'Alberta'], \
	781: ['Medford', ' Malden', 'Lynn', 'Massachusetts'], \
	784: ['Kingstown', 'Saint Vincent and the Grenadines'], \
	785: ['Topeka', ' Lawrence', 'Abilene', 'Kansas'], \
	786: ['Miami Beach', 'Miami', 'Hialeah', 'Florida'], \
	787: ['San Juan', 'Puerto Rico'], \
	800: ['Toll Free Service', 'Non-Geographic'], \
	801: ['Salt Lake City', ' Provo', 'Ogden', 'Utah'], \
	802: ['Essex', ' Brattleboro', 'Bennington', 'Vermont'], \
	803: ['Rock Hill', 'Columbia', 'South Carolina'], \
	804: ['Tuckahoe', ' Richmond', 'Mechanicsville', 'Virginia'], \
	805: ['Santa Barbara', 'Oxnard', 'Camarillo', 'California'], \
	806: ['Lubbock', 'Amarillo', 'Texas'], \
	807: ['Thunber Bay', 'Ontario'], \
	808: ['Honolulu', 'Hawaii'], \
	809: ['Santo Domingo', 'Dominican Republic'], \
	810: ['Flint', 'Michigan'], \
	811: ['Special Applications', 'Non-Geographic'], \
	812: ['Terre Haute', ' Evansville', 'Bloomington', 'Indiana'], \
	813: ['Tampa', 'Florida'], \
	814: ['Erie', 'Pennsylvania'], \
	815: ['Rockford', 'Joliet', 'Illinois'], \
	816: ['St. Joseph', 'Lees Summit', 'Kansas City', 'Missouri'], \
	817: ['North Richland Hills', ' Fort Worth', 'Arlington', 'Texas'], \
	818: ['Calabasas', 'Burbank', 'Agoura Hills', 'California'], \
	819: ['Shawinigan', ' Gatineau', 'Drummondville', 'Quebec'], \
	822: ['Toll Free Service', 'Non-Geographic'], \
	828: ['Asheville', 'North Carolina'], \
	829: ['Santo Domingo', 'Dominican Republic'], \
	830: ['Medina', 'Texas'], \
	831: ['Santa Cruz', 'Salinas', 'California'], \
	832: ['Missouri City', 'Houston', 'Baytown', 'Texas'], \
	833: ['Toll Free Service', 'Non-Geographic'], \
	835: ['Bethlehem', 'Pennsylvania'], \
	843: ['North Charleston', ' Myrtle Beach', 'Charleston', 'South Carolina'], \
	844: ['Toll Free Service', 'Non-Geographic'], \
	845: ['Kingston', 'New York'], \
	847: ['Elgin', 'Des Plaines', 'Arlington Heights', 'Illinois'], \
	848: ['Toms River', 'Edison', 'Brick Township', 'New Jersey'], \
	849: ['Santo Domingo', 'Dominican Republic'], \
	850: ['Tallahassee', 'Pensacola', 'Florida'], \
	855: ['Toll Free Service', 'Non-Geographic'], \
	856: ['Vineland', 'Camden', 'New Jersey'], \
	857: ['Cambridge', ' Brookline', 'Boston', 'Massachusetts'], \
	858: ['San Diego', 'California'], \
	859: ['Lexington', 'Kentucky'], \
	860: ['Manchester', ' Hartford', 'Bristol', 'Connecticut'], \
	862: ['Irvington', ' East Orange', 'Clifton', 'New Jersey'], \
	863: ['Lakeland', 'Florida'], \
	864: ['Greenville', 'South Carolina'], \
	865: ['Knoxville', 'Tennessee'], \
	866: ['Toll Free Service', 'Non-Geographic'], \
	867: ['Yellowknife', 'White Horse', 'Northwest Territories'], \
	868: ['San Fernando', 'Port of Spain', 'Chaguanas', 'Trinidad and Tobago'], \
	869: ['Charlestown', 'Basseterre', 'Saint Kitts and Nevis'], \
	870: ['West Memphis', 'Jonesboro', 'Arkansas'], \
	872: ['Chicago', 'Illinois'], \
	876: ['Kingston', 'Jamaica'], \
	877: ['Toll Free Service', 'Non-Geographic'], \
	878: ['Pittsburgh', 'Pennsylvania'], \
	880: ['Toll Free Service', 'Non-Geographic'], \
	881: ['Toll Free Service', 'Non-Geographic'], \
	882: ['Toll Free Service', 'Non-Geographic'], \
	888: ['Toll Free Service', 'Non-Geographic'], \
	898: ['General Purpose Code', 'Non-Geographic'], \
	900: ['Premium Telephone Numbers', 'Non-Geographic'], \
	901: ['Memphis', 'Tennessee'], \
	902: ['Sydney', 'Halifax', 'Nova Scotia'], \
	903: ['Tyler', 'Longview', 'Texas'], \
	904: ['Jacksonville', 'Florida'], \
	905: ['Vaughan', ' Mississauga', 'Brampton', 'Ontario'], \
	906: ['Michigan', 'Sault Ste Marie'], \
	907: ['Anchorage', 'Alaska'], \
	908: ['Juneau', ' Fairbanks', 'Elizabeth', 'Alaska'], \
	909: ['Diamond Bar', ' Chino', 'Anaheim', 'California'], \
	910: ['Wilmington', 'Jacksonville', 'Fayetteville', 'North Carolina'], \
	911: ['Emergency Services', 'Non-Geographic'], \
	912: ['Savannah', 'Georgia'], \
	913: ['Olathe', 'Kansas City', 'Kansas'], \
	914: ['White Plains', 'New Rochelle', 'Mount Vernon', 'New York'], \
	915: ['El Paso', 'Texas'], \
	916: ['Roseville', 'Cordova', ' Rancho', 'Elk Grove', 'California'], \
	917: ['New York City', 'New York'], \
	918: ['Tulsa', 'Tahlequah', 'Broken Arrow', 'Oklahoma'], \
	919: ['Raleigh', 'Durham', 'Cary', 'North Carolina'], \
	920: ['Oshkosh', 'Green Bay', 'Appleton', 'Wisconsin'], \
	925: ['Livermore', 'Concord', 'Antioch', 'California'], \
	927: ['Orlando', 'Florida'], \
	928: ['Yuma', ' Prescott', 'Flagstaff', 'Arizona'], \
	931: ['Clarksville', 'Tennessee'], \
	935: ['San Diego', 'California'], \
	936: ['Nacogdoches', 'Huntsville', 'Texas'], \
	937: ['Springfield', ' Kettering', 'Dayton', 'Ohio'], \
	938: ['Huntsville', 'Alabama'], \
	939: ['San Juan', 'Puerto Rico'], \
	940: ['Denton', 'Texas'], \
	941: ['Sarasota', 'Florida'], \
	947: ['Troy', 'Southfield', 'Farmington Hills', 'Michigan'], \
	949: ['Newport Beach', 'Irvine', 'Costa Mesa', 'California'], \
	951: ['Riverside', 'Hemet', 'Corona', 'California'], \
	952: ['Minnetonka', 'Burnsville', 'Bloomington', 'Minnesota'], \
	954: ['Hollywood', 'Fort Lauderdale', 'Florida'], \
	956: ['Laredo', 'Texas'], \
	957: ['Albuquerque', 'New Mexico'], \
	959: ['Hartford', 'Connecticut'], \
	970: ['Grand Junction', 'Durango', 'Colorado'], \
	971: ['Portland', 'Gresham', 'Beaverton', 'Oregon'], \
	972: ['Garland', ' Dallas', 'Carrollton', 'Texas'], \
	973: ['Passaic', ' Orange', 'Newark', 'New Jersey'], \
	975: ['Kansas City', 'Missouri'], \
	976: ['General Purpose Code', 'Non-Geographic'], \
	978: ['Lowell', 'Lawrence', 'Haverhill', 'Massachusetts'], \
	979: ['College Station', 'Bryan', 'Texas'], \
	980: ['Gastonia', 'Concord', 'Charlotte', 'North Carolina'], \
	984: ['Raleigh', 'North Carolina'], \
	985: ['Hammond', 'Louisiana'], \
	989: ['Saginaw', 'Alpena', 'Alma', 'Michigan'], \
	999: ['General Purpose Code', 'Non-Geographic']}
