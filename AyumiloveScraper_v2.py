import urllib.request
import re
from bs4 import BeautifulSoup

#set up our URL handler to load our requests.
url_handler = urllib.request
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'}

#Load the ayumilove homepage.
ayumi_home = url_handler.urlopen(urllib.request.Request('http://ayumilove.net/', headers=header))

#Use and create a BeautifulSoup object so we can parse the html file.
ayumilove_soup = BeautifulSoup(ayumi_home, "html.parser")

#Helper functions
def clean_tags(skill_node):
    skill_build_str = re.sub("<p>|</?strong>", "", str(skill_node.parent))
    skill_build_str = re.sub("</p>|<br/>", "\n", skill_build_str)
    skill_build_str = re.sub("\u2019|&#8217;|\u2018", "'", skill_build_str)
    skill_build_str = re.sub("\u2013", "-", skill_build_str)
    skill_build_str = re.sub("\u2192", "->", skill_build_str)
    skill_build_str = re.sub("\u2191", "^UP^", skill_build_str)
    skill_build_str = re.sub("\<span class=\"details\">|</span>", "", skill_build_str)

    return skill_build_str

#Only get the links that relate to skill build guides and exclude the beginner explorer skills in Maplestory.
def parse_skill_builds(list):
    omit = "(?!sao-sword-art-online-kirito-asuna-leafa|resistance-citizen|noblesse|zen|ayame|pink-bean|shared|beast-tamer|zero|5th-job)"
    skill_build_re = re.compile("http:\/\/ayumilove.net\/maplestory-" + omit + ".+-skill-build-guide\/")
    newList = []

    for url in list:
        url_match = skill_build_re.match(url.get("href"))
        if(url_match):
            if(url_match.group() not in newList and url_match.group() not in begginner_skill_url_list):
                newList.append(url_match.group())

    return newList

#Put urls with skill builds that don't have the generic "...Job Skill Build:" regex.
begginner_skill_url_list = ["http://ayumilove.net/maplestory-warrior-skill-build-guide/",
                           "http://ayumilove.net/maplestory-archer-skill-build-guide/",
                           "http://ayumilove.net/maplestory-thief-skill-build-guide/",
                           "http://ayumilove.net/maplestory-magician-skill-build-guide/",
                           "http://ayumilove.net/maplestory-pirate-skill-build-guide/"]

explorer_skill_builds = {"warrior":"", "archer":"", "thief":"", "magician":"", "pirate":""}

warrior_category = ["http://ayumilove.net/maplestory-dark-knight-skill-build-guide/",
                    "http://ayumilove.net/maplestory-hero-skill-build-guide/",
                    "http://ayumilove.net/maplestory-paladin-skill-build-guide/"]

mage_category = ["http://ayumilove.net/maplestory-bishop-skill-build-guide/",
                 "http://ayumilove.net/maplestory-fire-poison-archmage-skill-build-guide/",
                 "http://ayumilove.net/maplestory-ice-lightning-arch-mage-skill-build-guide/"]

thief_category = ["http://ayumilove.net/maplestory-night-lord-skill-build-guide/",
                  "http://ayumilove.net/maplestory-shadower-skill-build-guide/"]

archer_category = ["http://ayumilove.net/maplestory-bow-master-skill-build-guide/",
                   "http://ayumilove.net/maplestory-marksman-skill-build-guide/"]

pirate_category = ["http://ayumilove.net/maplestory-buccaneer-skill-build-guide/",
                   "http://ayumilove.net/maplestory-corsair-skill-build-guide/"]

beast_tamer_skill_url = "http://ayumilove.net/maplestory-beast-tamer-skill-build-guide/"

zero_skill_url = "http://ayumilove.net/maplestory-zero-skill-build-guide/"

#Section to get the generic begginner skill builds for the explorer class and storer it in
begginner_skill_re = "Skill Build Guide:|Skill Build:?"

#Load and store the html document in a variable from the begginner_skill_url_list
warrior_urllib = url_handler.urlopen(url_handler.Request(begginner_skill_url_list[0], headers=header))
archer_urllib = url_handler.urlopen(url_handler.Request(begginner_skill_url_list[1], headers=header))
thief_urllib = url_handler.urlopen(url_handler.Request(begginner_skill_url_list[2], headers=header))
magician_urllib = url_handler.urlopen(url_handler.Request(begginner_skill_url_list[3], headers=header))
pirate_urllib = url_handler.urlopen(url_handler.Request(begginner_skill_url_list[4], headers=header))

