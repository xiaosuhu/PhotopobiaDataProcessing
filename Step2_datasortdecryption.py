import csv,json
from nis import match
from EncryptDecryptXor import DecryptXor
import pandas as pd
import numpy as np


def write_csv(data):
    with open('/Users/frankhu/Moxytech/PhotophobiaData/data_decrypt.csv', 'a') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)

def createdf():
    regions = ['left_cranium','right_cranium','left_eye','right_eye','left_midface','right_midface','left_perioral','right_perioral','left_mouth','right_mouth',\
        'left_jaw','right_jaw','left_neck','right_neck','left_chest','right_chest','left_midsection','right_midsection','left_abdomen','right_abdomen','left_upper_back','right_upper_back',\
        'left_mid_back','right_mid_back','left_lower_back','right_lower_back','left_shoulder','left_upper_arm','left_elbow','left_lower_arm','left_wrist','left_hand',\
        'right_shoulder','right_upper_arm','right_elbow','right_lower_arm','right_wrist','right_hand',\
        'left_upper_leg','left_knee','left_lower_leg','left_ankle','left_foot','right_upper_leg','right_knee','right_lower_leg','right_ankle','right_foot',\
        'left_groin','right_groin','left_buttocks','right_buttocks','left_hip','right_hip']
    total_num_region=[80,80,4,4,5,5,6,6,53,53,13,13,30,30,47,47,28,28,28,28,40,40,24,24,24,24,40,45,18,54,9,51,40,45,18,54,9,51,91,52,104,26,100,91,52,104,26,100,10,10,13,13,18,18]
    total_intensity=np.zeros(len(total_num_region))
    total_coverage=np.zeros(len(total_num_region))
    coverage_percentage=np.zeros(len(total_num_region))
    average_intensity=np.zeros(len(total_num_region))
    PAINS=np.zeros(len(total_num_region))
    dermatomes=[""]*len(total_num_region)

    #nrs== pain_levels
    #time
    #guid


    data={'Regions':regions,'Total_cell':total_num_region,'Total_intensity':total_intensity,'Total_coverage':total_coverage,\
        'Coverage_percentage':coverage_percentage,'Average_intensity':average_intensity,'PAINS':PAINS,'Dermatomes':dermatomes}
    df = pd.DataFrame(data)

    return df

def unique(list1,list2):
  
    if isinstance(list1,str):
        list1 = list(list1)
  
    # traverse for all elements
    for x in list2:
        # check if exists in unique_list or not
        if x not in list1:
            list1.append(x)
    return list1

pd.options.mode.chained_assignment = None # Disable pandas warning

xorKey = [33, 86, 105, 118, 97, 76, 97, 77, 111, 120, 121, 84, 101, 99, 104, 33]
table_regions = ['left_cranium','right_cranium','left_eye','right_eye','left_midface','right_midface','left_perioral','right_perioral','left_mouth','right_mouth',\
        'left_jaw','right_jaw','left_neck','right_neck','left_chest','right_chest','left_midsection','right_midsection','left_abdomen','right_abdomen','left_upper_back','right_upper_back',\
        'left_mid_back','right_mid_back','left_lower_back','right_lower_back','left_shoulder','left_upper_arm','left_elbow','left_lower_arm','left_wrist','left_hand',\
        'right_shoulder','right_upper_arm','right_elbow','right_lower_arm','right_wrist','right_hand',\
        'left_upper_leg','left_knee','left_lower_leg','left_ankle','left_foot','right_upper_leg','right_knee','right_lower_leg','right_ankle','right_foot',\
        'left_groin','right_groin','left_buttocks','right_buttocks','left_hip','right_hip']

headrow=['guid','time','attack','nrs']
for i in range(len(table_regions)):
    headrow += ['Regions','Total_cell','Total_intenisty','Total_coverage','Coverage_percentage','Average_intensity','PAINS','Dermatomes']
write_csv(headrow)

