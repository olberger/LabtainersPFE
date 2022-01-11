import requests
import json
import base64
import os
import subprocess


#cmd curl pour upload un ficher dans l'espace perso moodle curl -X POST -F "file_1=@Capture.png" "http://127.0.0.1/webservice/upload.php?token=81e732801243059a4d65afd819781f24"

username = input("Username ? ")
password = input("Password ? ")
payload = {'username': username, 'password': password,'service': 'upload_f'}
headers = {'content-type': 'application/json'}
req_token_submit = requests.get('http://127.0.0.1/login/token.php',headers=headers,params=payload)
json_data = json.loads(req_token_submit.text)
token_submit = json_data["token"]
#print("tokken",token_submit)
url = 'http://127.0.0.1/webservice/rest/server.php?moodlewsrestformat=json'
wsfuntion_user = 'core_user_get_users_by_field'
ws_upload = 'core_files_upload'
ws_get_courses = 'core_enrol_get_users_courses'
ws_upload_sub = 'mod_assign_save_submission'
ws_get_info = 'core_webservice_get_site_info'
ws_get_assi = 'mod_assign_get_assignments'

#Upload a file to the private area of the user and get the id of the file

cmd_for_upload_a_file='http://127.0.0.1/webservice/upload.php?token=' + token_submit 
result = subprocess.run(['curl','-X','POST','-F','file_1=@test.png',cmd_for_upload_a_file], stdout=subprocess.PIPE)
r = result.stdout.decode('utf-8')
json_r = json.loads(r)
itemid = json_r[0]['itemid']

data = {'wstoken': token_submit, 'wsfunction': ws_get_info }
data_save_sub = requests.get(url,headers=headers,params=data)
user_id = json.loads(data_save_sub.text)['userid']
#print(user_id)

data1 = {'wstoken': token_submit, 'wsfunction': ws_get_courses,'userid':user_id,}
data_save_sub1 = requests.get(url,headers=headers,params=data1)
all_courses = json.loads(data_save_sub1.text)

for i in range(len(all_courses)):
    print(i,all_courses[i]['fullname'])
id_courses_choose = int(input("Choose your course id ..."))
id_course = all_courses[id_courses_choose]['id']
#print(id_course)

data2 = {'wstoken': token_submit, 'wsfunction': ws_get_assi,'courseids[0]':id_course }
data_assi = requests.get(url,headers=headers,params=data2)
all_assi = json.loads(data_assi.text)
id_assi = all_assi['courses'][0]['assignments'][0]['id']


data3 = {'wstoken': token_submit, 'wsfunction': ws_upload_sub , 'assignmentid' : id_assi,'plugindata[files_filemanager]': itemid}
data_save_assi = requests.get(url,headers=headers,params=data3)
save_assi = json.loads(data_save_assi.text)
if(save_assi == []):
    print("Votre archive est upload sur moodle !")
else:
    print("Une erreur est survenue")