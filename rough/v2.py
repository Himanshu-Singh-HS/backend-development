import json,requests
with open("rough/ucid_dict.json", 'r') as file:
    data = json.load(file)

url="https://beta.patdelanalytics.ai/api/v1/patent/number/validate"
ucids = list(data.keys())

print(ucids,len(data))

# ucids=["CN-118999932-A", "CN-116223224-B", "CN-116223224-A", "US-20240179486-A1", "US-11937068-B2", "US-20210289309-A1", "WO-2020127329-A1", "JP-2024020307-A", "IN-202328030652-A", "ZA-202105016-B", "IN-202127026884-A", "TW-I786356-B", "TW-202027065-A", "TH-2101003563-A", "SG-11202106482-Q", "KR-2659722-B1", "KR-20210101316-A", "CA-3123982-C", "CA-3123982-A1", "KR-20240005112-A", "CN-113316943-B", "CN-113316943-A", "AU-2019409705-B2", "AU-2019409705-A1", "JP-2022515998-A5", "JP-2022515998-A", "RU-2780536-C1", "EP-3900401-A1", "ID-2021-P", "BR-112021011170-A2", "BR-112021011170-A0", "MX-2021007337-A", "CA-3199318-A1", "SG-10202400572-W", "CN-118112098-A", "CN-118859200-A", "CN-118731954-A", "CN-116743983-A", "WO-2024057314-A1", "US-20220377489-A1", "WO-2021144308-A1", "IN-202227046108-A", "JP-2023511862-A", "BR-112022013974-A2", "BR-112022013974-A0", "KR-20220156809-A", "EP-4091344-A1", "CN-115280800-A", "CN-218647148-U", "CN-116299494-A", "CN-115684360-A", "CN-114740485-A", "US-11609317-B2", "US-20210356573-A1", "US-10324174-B2", "US-20170285151-A1", "US-20150226843-A1", "US-9880272-B2", "US-20150185318-A1", "US-20150103629-A1", "US-20130016583-A1", "CN-115704879-A", "CN-118781282-A", "CN-115685215-A", "US-20190154791-A1", "CN-109471069-B", "CN-109471069-A", "CN-110779989-B", "CN-110779989-A", "CN-212111790-U", "KR-2101771-B1", "CN-209803061-U", "CN-108894779-B", "CN-108894779-A", "CN-112926179-B", "CN-112926179-A", "CN-109683133-B", "CN-109683133-A", "CN-110487892-A", "CN-109187755-B", "CN-109187755-A", "CN-106248340-B", "CN-106248340-A", "CN-106124044-B", "CN-106124044-A", "CN-105763702-B", "CN-105763702-A", "WO-2018107299-A1", "CN-110235022-B", "CN-110235022-A", "KR-2529634-B1", "KR-20190092532-A", "JP-7026328-B2", "JP-2020501678-A", "US-11255965-B2", "US-20200041644-A1", "EP-3555660-B1", "EP-3555660-A4", "EP-3555660-A1", "CA-3045749-A1", "CN-108335336-B", "CN-108335336-A", "CN-108169333-A", "CN-105548363-A", "CN-211148532-U", "CN-107917960-A", "CN-108490077-A", "JP-4955381-B2", "JP-2008157812-A", "US-20130083628-A1", "JP-2013079949-A", "CA-2790481-A1", "EP-2574956-A1", "WO-2005121771-A1", "EP-1757928-B1", "EP-1757928-A4", "EP-1757928-A1", "EP-2982972-B1", "EP-2982972-A1", "US-8020445-B2", "US-20080245150-A1", "CN-1985165-B", "CN-1985165-A", "KR-0927365-B1", "KR-20070027702-A", "CN-101477085-B", "CN-101477085-A", "JP-4564286-B2", "JP-2005351864-A", "CN-104777485-B", "CN-104777485-A", "US-7822258-B2", "US-20060071668-A1", "WO-2005093404-A3", "WO-2005093404-A2", "US-7817843-B2", "US-20050209791-A1", "US-8169621-B2", "US-20100245844-A1", "WO-2008054496-A3", "WO-2008054496-A2", "KR-20080110779-A", "CN-101460863-B", "CN-101460863-A", "JP-2009532702-A", "EP-2013641-A2", "US-7715018-B2", "US-20070236694-A1", "CN-102636435-A", "CN-118855449-B", "CN-118855449-A", "US-20240264305-A1", "US-20240118416-A1", "WO-2020023631-A1", "CN-112739997-B", "CN-112739997-A", "US-11965958-B2", "US-20210310857-A1", "JP-7403526-B2", "JP-2021532359-A", "EP-3827228-A1", "KR-20210033532-A", "WO-2020023629-A1", "JP-7493491-B2", "JP-2021532358-A", "US-11762089-B2", "US-20210293953-A1", "EP-3827230-A1", "CN-112703376-A", "KR-20210035881-A", "WO-2020023622-A1", "JP-7488250-B2", "JP-2021532356-A", "US-20210310856-A1", "EP-3827227-A1", "CN-112703375-A", "KR-20210034076-A", "WO-2020023627-A1", "JP-2024041847-A", "US-11960002-B2", "US-20210311188-A1", "JP-7417587-B2", "JP-2021532357-A", "EP-3827229-A1", "CN-112739996-A", "KR-20210035273-A", "WO-2020023633-A1", "JP-2021532355-A", "US-20210311187-A1", "EP-3827226-A1", "CN-112739995-A", "KR-20210034661-A", "CN-116664471-A", "US-20220146668-A1", "CN-109752722-B", "CN-109752722-A", "EP-3480618-B1", "EP-3480618-A3", "EP-3480618-A2", "US-20190129027-A1", "CN-116559287-A", "CN-117607899-B", "CN-117607899-A", "CN-115166430-A", "CN-117452338-A", "WO-2023237988-A1", "WO-2020049012-A1", "JP-7449278-B2", "JP-2022502113-A5", "JP-2022502113-A", "US-20210338208-A1", "EP-3847473-A1", "CN-112654887-A", "CN-111521683-A", "US-11402503-B2", "US-20200025919-A1", "WO-2016039772-A1", "EP-3191868-B1", "EP-3191868-A1", "CN-106796290-B", "CN-106796290-A", "US-10451733-B2", "US-20170299719-A1", "WO-2017183540-A1", "CN-109073603-B", "CN-109073603-A", "KR-2125751-B1", "KR-20180121649-A", "US-10663433-B2", "US-20190113480-A1", "JP-2017194281-A", "JP-5997861-B1", "WO-2019216414-A1", "JP-7352291-B2", "JP-WO2019216414-A1", "US-11317233-B2", "US-20210058731-A1", "EP-3799035-A4", "EP-3799035-A1", "CN-103037204-A", "CN-106772370-B", "CN-106772370-A", "KR-1493956-B1", "US-10605783-B2", "US-20170052150-A1", "US-20190049962-A1", "US-10317905-B2", "CN-219437404-U", "CN-116297870-A", "CN-220586734-U", "CN-219097003-U", "CN-220795451-U", "CN-114415188-A", "CN-114415188-B", "CN-118884120-A", "CN-116374230-A", "CN-116374230-B", "US-20130142009-A1", "US-9110166-B2", "GC-0005871-B", "WO-2013082480-A1", "CA-2857027-A1", "CA-2857027-C", "AU-2012345736-A1", "AU-2012345736-B2", "MX-2014006392-A", "MX-333025-B", "EP-2776823-A1", "EP-2776823-A4", "BR-112014013059-A0", "BR-112014013059-A2", "CN-219320179-U", "CN-219339745-U", "CN-118604831-B", "CN-118818236-A", "CN-118746620-A", "CN-118425321-A", "CN-118333919-B", "CN-117968971-B", "CN-118169251-A", "CN-117825527-A", "CN-117557450-A", "CN-117409028-A", "CN-117330641-A", "CN-117214301-A", "CN-116990823-A", "CN-115620742-B", "CN-115541717-A", "KR-20240033311-A", "CN-115291225-A", "CN-115128618-A", "CN-115079264-B", "CN-115061122-A", "CN-117214903-A", "CN-114966676-B", "CN-114625319-A", "US-11474080-B2", "CN-114397010-A", "CN-114077551-A", "CN-114136432-A", "CN-114062507-A", "CN-216117875-U", "US-12117523-B2", "KR-20230003772-A", "CN-113592773-B", "CN-112985583-B", "CN-113176577-A", "CN-112946081-B", "CN-112882041-B", "CN-112697269-B", "CN-112630778-B", "CN-111835362-B", "KR-2714656-B1", "CN-111722233-B", "KR-2261754-B1", "CN-111257412-A", "CN-111007565-B", "US-12105052-B2", "CN-110501423-B", "WO-2020020867-A1", "CN-110456362-B", "CN-110220591-B", "US-20210132223-A1", "CN-110057921-B", "CN-110059371-B", "CN-109490419-B", "KR-2173404-B1",
#     "CN-109374748-A", "CN-109187771-B", "CN-208110038-U", "US-D920137-S1", "CN-107817297-A", "CN-106990172-B", "CN-206480055-U", "CN-106680825-B", "CN-106404377-A", "US-10281568-B2", "CN-106197881-A", "JP-6585547-B2", "CN-105675721-A", "CN-106918646-A", "CN-105572224-B", "CN-105182316-B", "CN-105223567-B", "CN-104614728-B", "CN-102865919-B", "CN-102981156-A", "TW-201211530-A", "CN-101865789-B", "JP-5697867-B2", "KR-1082085-B1", "JP-2009168518-A", "CN-116929662-A", "CN-116929662-B", "CN-112697269-A", "CN-117028870-A", "CN-112734713-A", "CN-112734713-B", "CN-105572224-A", "CN-118333919-A", "EP-2975397-A1", "EP-2975397-B1", "US-20160018519-A1", "US-9927521-B2", "CN-213661843-U", "CN-109916612-A", "CN-114397368-A", "CN-114397368-B", "US-20200033461-A1", "US-10989798-B2", "WO-2020023075-A1", "EP-3826541-A1", "EP-3826541-A4", "JP-2021529030-A", "JP-7242714-B2", "JP-2023065678-A", "US-20210223375-A1", "US-11703579-B2", "FR-3109826-A1", "FR-3109826-B1", "WO-2021219402-A1", "CA-3181398-A1", "CN-115516336-A", "KR-20230017788-A", "EP-4143606-A1", "EP-4143606-B1", "DK-4143606-T3", "US-20230168371-A1", "JP-2023525682-A", "IN-202247068730-A", "WO-2019215115-A1", "CN-112368600-A", "CN-112368600-B", "EP-3791204-A1", "US-20210219952-A1", "US-12130359-B2", "JP-2021522912-A", "JP-2021522912-A5", "JP-7401462-B2", "FR-3097707-A1", "FR-3097707-B1", "WO-2020254325-A1", "CA-3141652-A1", "CN-114008925-A", "EP-3987663-A1", "EP-3987663-B1", "DK-3987663-T3", "JP-2022547370-A", "JP-7499277-B2", "US-20220413134-A1", "US-11808849-B2", "KR-20150051762-A", "KR-1564647-B1", "CN-107132280-A", "CN-107132280-B", "JP-2008118168-A", "JP-4740770-B2", "WO-2007046180-A1", "EP-1950997-A1", "EP-1950997-A4", "EP-1950997-B1", "CN-101238754-A", "JP-WO2007046180-A1", "JP-4909279-B2", "US-20090301200-A1", "US-8397574-B2", "CN-104646260-A", "CN-104646260-B", "JP-2012023735-A", "JP-5391241-B2", "WO-2024136501-A1", "KR-20240100288-A", "CN-118333919-B2", "CN-117147694-A", "CN-117368840-A", "CN-115792927-A", "TW-M644123-U", "CN-117346881-A", "US-20240395121-A1", "CN-114384532-A", "CN-115170428-A", "KR-20230084929-A", "CN-113093198-A", "CN-113093198-B", "CN-115524397-A", "US-20170079624-A1", "US-10039526-B2", "WO-2017048549-A1", "BR-112018005425-A0", "BR-112018005425-A2", "CN-108027879-A", "KR-20180054738-A", "EP-3350747-A1", "JP-2018534958-A", "IN-201847012633-A", "US-20180310921-A1", "CN-112946081-A", "CN-110456362-A", "CN-109164453-A", "KR-20210021158-A", "CN-108389174-A", "CN-108389174-B", "CN-111443330-A", "CN-111443330-B", "GB-201810711-D0", "WO-2020002952-A1", "CN-112513675-A", "CN-112513675-B", "EP-3814799-A1", "US-20210275141-A1", "US-11857367-B2", "JP-2021529596-A", "JP-7340868-B2", "CN-112858183-A", "CN-112858183-B", "CN-111860664-A", "CN-111860664-B", "CN-111397726-A", "US-20090234230-A1", "US-9117439-B2", "EP-2101191-A2", "EP-2101191-A3", "EP-3919934-A1", "IL-197306-A", "IL-197306-B", "CA-2658063-A1", "CA-2658063-C", "KR-20090098748-A", "JP-2009219876-A", "JP-5888833-B2", "CN-101637395-A", "CN-101637395-B", "HK-1134645-A1", "KR-20120030488-A", "KR-1529247-B1", "JP-2016019849-A", "JP-6030207-B2", "CN-105223567-A", "CN-105241544-A", "CN-105241544-B", "CN-103512960-A", "CN-103512960-B", "EP-2541243-A1", "WO-2013006046-A1", "EP-2726861-A1", "EP-2726861-B1", "US-20140140167-A1", "US-9739752-B2", "CN-101865789-A", "WO-2024242153-A1", "US-20240385316-A1", "CN-118505719-A", "CN-116684843-A", "US-20200042548-A1", "US-11294965-B2", "US-20200042549-A1", "US-11036807-B2", "US-20200042557-A1", "US-11068544-B2", "US-20200045110-A1", "US-11748418-B2", "US-20200042240-A1", "US-11080337-B2", "WO-2020026036-A1", "CN-112534423-A", "KR-20210039394-A", "EP-3830713-A1", "JP-2022511233-A", "JP-7326667-B2", "WO-2020026112-A1", "CN-112513834-A", "CN-112513834-B", "EP-3830717-A1", "EP-3830717-B1", "EP-4266194-A1", "EP-4266194-B1", "JP-2021532472-A", "JP-7419621-B2", "JP-2023171874-A", "WO-2020028583-A1", "KR-20210037684-A", "CN-112673368-A", "EP-3830714-A1", "EP-3830714-B1", "EP-4220437-A1", "JP-2021533446-A", "JP-2024038276-A", "WO-2020028594-A1", "WO-2020028594-A9", "CN-112771515-A", "EP-3830716-A1", "EP-3830716-B1", "JP-2021533447-A", "JP-2023179680-A", "WO-2020028597-A1", "CN-112639768-A", "CN-112639768-B", "EP-3830715-A1", "EP-3830715-B1", "EP-4206951-A1", "JP-2021532473-A", "JP-2021532473-A5", "JP-7351057-B2", "US-20210256062-A1", "US-11727064-B2", "US-20210342395-A1", "US-11734363-B2", "CN-117664224-A", "CN-116363038-A", "CN-116363038-B", "CN-117557859-A", "CN-116664520-A", "CN-116664520-B", "CN-118433540-A", "CN-117440112-A", "CN-116485932-A", "CN-116385417-A", "CN-112184656-A", "CN-112184656-B", "WO-2022062461-A1", "KR-20230054427-A", "GB-202304874-D0", "GB-2614197-A", "JP-2023542371-A", "JP-7531946-B2", "US-20230230238-A1", "KR-20220098659-A", "KR-2503404-B1", "US-20220381606-A1", "WO-2022250219-A1", "EP-4351166-A1", "KR-20220163311-A", "CN-115374765-A", "CN-115374765-B", "JP-2024059209-A", "JP-2024060178-A", "CN-116433950-A", "CN-112333402-A", "CN-112333402-B", "WO-2022083599-A1", "US-20220215652-A1", "CN-114374725-A", "CN-113838001-A", "CN-113838001-B", "CN-113687415-A", "CN-113687415-B", "KR-20230006309-A", "CA-3115423-A1", "US-20210343309-A1", "US-11581009-B2", "CN-114494102-A", "CN-111812205-A", "CN-111812205-B", "CN-113542668-A", "CN-112101461-A", "CN-112101461-B", "CN-111122705-A", "CN-111122705-B", "US-20180031718-A1", "US-11163082-B2", "WO-2018026705-A1", "BR-112019002090-A0", "BR-112019002090-A2", "BR-112019002090-B1", "GB-201902574-D0", "GB-2567605-A", "GB-2567605-B", "CN-109690358-A", "CN-109690358-B", "SA-519401009-B1", "NO-20190216-A1", "CN-110163897-A", "CN-110163897-B", "CN-109660749-A", "CN-109660749-B", "KR-20200009638-A", "KR-2112340-B1", "CN-108303471-A", "TW-I663397-B", "TW-201934995-A", "CN-106292656-A", "CN-106292656-B", "CN-107356678-A", "CN-107356678-B", "CN-104410939-A", "CN-104410939-B", "WO-2016058393-A1", "EP-3209028-A1", "EP-3209028-A4", "US-20170223475-A1", "US-9866983-B2", "KR-1696088-B1", "KR-1406135-B1", "CN-104181235-A", "CN-104181235-B", "CN-103033816-A", "CN-103033816-B"]
not_ucids=[
    "BR-112014013059-A0",
    "BR-112018005425-A0",
    "BR-112018005425-A2",
    "BR-112019002090-A0",
    "BR-112021011170-A0",
    "BR-112022013974-A0",
    "CN-11833-A3919",
    "CN-118855449-B",
    "CN-118999932-A",
    "EP-4266194-B1",
    "GC-0005871-B",
    "ID-2021-P",
    "IL-197306-B",
    "JP-2021522912-A5",
    "JP-2021532473-A5",
    "JP-2022502113-A5",
    "JP-2022515998-A5",
    "KR-20070027702-A",
    "KR-20080110779-A",
    "KR-20090098748-A",
    "KR-20120030488-A",
    "KR-20150051762-A",
    "KR-20180054738-A",
    "KR-20180121649-A",
    "KR-20190092532-A",
    "KR-20200009638-A",
    "KR-20210021158-A",
    "KR-20210033532-A",
    "KR-20210034076-A",
    "KR-20210034661-A",
    "KR-20210035273-A",
    "KR-20210035881-A",
    "KR-20210037684-A",
    "KR-20210039394-A",
    "KR-20210101316-A",
    "KR-20220098659-A",
    "KR-20220156809-A",
    "KR-20220163311-A",
    "KR-20230003772-A",
    "KR-20230006309-A",
    "KR-20230017788-A",
    "KR-20230054427-A",
    "KR-20230084929-A",
    "KR-20240005112-A",
    "KR-20240033311-A",
    "KR-20240100288-A",
    "MX-333025-B",
    "SG-10202400572-W",
    "SG-11202106482-Q",
    "TH-2101003563-A",
    "US-20240385316-A1",
    "US-20240395121-A1",
    "WO-2024242153-A1",
    "JP-WO2019216414-A1",
    "JP-WO2007046180-A1"
]
again_check_without_kindcode = ["BR112014013059", "BR112018005425", "BR112018005425", "BR112019002090", "BR112021011170", "BR112022013974", "CN11833", "CN118855449", "CN118999932", "EP4266194", "GC0005871", "ID2021", "IL197306", "JP2021522912", "JP2021532473", "JP2022502113", "JP2022515998", "KR1020070027702", "KR1020080110779", "KR1020090098748", "KR1020120030488", "KR1020150051762", "KR1020180054738", "KR1020180121649", "KR1020190092532", "KR1020200009638", "KR1020210021158", "KR1020210033532", "KR1020210034076", "KR1020210034661", "KR1020210035273", "KR1020210035881", "KR1020210037684", "KR1020210039394", "KR1020210101316", "KR1020220098659", "KR1020220156809", "KR1020220163311", "KR1020230003772", "KR1020230006309", "KR1020230017788", "KR1020230054427", "KR1020230084929", "KR1020240005112", "KR1020240033311", "KR1020240100288", "MX333025", "SG10202400572", "SG11202106482", "TH2101003563", "US20240385316", "US20240395121", "WO2024242153", "JPWO2019216414", "JPWO2007046180"]

