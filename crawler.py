import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
from PyLyrics import *
class singerClass():
    def __init__(self,singer):
        self.singer = singer
        self.tracks = get_tracks(singer)
        self.getLyrics()
    def getLyrics(self):
        global total
        for track in self.tracks:
            X = []
            if len(track) < 2:
                print singer,':',track,'has no lyrics.'
                continue
            if self.check_exist(track[0],track[1]):
                total+=1
                print singer,':',track,'exists.'
                continue
            try:
                X = PyLyrics.getLyrics(track[0],track[1])
            except:
                print 
            if len(X) < 10 :
                print singer,':',track,'has no lyrics.'
                continue
            self.dumpLyrics(track[0],track[1],X)
            print 'songID:',total
            print singer,':',track,'has successfully been dumped.'
    def dumpLyrics(self,singer,track,lyrics):
        global total
        singer = singer.replace(' ','_').replace('/','').lower()
        track = track.replace(' ','_').replace('/','').lower()
        cwd = os.getcwd()
        LyricsDir = os.path.join(cwd,'Lyrics')
        SingerDir = os.path.join(LyricsDir,singer)
        dstDir = os.path.join(SingerDir,track+'.txt')
        if os.path.isdir(SingerDir) is False:
            os.mkdir(SingerDir)
        with open(dstDir,'w') as fp:
            fp.write(lyrics)
            fp.close()
        total += 1
    def check_exist(self,singer,track):
        singer = singer.replace(' ','_').replace('/','').lower()
        track = track.replace(' ','_').replace('/','').lower()
        cwd = os.getcwd()
        LyricsDir = os.path.join(cwd,'Lyrics')
        SingerDir = os.path.join(LyricsDir,singer)
        dstDir = os.path.join(SingerDir,track+'.txt')
        return os.path.isfile(dstDir)

def get_tracks(singer):
    s = requests.get('http://lyrics.wikia.com/{0}'.format(singer))
    songList = []
    for obj in s.text.split('\n'):
        if obj.startswith('<ol><li> <b><a') or obj.startswith('</li><li> <b><a'):
            start = obj.find('/wiki/')
            end = obj.find('\"',start)
            X = obj[start+6:end]
            songList.append(X.split(':'))
    return songList
def get_singer():
    s = requests.get('http://lyrics.wikia.com/wiki/Category:Hometown/United_States').text,"html.parser"
    singerList = []
    for obj in s[0].split('\n'):
        if obj.startswith('<ul><li><a') or obj.startswith('<li><a'):
            start = obj.find('/wiki/')
            end = obj.find('\"',start)
            singerList.append(obj[start+6:end])
    return singerList
if __name__ == '__main__':
    global total
    total = 0
    singers = get_singer()
    singerList = []
    for singer in singers:
        print 'Processing ',singer
        Sc = singerClass(singer)
    print 'There are',total,'songs been recorded.'



#spans = s.findAll('span',{'class':'CategoryTreeToggle'})
#for tag in spans:
#    tag = str(tag)
#    print tag
    #start = tag.find('United_States/')
    #end = tag.find('\"',start)
   # tag[start:end]
