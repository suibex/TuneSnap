import torch
import os,io,sys
import numpy as np 
import torch.nn as nn 
import torchaudio


CHUNK_LENGTH = 5
MAX_CHUNKS = 25

class Music(torch.utils.data.Dataset):
    def __init__(self,max_songs=60):
        super().__init__()

        self.x = [] 
        self.y = []

        files = os.listdir("./data")

        song_idx = 0x00 

        self.song_names = {

        }

       
        idx = 0x00 
        for f in files:
            if(idx == max_songs):
                break
            if(f.endswith(".mp3")):

                audio,freq = torchaudio.load("./data/"+f)
                audio=audio[0]
                reshape = torchaudio.transforms.Resample(freq,8000)

                freq = 8000
                audio = reshape(audio)
                
                chunk_samples = int(freq * CHUNK_LENGTH)
                num_chunks = len(audio)//CHUNK_LENGTH

                chunks = [] 

                if(num_chunks >= MAX_CHUNKS):
                    for i in range(MAX_CHUNKS):

                        start_sample = i*chunk_samples
                        end_sample = chunk_samples+start_sample
                        chunk = audio[start_sample:end_sample]

                        if(len(chunk) == 40000):
                            chunk = chunk.reshape(1,len(chunk))
                            spectogram = torchaudio.transforms.MelSpectrogram(freq)                
                            
                            chunk = spectogram(chunk)

                            
                            chunks.append(np.array(chunk))
                

                    if(len(chunks) >= MAX_CHUNKS):
                        chunks = chunks[:MAX_CHUNKS]
                        if(len(chunks) == MAX_CHUNKS):
                            for chunk in chunks:
                                self.x.append(chunk)
                            
                                self.y.append(np.array([song_idx]))
                    
                            self.song_names[song_idx] = f
                            print("added song:",f)
                            song_idx+=1
                            idx+=1

        self.songidx = song_idx
        print("[*] SONGS LOADED:",self.songidx)

        self.x = torch.tensor(np.array(self.x)).float()
        self.y = torch.tensor(np.array(self.y))

    def __getitem__(self,idx):
        return self.x[idx],self.y[idx]
    
    def __len__(self):
        return self.x.shape[0]
    

#d = Music()
