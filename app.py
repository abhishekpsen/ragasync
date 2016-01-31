from flask import Flask, request, render_template
import datetime,random
import urllib
import urllib2
from bs4 import BeautifulSoup

app = Flask(__name__)

#Name this method same as the url
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/music', methods=['POST','GET'])
def music():
	if request.method == 'POST':
		artist = request.form['artist']
		time_of_day = get_time_of_day(request.form['time'])
		raaga = get_raaga(time_of_day)
		video_urls = get_youtube_videos(raaga, artist)
		return render_template('music.html',video_urls=video_urls,time_of_day=time_of_day,raaga=raaga)
	else:
		artist = ''
		time_of_day = get_time_of_day()
		raaga = get_raaga(time_of_day)
		video_urls = get_youtube_videos(raaga, artist)
		return render_template('music.html',video_urls=video_urls,time_of_day=time_of_day,raaga=raaga)

def get_time_of_day(current_hour = datetime.datetime.now().hour):
	if current_hour < 12:
		return 'Morning'
	elif current_hour < 16:
		return 'Afternoon'
	elif current_hour < 20:
		return 'Evening'
	else:
		return 'Night'

def get_raaga(time_of_day):
	raagas = {'Morning':['Ahir Bhairav','Gurjari Todi','Sohini', 'Basant','Todi',\
	'Bhoopali Todi','Bhatiyar','Nat Bhairav','Bhairavi'],\
	 'Afternoon':['Poorvi', 'Madhuvanti', 'Bhimpalasi', 'Shuddha Sarang','Bhairavi',\
	 'Vrindavani Sarang','Multani','Gaud Sarang'],\
	  'Evening':['Desh', 'Yaman Kalyan', 'Khamaj', 'Puriya Dhanashri','Bhairavi',\
	  'Maru Bihag','Hansadhwani','Shuddha Kalyan','Marwa','Kamod'], \
	  'Night':['Malkauns', 'Bhinna Shadaj', 'Kedar', 'Kalavati','Bhairavi', \
	  'Tilak Kamod','Bageshri','Charukeshi','Darbari','Hamir','Malhar','Bihag']}
	return random.choice(raagas[time_of_day])

def get_youtube_videos(raaga,artist):
	if artist:
		textToSearch = 'Raga %s %s'%(raaga,artist)
	else:
		textToSearch = 'Raga %s'%(raaga)
	query = urllib.quote(textToSearch)
	url = "https://www.youtube.com/results?search_query=" + query
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html)
	video_urls = []
	for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
		video_urls.append('https://www.youtube.com/embed/' + vid['href'][9:])
	return video_urls


if __name__ == '__main__':
	app.run()
