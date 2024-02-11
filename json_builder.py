import json
import os,io,sys
import eyed3


def build_data_json():
    
   od = os.listdir("./data")
   
   out_json = {
  
   }  



   od = [x for x in od if x.endswith(".mp3")]
   song_list = [] 
  
   for idx,f in enumerate(od):
    if(idx >= 60):
      break
    
    if(f.endswith(".mp3")):

      audio  = eyed3.load("./data/"+f)
      out_json[idx]={
        'artist':audio.tag.artist,
        'title':audio.tag.title
      }
      song_list.append(audio.tag.artist+","+audio.tag.title)


    o = "\n".join(song_list)

    fd =open("./song_list.txt","w")
    fd.write(o)
    fd.close()
    
    fd =open("./songs.json","w")
    fd.write(json.dumps(out_json))
    fd.close()

build_data_json()


