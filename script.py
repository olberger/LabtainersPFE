import requests
import json

#cmd curl pour upload un ficher dans l'espace perso moodle curl -X POST -F "file_1=@Capture.png" "http://127.0.0.1/webservice/upload.php?token=81e732801243059a4d65afd819781f24"
username = 'admin'
username1= 'user'
password = '****'


payload = {'username': username, 'password': password,'service': 'assign'}
payload1 = {'username': username, 'password': password, 'service': 'viewuser'}
payload2 = {'username': username1, 'password': password, 'service': 'test'}
headers = {'content-type': 'application/json'}


req_token_submit = requests.get('http://127.0.0.1/login/token.php',headers=headers,params=payload)
req_token_get_user_id = requests.get('http://127.0.0.1/login/token.php',headers=headers,params=payload1)
req_token_get_test = requests.get('http://127.0.0.1/login/token.php',headers=headers,params=payload2)


json_data = json.loads(req_token_submit.text)
json_data1 = json.loads(req_token_get_user_id.text)
json_data2 = json.loads(req_token_get_test.text)

token_submit = json_data["token"]
token_get_user_id = json_data1["token"]
token_get_user_test = json_data2["token"]
print(token_submit, token_get_user_id,token_get_user_test)

wsfuntion = 'mod_assign_submit_grading_form'
wsfuntion_user = 'core_user_get_users_by_field'
wsfuntion_test = 'mod_assign_get_assignments'
wsfuntion_test2 = 'mod_assign_save_submission'
ws_upload = 'core_files_upload'

url = 'http://127.0.0.1/webservice/rest/server.php?moodlewsrestformat=json'

data = {'wstoken': token_get_user_id, 'wsfunction': wsfuntion_user ,'field':'id', 'values[0]': '2'}

req_get_user_id = requests.get(url,headers=headers,params=data)
json_user_data = json.loads(req_get_user_id.text)
#print(json_user_data)


    
data1 = {'wstoken': token_submit, 'wsfunction': wsfuntion ,'userid': '2', 'assignmentid': 1 ,'jsonformdata': '' }
req_submit_data = requests.post(url,headers=headers,params=data1)
json_a = json.loads(req_submit_data.text)
#print(req_submit_data.text)


data2 = {'wstoken': token_get_user_test, 'wsfunction': wsfuntion_test2 , 'assignmentid' : '1','plugindata[files_filemanager]': '248405723'}
req_submit_data = requests.post(url,headers=headers,params=data2)
json_a = json.loads(req_submit_data.text)
print(req_submit_data.text)





'''
userid = 2
assignmentid = 2
jsonformdata= json_data

field = 'id'
token2='a5f70d5ddee3f2006feadf50cf284ae2'
#data1 = {'wstoken': token, 'wsfuntion': wsfuntion ,'userid': userid, 'assignmentid': assignmentid,'jsonformdata': jsonformdata }
print(r2.text)
'''