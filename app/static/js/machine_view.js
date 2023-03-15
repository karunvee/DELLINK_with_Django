var plantName = document.getElementById('mcView_plantName').value;
var lineName = document.getElementById('mcView_lineName').value;
var machineName = document.getElementById('mcView_machineName').value;
var ip_port = document.getElementById('mcView_ip_port').value;
var deviceId = document.getElementById('mcView_deviceId').value;

var socket = new WebSocket('ws://localhost:8000/ws/app/');
        first_loading = false;
        socket.onmessage = function(e){
            raw_data = JSON.parse(e.data);
            if(first_loading == false){
                ShowMachineTags(raw_data);
                first_loading = true;
            }
            else{
                UpdateTags(raw_data);
            }
            
        }
        function UpdateTags(data){
            for(let i =0; i < raw_data.length; i++){
                if(raw_data[i]['plant_name'] == plantName ){
                    for(let j=0; j < raw_data[i]['line'].length; j++){

                        if(raw_data[i]['line'][j]['line_name'] == lineName){
                            for(let k=0; k < raw_data[i]['line'][j]['machine'].length; k++){

                                if(raw_data[i]['line'][j]['machine'][k]['machine_name'] == machineName){

                                    var status = document.querySelector('#status');
                                    status.innerHTML = ``;
                                    if(raw_data[i]['line'][j]['machine'][k]['status'] == 1){
                                        status.innerHTML += `<div class="display small Online"><label>Online</label></div>`;
                                    }
                                    else{
                                        status.innerHTML += `<div class="display small Offline"><label>Offline</label></div>`;
                                    }

                                    for(let l=0 ; l < raw_data[i]['line'][j]['machine'][k]['indicator'].length; l++){
                                        var tid = raw_data[i]['line'][j]['machine'][k]['indicator'][l]['tid'];
                                        var val = raw_data[i]['line'][j]['machine'][k]['indicator'][l]['value'];
                                        
                                        // Update value to tags table
                                        var ass_tag = document.getElementById("assTag" + String(tid));
                                        if (ass_tag != null){
                                            ass_tag.value = val;
                                            document.getElementById("btn-assigned" + String(tid)).style.display = "none";
                                            document.getElementById("btn-p-assigned" + String(tid)).style.display = "inline-block";
                                            document.getElementById("btn-deleted" + String(tid)).style.display = "inline-block";
                                        }
                                        document.getElementById("val" + String(tid)).value = val;
                                        //

                                        // Update value to button
                                        var btn_tag = document.getElementById("bTagValue" + String(tid));
                                        if(btn_tag != null){
                                            document.getElementById("bTagValue"+String(tid)).value = val;
                                            const btn = document.querySelector('#btn-TagValue'+String(tid));
                                            if(val == 1){
                                                btn.classList.remove("OFF");
                                                btn.classList.add("ON");
                                            }
                                            else{
                                                btn.classList.remove("ON");
                                                btn.classList.add("OFF");
                                            }
                                        }
                                        //
                                        
                                        // Update value to textbox
                                        var text_tag = document.getElementById("mTagValue" + String(tid));
                                        if(text_tag != null){
                                            if(text_tag !== document.activeElement){
                                                document.getElementById("mTagValue"+String(tid)).value = val;
                                            }
                                        }
                                        //

                                        // Update value to Indicator LED
                                        var indicator_tag = document.getElementById("indicator"+ String(tid))
                                        if (indicator_tag != null){
                                            const ind_show = document.querySelector('#indicator'+String(tid));
                                            if(val == 1){
                                                ind_show.classList.remove("OFF");
                                                ind_show.classList.add("ON");
                                            }
                                            else{
                                                ind_show.classList.remove("ON");
                                                ind_show.classList.add("OFF");
                                            }
                                        }
                                        //

                                        // Update value to STATUS LED
                                        var indicator_status = document.getElementById("indicator-status" + String(tid));
                                        if(indicator_status != null ){
                                                document.getElementById("indicator-status"+String(tid)).value = val;
                                                StatusMachine(val);
                                        }
                                        //

                                        // Update error to notification
                                        var errorCode = document.getElementById("errorCode" + String(tid));
                                        if(errorCode != null){
                                                document.getElementById("errorCode"+String(tid)).value = val;
                                                if(val != 0){
                                                    // document.getElementById('alert-message').style.display = "block";
                                                    var errorMsg = document.getElementById("errorMsg" + String(val));
                                                    if(errorMsg != null){
                                                        var eMsg = document.getElementById("errorMsg" + String(val)).value;
                                                        document.querySelector('#alert-container').innerHTML = `
                                                                    <div class="alert">
                                                                        <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span> 
                                                                        <strong>Error!</strong> ${eMsg}.
                                                                    </div>`;
                                                    }
                                                    else{
                                                        document.querySelector('#alert-container').innerHTML = `
                                                                    <div class="alert">
                                                                        <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span> 
                                                                        <strong>Error!</strong> Unknown error message.
                                                                    </div>`;
                                                    }
                                                    
                                                }
                                                else{
                                                    // document.getElementById('alert-message').style.display = "none";
                                                    document.querySelector('#alert-container').innerHTML = "";
                                                }
                                        }
                                        //
                                    }
                                }   
                            }
                        }
                    }
                }
            }
            
        }

        function ShowMachineTags(data){
            var table = document.querySelector('#table-tag');
            table.innerHTML = "";
            table.innerHTML += `
                            <tr>
                                <th>No.</th>
                                <th>Name</th>
                                <th>Data type</th>
                                <th>Tag ID</th>
                                <th>Register</th>
                                <th>Value</th>
                                <th class="th-indicator">Option</th>
                            </tr>
            `;
            var rowToggle = false;
            for(let i =0; i < raw_data.length; i++){
                if(raw_data[i]['plant_name'] == plantName ){
                    for(let j=0; j < raw_data[i]['line'].length; j++){

                        if(raw_data[i]['line'][j]['line_name'] == lineName){
                            for(let k=0; k < raw_data[i]['line'][j]['machine'].length; k++){

                                if(raw_data[i]['line'][j]['machine'][k]['machine_name'] == machineName){

                                    var status = document.querySelector('#status');
                                    status.innerHTML = ``;
                                    if(raw_data[i]['line'][j]['machine'][k]['status'] == 1){
                                        status.innerHTML += `<div class="display small Online"><label>Online</label></div>`;
                                    }
                                    else{
                                        status.innerHTML += `<div class="display small Offline"><label>Offline</label></div>`;
                                    }

                                    for(let l=0 ; l < raw_data[i]['line'][j]['machine'][k]['indicator'].length; l++){
                                    tid = raw_data[i]['line'][j]['machine'][k]['indicator'][l]['tid'];
                                    tag_name = raw_data[i]['line'][j]['machine'][k]['indicator'][l]['indicator_name'];
                                    
                                    newRow = "";
                                    if(rowToggle){
                                        newRow += `<tr class="tags-members color">`;
                                    }
                                    else{
                                        newRow += `<tr class="tags-members">`;
                                    }
                                    rowToggle = !rowToggle;
                                    newRow +=`
                                            <td>${l}</td>
                                            <td>${raw_data[i]['line'][j]['machine'][k]['indicator'][l]['indicator_name']}<input id="name${tid}" value="${raw_data[i]['line'][j]['machine'][k]['indicator'][l]['indicator_name']}" hidden/></td>
                                            <td>${raw_data[i]['line'][j]['machine'][k]['indicator'][l]['gp']}</td>
                                            <td>${tid}</td>
                                            <td>${raw_data[i]['line'][j]['machine'][k]['indicator'][l]['register']}<input id="reg${tid}" value="${raw_data[i]['line'][j]['machine'][k]['indicator'][l]['register']}" hidden/></td>
                                            <td><input id="val${tid}" class="tag-value" value="${raw_data[i]['line'][j]['machine'][k]['indicator'][l]['value']}" disabled/></td>
                                            <td class="td-indicator">
                                                <button id="btn-assigned${tid}" class="btn-assigned" onclick="openForm(${tid})">Unassigned</button>
                                                <button id="btn-p-assigned${tid}" class="btn-p-assigned" onclick="" style="display: none; background-color: #ccc; cursor: default;" disabled>&ensp;&nbsp;Assigned&ensp;</button>
                                                <button class="btn-tag-write" id='WriteData' onclick="WriteData(${tid})">Write Data</button>
                                                <input class="tag-add-value" id="TagValue${tid}"/>
                                                <button id="btn-deleted${tid}" class="btn-deleted" onclick="deleteForm(${tid}, '${tag_name}')" style="display: none; background-color: rgb(211, 51, 51); margin-left: 2px;"><i class='bx bx-trash' ></i></button>
                                            </td>
                                        </tr>
                                    `;

                                    table.innerHTML += newRow;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        function deleteForm(tid, tag_name){
            // Appearance Comfirm Form
            document.getElementById('confirmForm').style.display = "block";
            document.querySelector('#confirmForm').innerHTML = 
            `<div class="8">
                <div class="confirmForm-content">
                    <h1>Question ?</h1>
                    <p>Are you sure you want to delete this indicator id : <strong>${tid}</strong>, name : <strong>${tag_name}</strong> ?</p>
                    <hr>
                    <div class="clearfix">
                        <button class="btn-delete yes" onclick="location.href='/delete_indicator/pt${plantName}ln{{lineName}}mc{{machineName}}tid${tid}/';">Yes, I'm sure</button>
                        <button class="btn-delete no" type="button" onclick="document.getElementById('confirmForm').style.display='none'">No</button>
                    </div>
                </div>
            </div>`;
        }
        function showAddCameraForm(){
            document.getElementById('add-camera-form').style.display = "block";
            // document.querySelector('#add-camera-form').innerHTML = ``;
        }

        function openDIAPage(url){
            window.open(url, "DIA Link web","width=1000,height=600");
        }

        function openForm(tid) {
            document.getElementById('tagName').value = document.getElementById("name" + tid).value;

            document.getElementById('register').value = document.getElementById("reg" + tid).value;

            document.getElementById('tagID').innerText = tid;
            document.getElementById('tagID').value = tid;

            //>>> Appearance Assignment Form
            document.getElementById('assignForm').style.display = "block";
            //<<<

            //>>> clear
            document.getElementById("data_type").value = "";
            document.getElementById('datatype_bit').style.display = "none";
            document.getElementById('datatype_text').style.display = "none";
            document.getElementById('btn-add').style.display = "none";
            //<<<
        }



        //>>> Login to get tokenID
        var details = {
            'username': 'root',
            'password': 'admin',
        };
        var formBody  = [];
        for (var property in details) {
          var encodedKey = encodeURIComponent(property);
          var encodedValue = encodeURIComponent(details[property]);
          formBody.push(encodedKey + "=" + encodedValue);
        }
        formBody = formBody.join("&");

        fetch(ip_port + 'api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Content-Length': 0,
        },
        body: formBody,
        })
        .then((response) => response.json())
        .then((data) => {
            console.log('Success:', data);
            token_ = data.access_token ;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
        //<<<

        //>>> Write Data Registor
        function WriteData(tag_id, tg = 0){
            // $("body").css("cursor", "progress");
            console.log("token :" + token_);
            if (token_ == ""){
                alert("Authorization error : Token is empty!!");
            }
            else{
                switch(tg){
                    case 1:
                        var tag_value = document.getElementById("mTagValue"+tag_id).value;
                        break;
                    case 2:
                        var tag_value = document.getElementById("bTagValue"+tag_id).value;
                        tag_value = 1 - tag_value ;
                        break;
                    default:
                        var tag_value = document.getElementById("TagValue"+tag_id).value;
                        document.getElementById("TagValue"+tag_id).value = "";
                }
                let url_api = ip_port + 'api/v1/devices/'+ deviceId +'/tags/'+ String(tag_id) +'/value/' + tag_value;
                const initDetails = {
                method: 'PUT',
                headers: {
                    'Content-Length': 0,
                    'Authorization': "Bearer " + token_
                },
                }
                fetch(url_api,initDetails).then( response =>
                    {
                        if ( response.status == 401 )
                        {
                            console.log('Status Code: 401 Unauthorized');
                            alert('Status Code: 401 Unauthorized');
                            return;
                        }
                        // else if(response.status != 204)
                        else{
                            let msg = 'Value :' + tag_value + ', Tag ID :' + tag_id + ', Status Code: ' + response.status;
    
                            console.log(msg);
                            alert(msg);
                            return;
                        }
                        // alert('Write the value success!');
                        console.log( response.headers.get( "Content-Type" ) );
                        return 0;
                    }
                    )
            }
            // $("body").css("cursor", "default");
        }
        //<<<

        //>>> On Assignment data was changed
        const getDataType = () =>{
            let inputValue = document.getElementById("data_type").value; 
            if(inputValue == "BIT"){
                document.getElementById('datatype_bit').style.display = "block";
                document.getElementById('datatype_text').style.display = "none";
                document.getElementById('btn-add').style.display = "block";
            }
            else if(inputValue == ""){
                alert("Please select the data type");
                document.getElementById('datatype_bit').style.display = "none";
                document.getElementById('datatype_text').style.display = "none";
                document.getElementById('btn-add').style.display = "none";
            }
            else if(inputValue == "STATUS" || inputValue == "ERROR CODE"){
                document.getElementById('datatype_bit').style.display = "none";
                document.getElementById('datatype_text').style.display = "none";
                document.getElementById('btn-add').style.display = "block";
            }
            else{
                document.getElementById('datatype_bit').style.display = "none";
                document.getElementById('datatype_text').style.display = "block";
                document.getElementById('btn-add').style.display = "block";
            }
        }
        //<<<

        //>>> LED Status 
        p_val = "";
        function StatusMachine(val){
            const sg = document.querySelector('#status-green');
            const sy = document.querySelector('#status-yellow');
            const sr = document.querySelector('#status-red');
            if( val != p_val){
                switch (val){
                    case "0":
                        document.getElementById("text-indicator-status").innerText = "Normal";
                        sg.classList.remove("green");
                        sy.classList.remove("yellow");
                        sr.classList.remove("red");
                        sg.classList.add("green");
                        break;
                    case "1":
                        document.getElementById("text-indicator-status").innerText = "Error";
                        sg.classList.remove("green");
                        sy.classList.remove("yellow");
                        sr.classList.remove("red");
                        sr.classList.add("red");
                        break;
                    case "2":
                        document.getElementById("text-indicator-status").innerText = "Pause";
                        sg.classList.remove("green");
                        sy.classList.remove("yellow");
                        sr.classList.remove("red");
                        sy.classList.add("yellow");
                        break;
                    case "3":
                        document.getElementById("text-indicator-status").innerText = "standby";
                        sg.classList.remove("green");
                        sy.classList.remove("yellow");
                        sr.classList.remove("red");
                        sy.classList.add("yellow");
                        break;
                    case "4":
                        document.getElementById("text-indicator-status").innerText = "Wait for material";
                        sg.classList.remove("green");
                        sy.classList.remove("yellow");
                        sr.classList.remove("red");
                        sy.classList.add("yellow");
                        break;
                    case "5":
                        document.getElementById("text-indicator-status").innerText = "Output full material";
                        sg.classList.remove("green");
                        sy.classList.remove("yellow");
                        sr.classList.remove("red");
                        sy.classList.add("yellow");
                        break;
                    case "6":
                        document.getElementById("text-indicator-status").innerText = "Material low";
                        sg.classList.remove("green");
                        sy.classList.remove("yellow");
                        sr.classList.remove("red");
                        sy.classList.add("yellow");
                        break;
                    case "7":
                        document.getElementById("text-indicator-status").innerText = "Change line";
                        sg.classList.remove("green");
                        sy.classList.remove("yellow");
                        sr.classList.remove("red");
                        sy.classList.add("yellow");
                        break;
                    default:
                        document.getElementById("text-indicator-status").innerText = "Unknown";
                        sg.classList.remove("green");
                        sy.classList.remove("yellow");
                        sr.classList.remove("red");
                        break;
                }
            }
            p_val = val;
            
        }
        //<<<<.