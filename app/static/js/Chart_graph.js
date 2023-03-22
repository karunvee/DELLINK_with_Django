
function startTime() {
    if(timeReset.getTime() < today.getTime()){
        timeReset = new Date();
        timeReset.setHours(7, 30, 0, 0);
        timeStart = new Date();
        timeStart.setHours(7, 30, 0, 0);
        console("Reset time!!\n Start Time: "+ timeStart + "\n Reset Time: " + timeReset);
    }
    const today = new Date();
    let d = today.getDate();
    let M = today.getMonth() + 1;
    let y = today.getFullYear();
    let h = today.getHours();
    let m = today.getMinutes();
    let s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('clock-time').innerHTML =  d + "/" + M + "/"+ y + " - " +h + ":" + m + ":" + s;
    setTimeout(startTime, 1000);
  }
  
  function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
  }


function updateErrorTable(rw){
    var raw = rw[0]["error-history"];
    var errorTable = document.getElementById("table-error");

    errorTable.innerHTML = `
    <thead>
        <tr>
            <th class="error-header-date">Date/Time</th>
            <th class="error-header-code">ErrorCode</th>
            <th class="error-header-des">Description</th>
            <th class="error-header-counter">Counter</th>
            <th class="error-header-addi">additional</th>
        </tr>
    </thead>`;

    // errorTable.innerHTML = "";
    for(let i =0; i < raw.length; i++){
        if(plantName == raw[i]["plant_name"] && lineName == raw[i]["line_name"] && machineName == raw[i]["machine_name"]){
            var new_row = errorTable.insertRow(1);
            var date_cell = new_row.insertCell(0);
            var errorCode_cell = new_row.insertCell(1);
            var des_cell = new_row.insertCell(2);
            var count_cell = new_row.insertCell(3);
            var add_cell = new_row.insertCell(4);
            date_cell.innerHTML = raw[i]["datetime"].split('.')[0];
            errorCode_cell.innerHTML = raw[i]["error_code"];
            des_cell.innerHTML = raw[i]["error_message"];
            count_cell.innerHTML = "999";
            add_cell.innerHTML = "";
        }
        
    }
}

