import requests
import xmltodict
import time

def lawParsing(name):
    # public api settings
    age = "21" #알고싶은 국회의원 대수 입력(21대)
    key = "5609737d910a4f43b4c219838556b0b7"
    proposer = name
    url = "https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn?AGE=" + \
            age + "&key=" + key + "&PROPOSER=" +proposer
    req = requests.get(url).content #여기서 requests가 필요하다.
    # the role of xmltodict : It changes xml type into dictionary.
    xmlObject = xmltodict.parse(req)
    try:
        allData_law = xmlObject['nzmimeepazxkubdpn']['row']
        return allData_law
    except:
        return '0'
    # print(allData)

def poliParsing():
    key = "5609737d910a4f43b4c219838556b0b7"
    url = "https://open.assembly.go.kr/portal/openapi/nwvrqwxyaytdsfvhu?key=" + \
            key + "&psize=400"
    req = requests.get(url).content
    xmlObject = xmltodict.parse(req)
    allData_poli = xmlObject['nwvrqwxyaytdsfvhu']['row']
    return allData_poli
