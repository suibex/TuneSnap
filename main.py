import flask
from flask import * 
import os,io,sys
import torch
from train import Network
import torchaudio
import numpy as np
from io import BytesIO
import struct
import tempfile
from dataset import Music

class TuneSnapWeb:
    def __init__(self,pth) -> None:
        
        self.net = Network(60)
        mdl = torch.load(pth)
        
        fd = open("./songs.json","r")
        self.songs = json.loads(fd.read())
        
        fd.close()


        self.net.load_state_dict(mdl)
        print("** model loaded: ",self.net)

        self.app = flask.Flask(__name__)

        @self.app.route("/")
        def main():
            return render_template("index.html")

        @self.app.route("/predictSong",methods=["POST"])
        def predict():

            out = {
                'song':'',
                'idx':'',
                'artist':''
            }

            data = request.json
            data=data['data']
            dat = [] 
            for x in data:
                dat.append(struct.pack("B",data[x]))

            data = b"".join(dat)

            bobj = BytesIO(data)

            reshape = torchaudio.transforms.Resample(44100,8000)
            audio,freq = torchaudio.load(bobj)
            audio=audio[0]

            if(freq == 44100):

                audio = reshape(audio).view(-1)[:40000]
            
            else:
                if(freq == 8000):
                    audio = audio[:40000]

            
            spectogram = torchaudio.transforms.MelSpectrogram(8000)

            audio = spectogram(audio)
            audio =audio.reshape(1,128,201)

            outidx = self.net(audio)

            outidx = np.argmax(outidx.cpu().detach().numpy(),axis=-1)
        
            song = self.songs[str(outidx)]

            out['idx'] = str(outidx)
            out['song'] = song['title']
            out['artist'] = song['artist']
         


            return jsonify(out)
        


    def deploy(self):
        self.app.run("0.0.0.0",80,debug=True)


web = TuneSnapWeb("./out.pth")
web.deploy()
