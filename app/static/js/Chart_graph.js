const timelineContainer = document.querySelector('.timeline');
var toggleAutoFollowTimeline = true;
function initialPage(){
    startTime();
    timelineContainer.scrollTo(timelineContainer.scrollWidth, 0);
}

function DateTimeFormat(datetime){
    const dt = new Date(datetime);

    let d = dt.getDate();
    let M = dt.getMonth() + 1;
    let y = dt.getFullYear();
    let h = dt.getHours();
    let m = dt.getMinutes();
    let s = dt.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    datetime_txt = d + "/" + M + "/"+ y + " - " +h + ":" + m + ":" + s;
    return datetime_txt;
}

function startTime() {

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
    widthTimeline = 4000;
    timelineContainer.scrollTo(timelineContainer.scrollWidth, 0);
}
function zoominTimeline(){
    widthTimeline = widthTimeline * 2;
}
function zoomoutTimeline(){
    widthTimeline = widthTimeline / 2;
}
function tonowTimeline(){
    timelineContainer.scrollTo(timelineContainer.scrollWidth, 0);
}
function autofollowTimeline(){
    const autofollow_btn = document.getElementById('autofollow_btn');
    autofollow_btn.classList.toggle("on");
    toggleAutoFollowTimeline = !toggleAutoFollowTimeline;
}


