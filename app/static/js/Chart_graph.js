const timelineContainer = document.querySelector('.timeline');
var toggleAutoFollowTimeline = true;
function initialPage(){
    startTime();
    timelineContainer.scrollTo(timelineContainer.scrollWidth, 0);
}

function startTime() {

    const today = new Date();
    // if(timeReset.getTime() < today.getTime()){
    //     timeReset = new Date();
    //     timeReset.setHours(7, 30, 0, 0);
    //     timeStart = new Date();
    //     timeStart.setHours(7, 30, 0, 0);
    //     console("Reset time!!\n Start Time: "+ timeStart + "\n Reset Time: " + timeReset);
    // }
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
    var index = Math.ceil( (today.getTime() - timeStart.getTime())/(60*1000) );

    document.getElementById('timeline').style.width = `${widthTimeline + index}px`;
    if(toggleAutoFollowTimeline){
        timelineContainer.scrollTo(timelineContainer.scrollWidth, 0);
    }
  }
  function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
  }
function refreshTimeline(){
    widthTimeline = 1500;
    timelineContainer.scrollTo(timelineContainer.scrollWidth, 0);
    updateTimeline(raw_data_error);
}
function zoominTimeline(){
    widthTimeline = widthTimeline * 2;
    updateTimeline(raw_data_error);
}
function zoomoutTimeline(){
    widthTimeline = widthTimeline / 2;
    updateTimeline(raw_data_error);
}
function tonowTimeline(){
    timelineContainer.scrollTo(timelineContainer.scrollWidth, 0);
}
function autofollowTimeline(){
    const autofollow_btn = document.getElementById('autofollow_btn');
    autofollow_btn.classList.toggle("on");
    toggleAutoFollowTimeline = !toggleAutoFollowTimeline;
}