# print("again_check_without_kindcodelen",len(again_check_without_kindcode))
 
third_time=[
    "BR-112018005425",
    "CN-11833",
    "CN-118999932",
    "GC-0005871",
    "ID-2021",
    "KR-20070027702",
    "KR-20080110779",
    "KR-20090098748",
    "KR-20120030488",
    "KR-20150051762",
    "KR-20180054738",
    "KR-20180121649",
    "KR-20190092532",
    "KR-20200009638",
    "KR-20210021158",
    "KR-20210033532",
    "KR-20210034076",
    "KR-20210034661",
    "KR-20210035273",
    "KR-20210035881",
    "KR-20210037684",
    "KR-20210039394",
    "KR-20210101316",
    "KR-20220098659",
    "KR-20220156809",
    "KR-20220163311",
    "KR-20230003772",
    "KR-20230006309",
    "KR-20230017788",
    "KR-20230054427",
    "KR-20230084929",
    "KR-20240005112",
    "KR-20240033311",
    "KR-20240100288",
    "MX-333025",
    "SG-10202400572",
    "SG-11202106482",
    "TH-2101003563",
    "US-20240385316",
    "US-20240395121",
    "WO-2024242153",
    "JP-WO2019216414",
    "JP-WO2007046180"
]
k_without_kindcode=['BR112014013059', 'BR112018005425', 'BR112018005425', 'BR112019002090', 'BR112021011170', 'BR112022013974', 'CN118333919', 'CN118855449', 'CN118999932', 'EP4266194', 'GC0005871', 'ID2021', 'IL197306', 'JP2021522912', 'JP2021532473', 'JP2022502113', 'JP2022515998', 'MX333025', 'SG10202400572', 'SG11202106482', 'TH2101003563', 'US20240385316', 'US20240395121', 'WO2024242153', 'JPWO2019216414', 'JPWO2007046180']
# k_without_kindcode= list(set(k_without_kindcode)) 
# print("k_without_kindcode",len(k_without_kindcode))
successful_numbers = []
does_not_exists=[]
_ucids=set()
for item in ucids:
    x,y,z = item.split("-")
    _ucids.add(f'{x}{y}')
