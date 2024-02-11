# TuneSnap
TuneSnap is a song classifier web application powered by CNN.<br>

<h1>Why?</h1>
I've built this project for the smartAInnovators hackathon that will happen in April.<br>
I can almost guarantee that my team will win.<br>
<br>
<h1>Architecture</h1>
It uses a custom CNN I've built to classify 5-second chunks on 8000HZ of any song and transform it into a MEL spectrogram.<br>
From there it just goes through a couple of convolutional layers and the final layer is Softmax.<br>
The only problem with this architecture is scalability.<br>
The more songs to classify, the deeper the model should be.<br>
This can be fixed by possibly replacing the whole architecture with just one ResNet.<br>
<div> <img width="975" alt="Screenshot 2024-02-11 at 13 18 49" src="https://github.com/suibex/TuneSnap/assets/59802817/cf26fc95-7231-4cbc-a793-db619cd951d5"></div>
<h1>How to run it?</h1>
I added poetry for convenience so it takes about 2 minutes to set up.<br>

```
poetry install
poetry shell
python3 main.py
```

Wolla.<br>
You're running TuneSnap instance on your localhost.<br>
Access it on port 8080.<br>


<h1>UI</h1>
<img width="1440" alt="Screenshot 2024-01-25 at 20 00 01" src="https://github.com/suibex/TuneSnap/assets/59802817/9d93a8d0-29f2-40f1-aac0-41185d26f220">
<br>
<img width="1440" alt="Screenshot 2024-01-25 at 20 00 16" src="https://github.com/suibex/TuneSnap/assets/59802817/1d08294b-3ab8-4b30-8002-6c8384327ab3">
<br>
<img width="1440" alt="Screenshot 2024-01-25 at 20 19 33" src="https://github.com/suibex/TuneSnap/assets/59802817/0ecf8928-97bf-41e8-8145-24019c46bbbc">