#Create a BeautifulSoup object to parse through each webpages.
warrior_skills_soup = BeautifulSoup(warrior_urllib, "html.parser")
archer_skills_soup = BeautifulSoup(archer_urllib, "html.parser")
thief_skills_soup = BeautifulSoup(thief_urllib, "html.parser")
magician_skills_soup = BeautifulSoup(magician_urllib, "html.parser")
pirate_skills_soup = BeautifulSoup(pirate_urllib, "html.parser")

#Remove any unicode or html tags from the input and then store it into a variable.
warrior_skills_str = clean_tags(warrior_skills_soup.find("strong", string=re.compile(begginner_skill_re)))
archer_skill_str = clean_tags(archer_skills_soup.find("strong", string=re.compile(begginner_skill_re)))
thief_skills_str = clean_tags(thief_skills_soup.find("strong", string=re.compile(begginner_skill_re)))
magician_skills_str = clean_tags(magician_skills_soup.find("strong", string=re.compile(begginner_skill_re)))
pirate_skills_str = clean_tags(pirate_skills_soup.find("strong", string=re.compile(begginner_skill_re)))

#Store the skill builds into the proper category.
explorer_skill_builds["warrior"] = warrior_skills_str
explorer_skill_builds["archer"] = archer_skill_str
explorer_skill_builds["thief"] = thief_skills_str
explorer_skill_builds["magician"] = magician_skills_str
explorer_skill_builds["pirate"] = pirate_skills_str



#Move to the section of the tree that contains all URL Skill Builds and return a list of children.
url_list = ayumilove_soup.body.div.div.find_all("a")


job_skill_re = ".+ Job Skill Build.*:|(.+ Job Skill Build:|Skill Build:?|(?!Beginner )Skill Build Guide:|^Ice-Lightning 2nd Job Skill Build$)"

url_list = parse_skill_builds(url_list)

for url in url_list:
    skill_build_url = url_handler.urlopen(url_handler.Request(url, headers=header))
    skill_build_soup = BeautifulSoup(skill_build_url, "html.parser")

    textName = str(skill_build_soup.title.string).replace("|", "")
    f = open(textName + ".txt", "w+")

    #Check which class contains the generic begginner skills and add it to the text file.
    if(url in warrior_category):
        f.write(warrior_skills_str)
    elif(url in archer_category):
        f.write(archer_skill_str)
    elif(url in thief_category):
        f.write(thief_skills_str)
    elif(url in mage_category):
        f.write(magician_skills_str)
    elif(url in pirate_category):
        f.write(pirate_skills_str)

    skill_build_list = skill_build_soup.find_all("strong", string=re.compile(job_skill_re))

    for skill_node in skill_build_list:
        # Parse and replace the string with any unicode that won't translate well to .txt file.
        current_skill_build = clean_tags(skill_node)

        f.write(current_skill_build)
        #Place "ending markers" to divide the skill builds into sections in the .txt file.
        f.write("~End_Of_Section~\n")
    f.close()

#Zero skill build url and beast tamer url will be parsed here because the format is a bit different and not "Generic"
zero_skill_re = "(Alpha|Beta) Skill Build:"
beast_tamer_skill_re = "((Bear|Snow Leopard|Hawk|Cat) Skill Build:)|^Beast Tamer Hyper Skill Build Guide:$"

zero_urllib = url_handler.urlopen(url_handler.Request(zero_skill_url, headers=header))
beast_tamer_urllib = url_handler.urlopen(url_handler.Request(beast_tamer_skill_url, headers=header))

zero_skill_soup = BeautifulSoup(zero_urllib, "html.parser")
beast_tamer_skill_soup = BeautifulSoup(beast_tamer_urllib, "html.parser")

#Get the skill build for zero and store it in a list. *find_all returns a list of results.
zero_skills_html = zero_skill_soup.find_all("strong", string=re.compile(zero_skill_re))
zero_skill_build_str = [clean_tags(zero_skills_html[0]), clean_tags(zero_skills_html[1])]

#Store the information into the text file.
zero_skill_file = open(str(zero_skill_soup.title.string).replace("|", "") + ".txt", "w+")
zero_skill_file.write(zero_skill_build_str[0])
zero_skill_file.write("~End_Of_Section~\n")
zero_skill_file.write(zero_skill_build_str[1])
zero_skill_file.write("~End_Of_Section~\n")
zero_skill_file.close()

#Get the skill build for beast tamer and store it in a list.
beast_tamer_skills_html = beast_tamer_skill_soup.find_all("strong", string=re.compile(beast_tamer_skill_re))
beast_tamer_skill_file = open(str(beast_tamer_skill_soup.title.string).replace("|", "") + ".txt", "w+")

for skill_build in beast_tamer_skills_html:
    beast_tamer_skill_file.write(clean_tags(skill_build))
    beast_tamer_skill_file.write("~End_Of_Section~\n")

beast_tamer_skill_file.close()

