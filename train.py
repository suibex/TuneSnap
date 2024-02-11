import torch
import os,io,sys
import numpy as np 
import torch.nn as nn 
import torchaudio
from dataset import Music
import matplotlib.pyplot as plt 


class Network(nn.Module):
    def __init__(self,n_songs):
        super().__init__()

        self.c = nn.Conv1d(128,256,1,1,0)
        self.act = nn.ELU()
        self.o = nn.Conv1d(256,128,4,2,1)
        self.m = nn.MaxPool2d(2)

        self.b1 = nn.BatchNorm1d(64)
        self.b2 = nn.BatchNorm1d(16)
        self.b3 = nn.BatchNorm1d(8)

        self.o1 = nn.Conv1d(64,32,2,2,1)
        self.m1 = nn.MaxPool2d(2)

        self.o2 = nn.Conv1d(16,16,2,2,1)
        self.m2 = nn.MaxPool2d(2)

        self.drop = nn.Dropout(0.25)

        self.lin = nn.Linear(3*8,n_songs)
        self.dd = nn.LogSoftmax(dim=0)

       

    def forward(self,x):
            
        x = self.act(self.c(x))
       
        x = self.o(x)
        x = self.m(x)
        x = self.act(x)
        x = self.b1(x)
            
        x = self.o1(x)
        x = self.m1(x)
        x = self.act(x)
        x = self.b2(x)

        
        x = self.o2(x)
        x = self.m2(x)
        x = self.act(x)
        x = self.b3(x)
        
   #     x = self.drop(x)
        x = x.view(-1)
        x = self.lin(x)
        x = self.dd(x)
  

        return x
    


def train_model():

    data = Music()
    net = Network(data.songidx)

    trainl = torch.utils.data.DataLoader(data,batch_size=1,shuffle=True,num_workers=0)
    lossfn = nn.NLLLoss()
    
    EPOCHS = 200
    LR = 5e-4

    optim = torch.optim.Adam(net.parameters(), lr=LR)
 
    for e in range(EPOCHS):
        dk,d = 0x00, 0x00 

        for b,(x,y) in enumerate(trainl):

            x=x.reshape(x.size(0),128,201)

            optim.zero_grad()

            out = net(x).reshape(1,data.songidx)
            
            y = y.view(-1)

            loss = lossfn(out,y)

            loss.backward()
            optim.step()
            

            dk+=loss.item()
            d+=1
            print("epoch:",e,dk/d)
    
    torch.save(net.state_dict(),"./out.pth")
      


def test_1():

    net = Network(87)

    p = torch.load("./out.pth")
    net.load_state_dict(p)

    audio,freq = torchaudio.load("../example.mp3")
    reshape = torchaudio.transforms.Resample(freq,8000)
    freq = 8000
    
    if(freq == 44100):

        audio = reshape(audio).view(2,-1)[0][:40000]
        torchaudio.save("./kurac.mp3",audio.reshape(1,40000),8000)

    else:
        if(freq == 8000):
            audio = audio[:40000]
    
    spectogram = torchaudio.transforms.MelSpectrogram(8000)

    audio = spectogram(audio).reshape(1,128,201)

    o = np.argmax(net(audio).cpu().detach().numpy(),axis=-1)


def test_shit():
    data = Music(5)
    
    net = Network(60)

    p = torch.load("./out.pth")
    net.load_state_dict(p)

    trainl = torch.utils.data.DataLoader(data,batch_size=1,shuffle=True,num_workers=0)


  

    results = [] 
    succ = 0x00 
    failed = 0x00 

    for _ in range(50):
        vdx = 0x00 
        for b,(x,y) in enumerate(trainl):

            if(vdx >= 5):
                break

            x=x.reshape(1,128,201)
            o = np.argmax(net(x).cpu().detach().numpy(),axis=-1)
            y=y.cpu().detach().numpy()[0][0]

            if(o != y):
                emoji = "❌"
                failed+=1
            else:
                emoji = "✅"
                succ+=1


            results.append([[o,y],emoji])

            vdx+=1

    print("● Test 1 results ")

    print("Success:",succ,"Failed:",failed)


    for res in results:
        try:
            name_song_y = data.song_names[res[0][1]].split("]")[1]
            pred_song_y = data.song_names[res[0][0]].split("]")[1]
            print("***************************************")
            print("Predicted song:",pred_song_y)
            print("Actual song:",name_song_y)
            print("Is it correct?",res[1])
        except Exception as e:
            print("error")
            ...




if __name__ == "__main__":
    #train_model()
    
    test_shit()

