function myFunction() {
    document.getElementById("some").innerHTML = "Kek";
}


let ws = new WebSocket("ws://localhost:8007/api/ws");
let receive_audio = false
ws.onmessage = function (event) {
    console.log(typeof event.data)
    console.log(event.data)
    if (receive_audio) {
//            let blob = new Blob(event.data);
            event.type = 'audio/wav';
            recordedAudio.src = URL.createObjectURL(event.data);
            recordedAudio.controls = true;
            recordedAudio.autoplay = true;
            receive_audio = false;
    }
    if (event.data === '<BEGIN_VOICE_MESSAGE_TRANSMISSION>') {
        receive_audio = true;
        return null;
    }
    let messages = document.getElementById('messages')
    let message = document.createElement('li')
    let content = document.createTextNode(event.data)
    message.appendChild(content)
    messages.appendChild(message)
};
function sendMessage(event) {
    let input = document.getElementById("messageText")
    ws.send(input.value)
    input.value = ''
    event.preventDefault()
}

navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => { handlerFunction(stream) })


function handlerFunction(stream) {
    rec = new MediaRecorder(stream);
    rec.ondataavailable = e => {
        audioChunks.push(e.data);
        if (rec.state == "inactive") {
            let blob = new Blob(audioChunks);
            sendData(blob)
        }
    }
}
function sendData(data) {
    console.log('Sending data...')
    ws.send('<BEGIN_VOICE_MESSAGE_TRANSMISSION>')
    // audio_format
    // ws.send(JSON.stringify())
    ws.send(data)

 }

record.onclick = e => {
    console.log('I was clicked')
    record.disabled = true;
    record.style.backgroundColor = "blue"
    stopRecord.disabled = false;
    audioChunks = [];
    rec.start();
}
stopRecord.onclick = e => {
    console.log("I was clicked")
    record.disabled = false;
    stop.disabled = true;
    record.style.backgroundColor = "red"
    rec.stop();
}