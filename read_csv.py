import pandas as pd


def aps_stations():
    data = pd.read_csv("dumpOutput-02.csv", header=[0])

    line_count=0

    bssid_stationMACs=data.iloc[:,0]
    first_times=data.iloc[:,1]
    last_times=data.iloc[:,2]
    channel_power=data.iloc[:,3]
    speed_packets=data.iloc[:,4]
    privacy_bssid=data.iloc[:,5]
    ESSIDs=data.iloc[:,13]

    bssids=[]
    stationMacs=[]

    isAP=True

    for bst in bssid_stationMACs:
        
        if(bst=="Station MAC"):
            isAP=False
        
        if(isAP):
            bssids+=[bst.strip()]
        elif (bst!="Station MAC"):
            stationMacs+=[bst.strip()]
    isAP=True


    first_times_ap=[]   #access points
    first_times_st=[]   #stations


    for item in first_times:
        #print(item==" First time seen")
        
        if(item==" First time seen"):
            isAP=False
        
        if(isAP):
            first_times_ap+=[item.strip()]
        elif (item!=" First time seen"):
            first_times_st+=[item.strip()]
    isAP=True

    last_times_ap=[]   #access points
    last_times_st=[]   #stations

    for item in last_times:
        
        if(item==" Last time seen"):
            isAP=False
        
        if(isAP):
            last_times_ap+=[item.strip()]
        elif (item!=" Last time seen"):
            last_times_st+=[item.strip()]
    isAP=True

    speeds_ap=[]   #access points
    packets_st=[]   #stations

    for item in speed_packets:
        
        if(item==" # packets"):
            isAP=False
        
        if(isAP):
            speeds_ap+=[item.strip()]
        elif (item!=" # packets"):
            packets_st+=[item.strip()]
    isAP=True

    auths_ap=[]   #access points
    BSSIDs_st=[]   #stations

    for item in privacy_bssid:
        
        if(item==" BSSID"):
            isAP=False
        
        if(isAP):
            auths_ap+=[item.strip()]
        elif (item!=" BSSID"):
            BSSIDs_st+=[item.strip()]
    isAP=True

    # print(auths_ap)
    # print(BSSIDs_st)

    #create accesspoints and stations as arrays of arrays containing all information of a single AP or St

    i=0
    stations=[]
    for stn in stationMacs:
        station=[]
        station=[stn,first_times_st[i],last_times_st[i],packets_st[i],BSSIDs_st[i]]
        stations+=[station]
        i+=1
    i=0
    
    aps=[]
    for ap in bssids:
        ap_arr=[]
        ap_arr=[ap,first_times_ap[i],last_times_ap[i],speeds_ap[i],auths_ap[i]]
        aps+=[ap_arr]
        i+=1
    
    return aps,stations


