function submitKeyword() {
    let newKeyword = document.getElementsByName('keyword_input');
    console.log(newKeyword[0].value);
    localStorage.setItem("keyword", newKeyword[0].value);
    let textPopup = document.getElementById("keyword_upload_msg");
    textPopup.setAttribute("class", "w3-show w3-margin");
}

function callTransform() {
    let keywordInput = document.getElementsByName('keyword_input');
    let keywordVal = localStorage.getItem("keyword");
    keywordInput[0].value = keywordVal;
    let smlInput = document.getElementById("textData");
    let smlContent = smlInput.value;
    console.log(keywordVal);
    console.log(smlContent);
    let listAudio = document.getElementById("audioList");
    let itemTemplate = document.getElementById("audioItem");
    let uploadSpinner = document.getElementById("upload_spinner");
    uploadSpinner.setAttribute("class", "spinner-border w3-show");
    fetch('/convert', {
        credentials: 'include',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            {'keyword': keywordVal, 'sml': smlContent}
        )
    }).then(response => response.json())
        .then(async function (result) {
            console.log(result);
            uploadSpinner.setAttribute("class", "spinner-border w3-hide");
            for (let i = 0; i < result.length; i++) {
                let newElement = itemTemplate.cloneNode(true);
                newElement.setAttribute("class", "w3-bar");
                let aud = document.createElement("AUDIO");
                aud.setAttribute("id", result[i]["Link"].replace("https://arxiv.org/abs/", ""));
                aud.setAttribute("src", "/static/audio/" + result[i]["Link"].replace("https://arxiv.org/abs/", "") + ".wav");
                document.body.appendChild(aud);
                let ogHTML = itemTemplate.innerHTML;
                ogHTML = ogHTML.replace("Title", result[i]["Title"]);
                ogHTML = ogHTML.replace("Authors", result[i]["Authors"]);
                ogHTML = ogHTML.replace("Abstract", result[i]["Abstract"]);
                ogHTML = ogHTML.replace("AUDIO", result[i]["Link"].replace("https://arxiv.org/abs/", ""));
                ogHTML = ogHTML.replace("AUDIO", result[i]["Link"].replace("https://arxiv.org/abs/", ""));
                ogHTML = ogHTML.replace("LINK_TO_ARXIV", result[i]["Link"]);
                newElement.innerHTML = ogHTML;
                listAudio.appendChild(newElement);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function playSequentially() {
    let masterAudio = document.getElementById("allAudios");
    if (masterAudio == null) {
        let allAudios = document.getElementsByTagName("audio");
        console.log(allAudios);
        let allSrcs = Array();
        for (let i = 0; i < allAudios.length; i++) {
            allSrcs.push(allAudios[i].getAttribute("src"));
        }
        let audio = new Audio(allSrcs[0]);
        audio.setAttribute("id", "allAudios")

        document.body.appendChild(audio);

        audio.play();

        let index = 1;
        audio.onended = function() {
            if(index < allSrcs.length){
                audio.src=allSrcs[index];
                audio.play();
                index++;
            }
        };
    } else {
        masterAudio.play();
    }

}

function pauseAll() {
    let masterAudio = document.getElementById("allAudios");
    masterAudio.pause();
}