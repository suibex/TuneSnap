
var CTX = undefined;
var microphone = undefined;
var recording = false;

var audio_chunk = [] 
var mediaStream = undefined;
var mediaRecorder = undefined;

var recTimer = undefined;


async function recordAudio(){

  const inputElement = document.getElementById("audioFileInput");

  console.log(inputElement)

  // Check if a file is selected
  if (inputElement.files.length > 0) {
      const audioFile = inputElement.files[0];


// Create a FileReader
const reader = new FileReader();

// Define the function to execute when the file is read
reader.onload = async function(event) {
    // Access the result (file content) as a buffer
    const url = event.target.result;
    document.getElementById("sml-notif").style.display="block";
    var arr = new Uint8Array(url)
    console.log(arr); 
    var rq = await fetch("/predictSong",{
      method:"POST",
      body:JSON.stringify({
        'data':arr
      }),
      headers:{
        'Content-Type':'application/json'
      }
    })
  
  
    document.getElementById("sml-notif").style.display="block";
    var resp = await rq.json();

  
  
    document.getElementById("sml-notif").style.display="none";
    document.getElementById("overlay").style.backgroundColor="black";
    document.getElementById("circle").style.display="none";
    document.getElementById("result").style.display="block";
    document.getElementById("biggie").textContent=resp['song']
    document.getElementById("biggie").style.fontSize="6vw";
    document.getElementById("kd").display="block"
    

    document.getElementById("artist_name").style.display="block";
    document.getElementById("artist_name").textContent = resp['artist']


    document.body.style.backgroundColor="black";
    document.body.style.background="black";

};

// Read the file as an ArrayBuffer
    reader.readAsArrayBuffer(audioFile);
  }



}

document.getElementById('btn-click').addEventListener('click', function () {
  document.getElementById('audioFileInput').click();
});


document.getElementById('audioFileInput').addEventListener('change', function () {
  recordAudio();
});
