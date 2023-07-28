# Hello explorer, you have been selected to be part of an early beta for a new system.
# If you encounter an issues with running, packager, and language server (autocomplete, code diagnostics),
# please email devex@replit.com or post on ask.replit.com
# You can always turn off explorer from https://replit.com/account#roles
# 
# Thank you!

import json
import time
#from datetime import datetime
import random


from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, CategoriesOptions
#from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Authentication via IAM
# authenticator = IAMAuthenticator('your_api_key')
# service = NaturalLanguageUnderstandingV1(
#     version='2018-03-16',
#     authenticator=authenticator)
# service.set_service_url('https://gateway.watsonplatform.net/natural-language-understanding/api')

# Authentication via external config like VCAP_SERVICES
service = NaturalLanguageUnderstandingV1(
    version='2018-03-16')
#service.set_service_url('https://gateway.watsonplatform.net/natural-language-understanding/api')

#response = service.analyze(
#    text='Bruce Banner is the Hulk and Bruce Wayne is BATMAN! '
#    'Superman fears not Banner, but Wayne.',
#    features=Features(entities=EntitiesOptions(),
#                      keywords=KeywordsOptions())).get_result()

#print(json.dumps(response, indent=2))

url1 = "http://newsroom.ibm.com/Guerbet-and-IBM-Watson-Health-Announce-Strategic-Partnership-for-Artificial-Intelligence-in-Medical-Imaging-Liver"
url2 = "https://medium.com/swlh/how-to-study-for-data-structures-and-algorithms-interviews-at-faang-65043e00b5df" 
url3 = "https://developer.ibm.com/tutorials/smart-bookmark-plugin-using-watson-nlu/"
url4 = "https://www.msn.com/en-in/money/technology/alien-life-on-saturn-moon-nasa-cassini-found-potential-proof-says-study/ar-AALXLVN?ocid=winp1taskbar"
url5 = "https://kgisl.github.io/makesite/blog/cokreating-geniuses/"
url6 = "https://j.mp/bookThis"
url7 = "https://stackoverflow.blog/2021/07/07/the-unexpected-benefits-of-mentoring-others/"
url8 = "https://www.businesstoday.in/industry/it/story/tcs-to-hire-40000-freshers-from-campuses-in-current-fiscal-300932-2021-07-09"
url9 = "https://www.deccanherald.com/business/business-news/elon-musk-trial-asks-the-2-billion-question-who-controls-tesla-1006673.html"
url10 = "https://www.tennisworldusa.org/tennis/news/Roger_Federer/99764/novak-djokovic-i-hope-that-roger-federer-rafael-nadal-and-me-can-/"
urls = [url1, url2, url3, url4, url5, url6, url7, url8, url9, url10]


filename = "urls.txt"
with open(filename, 'r') as fp:
    urls = fp.readlines()

filename = "chrome_bookmarks.json"

data = ""
try: 
    with open(filename, encoding="utf8") as fp: 
        data = json.loads(fp.read())

    urls = [] 
    for d in data:
        if 'url' in d:
            urls.append(d['url'])

except Exception as error:
    print(error)



#Summary object 
categ = dict()
failed = list()

random.seed(time.time())
#random.seed(datetime.now())
random.shuffle(urls)


for i, nlu_url in enumerate(reversed(urls[:400]), 1):
    nlu_url = nlu_url.strip()
    try:
        response = service.analyze(
            url=nlu_url,
            features=Features(categories=CategoriesOptions(), \
                            #entities=EntitiesOptions(),
                            #keywords=KeywordsOptions())
                            )).get_result()
    except Exception as error:
        print(error)
        failed.append(nlu_url)
        time.sleep(2)

    # print(json.dumps(response, indent=2))
    print(i, response['retrieved_url'])
    for c in response['categories']:
        score, label = c['score'], c['label'] 
        # print("-", score, label)
    
        if label not in categ:
            categ[label] = score
        else:
            categ[label] += score

print("--------")
#print("Not processed", failed) if failed else print("All processed")
print("Summary")

from collections import defaultdict
entries = categ.items()
summary = defaultdict(dict)
for label, count in sorted(entries, key=lambda x:x[1], reverse=True):
    print(label, count)
    tokens = label.split('/')
    top = tokens[1]
    if len(tokens) > 2: 
        subs = tokens[2:]
    if top not in summary:
        summary[top]['count'] = count
        summary[top]['subs'] = set(subs)
    else:
        summary[top]['count'] += count
        summary[top]['subs'].update(subs)
        
print("-----CONSOLIDATED----")
for top, info in sorted(summary.items(), key=lambda x:x[1]['count'], reverse=True):
    print(f'- {info["count"]:.2f}: {top.upper()} {", ".join(sorted(info["subs"]))}')