_ucids = list(_ucids)
payload = {"numbers": _ucids}
try:
    
    response = requests.post(url, json=payload)
    response.raise_for_status()  

 
    data = response.json()
    from pprint import pprint
    # pprint(data,width=150)
    # with open("rough/output3/response_data_succesfull.json", "w") as json_file:
    #     json.dump(data, json_file, indent=4) 
    a=[]
        
    for item in data.get("numbers", []):
        if item.get("status") == "OK": 
            successful_numbers.append(item["number"])
            
        elif item.get("status") == "ERROR": 
            does_not_exists.append(item["number"])
        a.append(item["number"])
    a.sort()
    successful_numbers.sort()
    does_not_exists.sort()
    # print("succesfull",a,len(a))

except Exception as e :
    print("erroe here ",e)
    
# with open("rough/output2/total_data_success_without_code.json", "w") as json_file:
#     json.dump(successful_numbers, json_file, indent=4)

with open("rough/output3/response_data_succesfull5.json", "w") as json_file:
    json.dump( successful_numbers,json_file, indent=4) 
with open("rough/output3/response_data_not_validate5.json", "w") as json_file:
    json.dump( does_not_exists,json_file, indent=4) 
    
print(f"Validation complete. Total successful numbers saved: {len(successful_numbers)} and {len(does_not_exists)} and {len(data.get('numbers', []))}")   

