const modal = document.getElementById("myModal");
const btn = document.getElementById("myBtn");
const span = document.getElementsByClassName("close")[0];
const inputList = document.getElementById("inputList");

btn.onclick = function() {
    modal.style.display = "block";
};

span.onclick = function() {
    location.reload();
};

window.onclick = function(event) {
    if (event.target === modal) {
        location.reload();
    }
};

function sendRequest(){
    const request = new XMLHttpRequest();
    const data = findAllInputs();
    request.open("POST","/predict");
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.onreadystatechange = function() {
        if (request.readyState === 4) {
            console.log(request.response)
            $(".from").empty();
            $(".modal-content").css("height", "12%");
            $(".modal-content").css("overflow", "hidden");
            if(request.response === "True"){
                $(".oui").show()
            }else{
                $(".non").show()
            }
        }
    };
    request.send(JSON.stringify(data))
}

function findAllInputs(){
    let all = Array.from(inputList.getElementsByTagName("input"));
    all = all.concat(Array.from(inputList.getElementsByTagName("select")));
    let obj = {};
    for (let i = 0; i < all.length; i++) {
        obj[all[i].name] = all[i].value;
    }
    return obj
}
