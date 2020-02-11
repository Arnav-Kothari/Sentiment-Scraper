# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import requests
from bs4 import BeautifulSoup

AIREQ =  'https://www.airlinequality.com/airline-reviews/jetblue-airways/?fbclid=IwAR3MvWvi0PVXyheq9TpmIOT9Bb_dDoAZm5BtGHESn5acW_QmOjjlEoGTWis'
REDDIT = 'https://www.reddit.com/r/jetblue/'
C_AFFAIRS = 'https://www.consumeraffairs.com/travel/jetblue.html'
KAYAK = 'https://www.kayak.com/JetBlue.B6.airline.html'

outfile = "output.txt"
# FUNCTION: reddit HTML reader and writer
# PARAMETER: 'soup' variable
def printReddit(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    with open(outfile,'w', encoding = "utf8") as file:
        for p in soup.find_all('p'):
            str = p.text + '\n'
            file.write(str)
            # print(str)

def printairEq(url):  
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    with open(outfile,'w', encoding = "utf8") as file:
        posts = soup.find_all(class_='tc_mobile')
        for post in posts:
            com = post.find(class_='text_content').get_text().replace('\n', '')
            file.write(com + '\n')
            # print(com + '\n')

def printCAffairs(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    with open(outfile,'w', encoding = "utf8") as file:
        temp = 0
        for p in soup.select('p'):
            # write the even paragraphs to output
            if (temp % 2 == 0):
                str = p.text + '\n'
                file.write(str)
       
            temp = temp + 1

def printKayak(url):
    # response gets url
    response = requests.get(url)
  
    # Soup holds the parsed HTML data
    soup = BeautifulSoup(response.text, 'html.parser')
    # writes to a file and encodes the text for efficency
    with open(outfile,'a', encoding = "utf8") as file:
        # finds and outputs all the paragraphs in the file
        for p in soup.find_all('p'):
            str = p.text + '\n'
            file.write(str)
     


# url = 'https://www.tripadvisor.com/Hotel_Review-g1933359-d307591-Reviews-Amandari-Kedewatan_Ubud_Gianyar_Regency_Bali.html'
# url = 'https://www.facebook.com/pg/JetBlue/community/?ref=page_internal'
# url = 'https://twitter.com/search?q=jetblue&src=typed_query'
# url = 'https://www.esky.com/reviews/al/b6/jetblue'

# --- Gets HTML from URL and puts into var soup ---
print("Select: Reddit or Airline equality or Cons affairs or Kayak")
website = input()

if (website == "Reddit"):
    printReddit(REDDIT)
    
if (website == "Airline equality"):
    printairEq(AIREQ)

if (website == "Cons affairs"):
    printCAffairs(C_AFFAIRS)

if (website == "Kayak"):
    printKayak(KAYAK)

flags = input("Extremes? (y/n): ")
    

# Instantiates a client
client = language.LanguageServiceClient()
# The text to analyze
f = open(outfile, "r", encoding='utf8')
text = f.read()
document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
response = client.analyze_sentiment(document)


total = response.document_sentiment.score
for sentence in response.sentences:
    if (flags == "y"):
        if (sentence.sentiment.score > 0.8 or sentence.sentiment.score < -0.8):
            print("Sentence text: {}".format(sentence.text.content))
            print("Score: {}".format(float(sentence.sentiment.score)))
            print("Magnitude: {}".format(float(sentence.sentiment.magnitude)))
            print("\n")
    else:
        print("Sentence text: {}".format(sentence.text.content))
        print("Score: {}".format(float(sentence.sentiment.score)))
        print("Magnitude: {}".format(float(sentence.sentiment.magnitude)))
        print("\n")

print('Overall Sentiment: {0:.1f}'.format(float(total)))
f.close()






