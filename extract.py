import re
import requests
import json
from bs4 import BeautifulSoup
from collections import OrderedDict

DREAMBANK = "http://dreambank.net/random_sample.cgi?series={0}&min=1&max=9999&n=10000"

# Dream collections to download
DREAMERS = {
    "alta": "Alta: a detailed dreamer", "angie": "Angie: age 18 & 20", "arlie": "Arlie: a middle-aged woman", "b": "Barb Sanders", "b2": "Barb Sanders #2", "b-baseline": "Barb Sanders: baseline", "bay_area_girls_456": "Bay Area girls: Grades 4-6", "bay_area_girls_789": "Bay Area girls: Grades 7-9", "bea1": "Bea 1: a high school student", "bea2": "Bea 2: a college student", "blind-f": "Blind dreamers (F)", "blind-m": "Blind dreamers (M)", "chris": "Chris: a transvestite", "chuck": "Chuck: a physical scientist", "hall_female": "College women, late 1940s", "dahlia": "Dahlia: concerns with appearance", "david": "David: teenage dreams", "vonuslar.de": "Detlev von Uslar, auf Deutsch", "dorothea": "Dorothea: 53 years of dreams", "ed": "Ed: dreams of his late wife", "edna": "Edna: a blind woman", "elizabeth": "Elizabeth: a woman in her 40s", "emmas_husband": "Emma's Husband", "emma": "Emma: 48 years of dreams", "esther": "Esther: an adolescent girl", "german-f.de": "German dreams (F)", "german-m.de": "German dreams (M)", "norms-f": "Hall/VdC Norms: Female", "norms-m": "Hall/VdC Norms: Male", "jasmine1": "Jasmine 1: middle school", "jasmine2": "Jasmine 2: high school", "jasmine3": "Jasmine 3: college 1", "jasmine4": "Jasmine 4: college 2", "jeff": "Jeff: a lucid dreamer", "joan": "Joan: a lesbian", "kenneth": "Kenneth", "lawrence": "Lawrence, a young man", "mack": "Mack: A poor recaller", "madeline1-hs": "Madeline 1: High School", "madeline2-dorms": "Madeline 2: College Dorms", "madeline3-offcampus": "Madeline 3: Off-Campus", "madeline4-postgrad": "Madeline 4: After College", "mark": "Mark: a young boy", "melissa": "Melissa: a young girl", "melora": "Melora (Melvin's wife)", "melvin": "Melvin (Melora's husband)", "merri": "Merri: an artist", "miami-home": "Miami Home-Lab: Home", "miami-lab": "Miami Home-Lab: Lab", "midwest_teens-f": "Midwest teenagers (F)", "midwest_teens-m": "Midwest teenagers (M)", "nancy": "Nancy: Caring & headstrong", "natural_scientist": "The Natural Scientist", "norman": "Norman: a child molester", "pegasus": "Pegasus: a factory worker", "peru-m": "Peruvian men", "peru-f": "Peruvian women", "phil1": "Phil 1: teens", "phil2": "Phil 2: late 20s", "phil3": "Phil 3: retirement", "physiologist": "The Physiologist", "ringo": "Ringo: from the 1960s", "bosnak": "Robert Bosnak: A dream analyst", "samantha": "Samantha: in her 20s", "seventh_graders": "Seventh grade girls", "zurich-f.de": "Swiss children, auf Deutsch (F)", "zurich-m.de": "Swiss children, auf Deutsch (M)", "toby": "Toby: A friendly party animal", "tom": "Tom: An outgoing man", "ucsc_women": "UCSC women, 1996", "vickie": "Vickie: a 10-year-old girl", "vietnam_vet": "Vietnam Vet: 1970-2008 war dreams", "vietnam_vet2": "Vietnam Vet: 2015 dreams", "wedding": "Wedding dreams", "west_coast_teens": "West Coast teenage girls" }


NUMBER_RE = r'^\#(\S+)'

HEAD_RE = r'^\((.+?)\)(\w)'

def process_dream_span(span):
    text = span.text.encode('utf-8').strip()
    # remove number
    number_groups = re.match(NUMBER_RE,  text)
    number = number_groups.group(1).strip()
    
    text = re.sub(NUMBER_RE, '', text).strip()
    
    # remove word count
    text = re.sub(r'\s*\(\d+\s+words\)\s*$', '', text, re.I)
    
    # Split nb-space as paragraphs
    text = re.sub('\\s*?(\xc2\xa0)+\\s*', '\n', text).strip()
    
    # sep desc
    head_match = re.match(HEAD_RE, text)
    if head_match is None:
        return OrderedDict([
            ('number', number),
            ('content', text)])

    head = head_match.group(1).strip()
    text = re.sub(HEAD_RE, lambda x: x.group(2), text).strip()

    return OrderedDict([
        ('number', number),
        ('head', head),
        ('content', text)])

def process_dream_page(text):
    soup = BeautifulSoup(text, 'html.parser')
    dreams = soup.find_all('span')
    
    for dream in soup.find_all('span'):
        data = process_dream_span(dream)
        if data is not None:
            yield data

def download_dreams(dreamer):
    url = DREAMBANK.format(dreamer)
    r = requests.get(url)
    if r.status_code != 200:
        print("error getting dreams")
        return None
    return r.text

def collect_dreams(dreamer, desc):
    text = download_dreams(dreamer)
    return OrderedDict([
        ('dreamer', dreamer),
        ('description', desc),
        ('dreams', list(process_dream_page(text)))])


for dreamer, desc in DREAMERS.iteritems():
    dreams = collect_dreams(dreamer, desc)
    if dreams is not None:
        with open('dreams/' + dreamer + '.json', 'w') as out_file:
            json.dump(dreams, out_file, sort_keys=False, indent=4, ensure_ascii=False)
