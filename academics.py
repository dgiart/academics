import requests
import re
import pickle
import numpy as np
from bs4 import BeautifulSoup
from datetime import date
import sys, os, time

def age(birthDate):
    actualDate = date.today()
    actualDateList = [actualDate.day,actualDate.month, actualDate.year]
    birthDateList = [int(num) for num in birthDate.split('.')]
    age =np.array(actualDateList) - np.array(birthDateList)
    if age[1] > 0:
        return age[2]
    elif age[1] < 0:
        return age[2] - 1
    else:
        if age[0] > 0:
            return age[2]
        else:
            return age[2] - 1

def academicsIdList(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,features="lxml")
    academicsPages = soup.findAll("a",{"class":"onHoverBold"})
    ids = []
    for page in academicsPages[5:]:
        num = ''.join(re.findall('\d',str(page)))
        ids.append(num)
    return ids
def get_name_birth(url, _id):
    print(f'id = {_id}')
    # import requests
    #
    # from bs4 import BeautifulSoup
    response = requests.get(url)
    soup = BeautifulSoup(response.text,features="lxml")
    name = None
    birthDate = None
    pers = {}
    try:
        nameInSoup = soup.find('a', {"class" :"nas-siteHeader nas-siteHeader-level1"})
        nameUncleaned = nameInSoup.contents[0]
        name = re.sub("\d|\\.|\(|\)|\r|\n|\t","",nameUncleaned)
        # print(f'name = {name}\n')
    except:
        pass
        # print ('NO name')
    try:
        info = soup.find('div', {"class" :"FontContentPersonalSite"})
        birth = re.split(' +',str(info.contents[0]))
        birthDate = birth[1]
        # print(f'info =\n {birthDate}\n\n')
    except:
        pass
        # print ('NO info\n\n')
    if name != None and birthDate != None:
        pers['id'] = _id
        pers['name'] = name,
        pers['birthDate'] = birthDate
    return pers


    # print(dir(info.contents[0].string))
    # num = Div.text[:-8].replace(' ', '')
    # return int(num)



def main():
    start = time.time()
    print (age('15.03.1979'))
    urlAcad = 'http://nas.gov.ua/UA/Members/Pages/Academicians.aspx'
    members = []
    academicsIds = academicsIdList(urlAcad)
    # n = 1
    # for academicId in academicsIds:
    #     print(f'{n}:  {academicId}')
    #     n += 1
    for academicId in academicsIds:
        url = url = f'http://nas.gov.ua/UA/PersonalSite/Pages/Biography.aspx?PersonID={academicId}'
        pers = get_name_birth(url,academicId)
        if pers != {}:
            print (f"id = {pers['id']}, name: {pers['name']}, birthDate: {pers['birthDate']}")
            # age_ = age(pers['birthDate'])
            # pers['age'] = age_
            # members.append(pers)
    # print(f'members: {len(members)}\n')
    # with open('academics.pckl','wb') as file:
    #     pickle.dump(members, file)
    # fin = time.time()
    # print (f'Time fo {len(academicsIds)} people: {fin - start}')


# def main():
#     import sys, os, time
#     start = time.time()
#     print (sys.version)
#     print (os.getcwd())
#
#     # url = f'http://nas.gov.ua/UA/PersonalSite/Pages/Biography.aspx?PersonID=0000000074'
#     ids = range(70,80)
#     id0 = '0000000000'
#     members = []
#     for _id in ids:
#         url = f'http://nas.gov.ua/UA/PersonalSite/Pages/Biography.aspx?PersonID={id0[:len(id0) - len(str(_id))] + str(_id)}'
#         pers = get_name_birth(url,_id)
#
    #     if pers != {}:
    #         age_ = age(pers['birthDate'])
    #         name = pers['name']
    #         print (f'age = {age_}, name: {name}')
    #         members.append(pers)
    # print(f'members: {len(members)}\n')
    # print(members)
    # with open('academics.pckl','wb') as file:
    #     pickle.dump(members, file)
    # fin = time.time()
    # print (f'Time fo {len(ids)} people: {fin - start}')





if __name__ == '__main__':
    main()
