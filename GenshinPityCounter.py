from bs4 import BeautifulSoup
import requests
import json

chkpoint_id = "0"
item_5_stars = []
pity_5_stars = []
item_4_stars = []
pity_4_stars = []
cnt_4_stars = 0
cnt_5_stars = 0
cnt = 0

'''
    variable links bisa diubah value gacha typenya:
        301 = Character Event Banner
        302 = Weapon Event Banner
        200 = Standard Banner
        100 = Beginner Banner
'''

auth_key = input("link feedback:")
auth_key = auth_key[auth_key.find("authkey=")+8:]
auth_key = auth_key[:auth_key.find("&")]
links = f'https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getGachaLog?authkey_ver=1&sign_type=2&auth_appid=webview_gacha&init_type=301&lang=en&authkey={auth_key}&gacha_type=301&page=1&size=20&end_id={chkpoint_id}'
response = requests.get(links)
while response.status_code == 200 and cnt<=20:

    soup = BeautifulSoup(response.text, 'html.parser')
    site_json = json.loads(soup.text)

    for a in (site_json['data']['list']):

        if len(item_5_stars) != 0:
            cnt_5_stars += 1

        if len(item_4_stars) != 0:
            cnt_4_stars += 1

        if a['rank_type']=='5':
            item_5_stars.append(f'{a["name"]}')
            if len(item_5_stars)>1 :
                pity_5_stars.append(str(cnt_5_stars))
            cnt_5_stars = 0

        elif a['rank_type']=='4':
            item_4_stars.append(f'{a["name"]}')
            if len(item_4_stars) > 1:
                pity_4_stars.append(str(cnt_4_stars))
            cnt_4_stars = 0

        #print(a['name'] + '\t' + a['item_type'] + '\t' + a['rank_type'] +' Stars')
        chkpoint_id = a['id']

    links = f'https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getGachaLog?authkey_ver=1&sign_type=2&auth_appid=webview_gacha&init_type=301&lang=en&authkey={auth_key}&gacha_type=301&page=1&size=20&end_id={chkpoint_id}'
    response = requests.get(links)
    cnt += 1

avr = 0
print("\n5 Stars :\n")
for a,b in zip(item_5_stars,pity_5_stars):
    avr += int(b)
    print (a,'pity '+b)
print("Average Pity",avr/(len(item_5_stars)-1))
print ('\n4 Stars :\n')
avr = 0

for a,b in zip(item_4_stars,pity_4_stars):
    avr += int(b)
    print (a,'pity '+b)
print("Average Pity",avr/(len(item_4_stars)-1))