attackcount=1
with open('/Users/frankhu/Moxytech/PhotophobiaData/PainData20221130edit.csv',newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['geopaindatafilename'][0]=='P':
            # print(row['sync_time'],row['geopaindatafilename'][0])
            jsondata=json.loads(DecryptXor(row['geopaindata'][11:len(row['geopaindata'])],xorKey))
            df = createdf()
            for i in range(len(jsondata['bodymap']['activeCells'])):
                for tr in range(len(table_regions)):
                    if jsondata['bodymap']['activeCells'][i]['region'] == table_regions[tr]:
                            # print('1')
                            df['Total_intensity'][tr] += jsondata['bodymap']['activeCells'][i]['intensity']
                            df['Total_coverage'][tr] += 1
                            df['Dermatomes'][tr] = unique(df['Dermatomes'][tr],jsondata['bodymap']['activeCells'][i]['dermatomes'])
                          
            # Calc the other parameters for this round
            df['Coverage_percentage']=df['Total_coverage']/df['Total_cell']
            df['Average_intensity']=df['Total_intensity']/df['Total_coverage']
            df['PAINS']=df['Average_intensity']*(df['Coverage_percentage'])*0.1
            #df['Dermatomes'] = unique(df['Dermatomes'])
            attackcount += 1    

            # Write the data into csv file
            csvdata=[jsondata['diagnosis'][0]['guid'],jsondata['timeCreated'],attackcount,jsondata['nrs']['value']]
            for i in range(len(df)):
                csvdata += list(df.iloc[i].values[0:8])
            write_csv(csvdata)



"""
private static int GetNumCells(gpBody.Region region)
	{	
		switch(region)
		{
			case gpBody.Region.body: { return 2026; }
						
			case gpBody.Region.headneck:				{ return 382; }
				case gpBody.Region.head:					{ return 322; }
					case gpBody.Region.cranium:				{ return 160; }
						case gpBody.Region.left_cranium:			{ return 80; }
						case gpBody.Region.right_cranium:			{ return 80; }
					case gpBody.Region.eyes:					{ return 8; }
						case gpBody.Region.left_eye:				{ return 4; }
						case gpBody.Region.right_eye:				{ return 4; }
					case gpBody.Region.midface:				{ return 10; }
						case gpBody.Region.left_midface:			{ return 5; }
						case gpBody.Region.right_midface:			{ return 5; }
					case gpBody.Region.perioral:				{ return 12; }
						case gpBody.Region.left_perioral:			{ return 6; }
						case gpBody.Region.right_perioral:			{ return 6; }
					case gpBody.Region.mouth:					{ return 106; }
						case gpBody.Region.left_mouth:				{ return 53; }
						case gpBody.Region.right_mouth:			{ return 53; }
					case gpBody.Region.jaw:					{ return 26; }
						case gpBody.Region.left_jaw:				{ return 13; }
						case gpBody.Region.right_jaw:				{ return 13; }
				case gpBody.Region.neck:						{ return 60; }
					case gpBody.Region.left_neck:					{ return 30; }
					case gpBody.Region.right_neck:					{ return 30; }
	
			case gpBody.Region.trunk:						{ return 382; }
				case gpBody.Region.chest:						{ return 94; }
					case gpBody.Region.left_chest:					{ return 47; }
					case gpBody.Region.right_chest:				{ return 47; }
				case gpBody.Region.midsection:					{ return 56; }
					case gpBody.Region.left_midsection:			{ return 28; }
					case gpBody.Region.right_midsection:			{ return 28; }
				case gpBody.Region.abdomen:					{ return 56; }
					case gpBody.Region.left_abdomen:				{ return 28; }
					case gpBody.Region.right_abdomen:				{ return 28; }
				case gpBody.Region.upper_back:					{ return 80; }
					case gpBody.Region.left_upper_back:			{ return 40; }
					case gpBody.Region.right_upper_back:			{ return 40; }
				case gpBody.Region.mid_back:					{ return 48; }
					case gpBody.Region.left_mid_back:				{ return 24; }
					case gpBody.Region.right_mid_back:				{ return 24; }
				case gpBody.Region.lower_back:					{ return 48; }
					case gpBody.Region.left_lower_back:			{ return 24; }
					case gpBody.Region.right_lower_back:			{ return 24; }

			case gpBody.Region.left_arm:						{ return 217; }
				case gpBody.Region.left_shoulder:					{ return 40; }
				case gpBody.Region.left_upper_arm:					{ return 45; }
				case gpBody.Region.left_elbow:						{ return 18; }
				case gpBody.Region.left_lower_arm:					{ return 54; }
				case gpBody.Region.left_wrist:						{ return 9; }
				case gpBody.Region.left_hand:						{ return 51; }
				
			case gpBody.Region.right_arm:						{ return 217; }
				case gpBody.Region.right_shoulder:					{ return 40; }
				case gpBody.Region.right_upper_arm:				{ return 45; }
				case gpBody.Region.right_elbow:					{ return 18; }
				case gpBody.Region.right_lower_arm:				{ return 54; }
				case gpBody.Region.right_wrist:					{ return 9; }
				case gpBody.Region.right_hand:						{ return 51; }

			case gpBody.Region.left_leg:						{ return 373; }
				case gpBody.Region.left_upper_leg:					{ return 91; }
				case gpBody.Region.left_knee:						{ return 52; }
				case gpBody.Region.left_lower_leg:					{ return 104; }
				case gpBody.Region.left_ankle:						{ return 26; }
				case gpBody.Region.left_foot:						{ return 100; }

			case gpBody.Region.right_leg:						{ return 373; }
				case gpBody.Region.right_upper_leg:				{ return 91; }
				case gpBody.Region.right_knee:						{ return 52; }
				case gpBody.Region.right_lower_leg:				{ return 104; }
				case gpBody.Region.right_ankle:					{ return 26; }
				case gpBody.Region.right_foot:						{ return 100; }

			case gpBody.Region.pelvis:						{ return 82; }
				case gpBody.Region.groin:						{ return 20; }
					case gpBody.Region.left_groin:					{ return 10; }
					case gpBody.Region.right_groin:				{ return 10; }
				case gpBody.Region.buttocks:					{ return 26; }
					case gpBody.Region.left_buttocks:				{ return 13; }
					case gpBody.Region.right_buttocks:				{ return 13; }
				case gpBody.Region.hip:						{ return 36; }
					case gpBody.Region.left_hip:					{ return 18; }
					case gpBody.Region.right_hip:					{ return 18; }
		}

		return -1; 
	}

"""