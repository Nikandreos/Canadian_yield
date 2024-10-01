import requests
import json
import pandas as pd
from datetime import date



# STAR_CANADA.py

def data_retrieve_by_range(id:list,start_date="2005-12-01", end_date=str(date.today()),
                  url = "https://www150.statcan.gc.ca/t1/wds/rest/getBulkVectorDataByRange"):

    
    """
        the function reads data from CANADA Stats for a list of vecotr_id (product_id)
        
        the default start dat is 2005-12-01
        the default end date is today
        both start_date and end_date are strings
        
    """
    # Define the payload (POST body) as a dictionary
    payload = {
        "vectorIds": id,
        "startDataPointReleaseDate": f"{start_date}T08:30",
        "endDataPointReleaseDate": f"{end_date}T19:00"
    }
    
    try:
        # Send a POST request with the payload
        response = requests.post(url, json=payload)
    
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
    
            # Now you can work with the retrieved data
            # For example, print the entire response:
            #print(json.dumps(data, indent=2))
        else:
            print(f"Error: Request failed with status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Error: {e}")
    
    date_range = pd.date_range(start=start_date, end=end_date)
    # Create a DataFrame with the date column
    df = pd.DataFrame({'date': date_range})

    for v in data:
        #print(v['object']['vectorDataPoint'])
        if v['object']['vectorDataPoint']!=[]:
            
            df_temp=pd.DataFrame(v['object']['vectorDataPoint'])
            
            df_temp=df_temp[['refPer', 'value','releaseTime']]
            df_temp['date']=pd.to_datetime(df_temp['refPer'])
            df_temp.drop(columns=['refPer'],inplace=True)
            df_temp.rename(columns={'value':f"value_{v['object']['vectorId']}", 
                                    'releaseTime':f"releaseTime_{v['object']['vectorId']}"},inplace=True)
            
            #print(df_temp)
            #print(v['object']['vectorDataPoint'][-1])
            df=pd.merge(df,df_temp,how='left', on='date')
            #print(df)
        else:
            break
    return(df)



def latest_data_points(vector_id:int , periods=10):
    """
        The function that retrieve the latest data points of a list of vectors from Statscan
        The function returns a DataFrame with the latest data points
        The default number of periods is 10
    """
    # Define the API endpoint URL
    url = "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorsAndLatestNPeriods"
    
    # Define the payload (POST body) as a list of dictionaries
    payload = [{"vectorId": vector_id, "latestN": 3}]
    
    try:
        # Send a POST request with the payload
        response = requests.post(url, json=payload)
    
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
        else:
            print(f"Error: Request failed with status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Error: {e}")
    return(pd.DataFrame(data[0]['object']['vectorDataPoint']))


def codes_explain(code='freq'):
    '''
        Explains the codes defined by STATS CAN
        The default code is 'freq' which returns the frequency codes
        The other code is 'scalar' which returns the scalar codes
    '''
    # URL of the JSON file
    url = "https://www150.statcan.gc.ca/t1/wds/rest/getCodeSets"
    
    # Fetch the JSON data
    response = requests.get(url)
    data = response.json()

    if code=='scalar':
        return(pd.DataFrame(data['object']['scalar'])[['scalarFactorCode','scalarFactorDescEn']])
    else:
        return(pd.DataFrame(data['object']['frequency'])[['frequencyCode','frequencyDescEn']])
    

def get_title(product_id:str):
    '''
        The function returns the title of the product_id from Statscan
        product_id is a string
    '''
    # URL of the JSON file
    url="https://www150.statcan.gc.ca/t1/wds/rest/getCubeMetadata"
    payload=[{"productId":product_id}]
    # Fetch the JSON data
    response = requests.post(url, json=payload)
    data = response.json()
    
    data_dict={k: data[0]['object'][k] for k in ['productId','cubeTitleEn']}
    
    return(data_dict)


def get_meta_data(vector_id:list,title_included=False, 
                  url = "https://www150.statcan.gc.ca/t1/wds/rest/getSeriesInfoFromVector"):

    '''
        The function returns the metadata of the vector_id from Statscan
        The default title_included is False
        The default url is the Statscan API endpoint
    '''
    # Define the API endpoint URL
    data_list=[]
    for i in vector_id:
        # Define the payload (POST body) as a list of dictionaries
        payload = [{"vectorId":i}]
        
        try:
            # Send a POST request with the payload
            response = requests.post(url, json=payload)
            
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()
            else:
                print(f"Error: Request failed with status code {response.status_code}")
        except requests.RequestException as e:
            print(f"Error: vector id {i} could not be retrieved. \n ERROR:{e}")
        #print(data[0]['object']['frequencyCode'])
        if data[0]['object']['responseStatusCode']==0:
            data_list.append(data[0]['object'])

    if title_included==True:
        data_list=pd.merge(pd.DataFrame(data_list),codes_explain(code='scalar'),on='scalarFactorCode')
        data_list=pd.merge(pd.DataFrame(data_list),codes_explain(code='freq'),on='frequencyCode')

        title=[]
        for i in set(data_list['productId']):
            try:
                title.append(get_title(i))
            except:
                continue
        data_list['productId']=pd.to_numeric(data_list['productId'])
        title=pd.DataFrame(title)
        title['productId']=pd.to_numeric(title['productId'])
        data_list=pd.merge(data_list,title,on='productId')
    return(pd.DataFrame(data_list))

# list all cube lists
def list_all_data():
    url='https://www150.statcan.gc.ca/t1/wds/rest/getAllCubesListLite'
    try:
        response=requests.get(url=url)
        data=response.json()
    except:
        print(f"error: {e}")
    return(pd.DataFrame(data))


if __name__ == "__main__":
    # Code to execute when the module is run as a script
    pass
