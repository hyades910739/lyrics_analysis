try:
	import requests
	import bs4
	from bs4 import BeautifulSoup
	import os
	import re
	import sys	
except:
	print("This script require bs4,requests,installed it.")
	exit()


'''
function to get lyrics from mojim
require bs4 and request
'''
def get_lyrics(url):
    web = requests.get(url)
    soup = BeautifulSoup(web.text,"lxml")
    temp = soup.select("#fsZx3")
    try:
        temp = temp[0]
    except:
        print("failed to load lyrics at url : ",url)
        return 0
    lyrics = []
    end = re.compile('\[[0-9]')
    u3000 = re.compile("\u3000")    
    for sent in temp.children:
        if type(sent) is bs4.element.Tag:
            sent.append('\n')
        else:
            sent = str(sent)
            if end.match(sent):
                break
            sent = u3000.sub(" ",sent)    
            lyrics.append(sent)
    return "\n".join(lyrics)


def main():
	if len(sys.argv)< 2:
		raise ValueError('please input a mojim album url')

	urls = sys.argv[1:]
	songs_url = {}
	for url in urls:
		web_album = requests.get(url)
		soup = BeautifulSoup(web_album.text,"lxml")
		# get folder name, create it
		album,_,artist,*_ = soup.find("meta",attrs={"property":"og:title"}).get("content").split()
		quote = re.compile("[()]")
		album = quote.sub("",album)
		artist = quote.sub("",artist)
		fold_name = artist+"_"+album
		fold_name = os.path.join("lyrics",fold_name)
		if not os.path.exists("lyrics"):
			os.mkdir("lyrics")
		print("now crawling : ",fold_name,"...")
		try:
			os.mkdir(fold_name)
		except FileExistsError:
			print("folder : ",fold_name,", is already existed, skip it.")			
		# get song urls:
		soup.select(".hc3",limit=2)
		for span in soup.select(".hc3",limit=2):
		    for a in  span.select("a"):
		        title = a['title']
		        url = a['href']
		        songs_url[title] = url
		#crawl!!
		lyrics_dict = {}
		for title,url in songs_url.items():
		    #把歌詞兩個字從title刪去:
		    title = re.split("歌詞",title)[0]
		    url = "".join(["https://mojim.com",url])
		    lyrics_dict[title] = get_lyrics(url)

		# in case some web failed to load
		fail_lyrics = []
		for key,value in lyrics_dict.items():
		    if value is 0:
		        fail_lyrics.append(key)
		for key in fail_lyrics:
		    lyrics_dict.pop(key)    

		for title,lyrics in lyrics_dict.items():
		    with open(os.path.join(fold_name,title)+".txt",'w') as f:
		        f.write(lyrics)

	return 0

if __name__ == '__main__':
		main()	