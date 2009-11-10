var xmlhttp = false;
if(window.XMLHttpRequest)
    xmlhttp = new XMLHttpRequest();
else if(window.ActiveXObject)
    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
function track_click() {
    if (xmlhttp) {
	xmlhttp.open("HEAD", "/naive_click_tracking", false);
	xmlhttp.send(null);
	//alert('Click recorded');
    }
}
if(typeof window.addEventListener != "undefined")
    window.addEventListener("load", track_init, false);
else if(typeof document.addEventListener != "undefined")
    document.addEventListener("load", track_init, false);
else if(typeof window.attachEvent != "undefined")
    window.attachEvent("onload", track_init);
function track_init() {
    if(document.all) {
	var el = document.getElementsByTagName("iframe");
	for(var i = 0; i < el.length; i++)
	    if(el[i].src.indexOf("pagead2.googlesyndication.com") > - 1)
		el[i].onfocus = track_click;
    }
    else {
	window.addEventListener("beforeunload", doPageExit, false);
	window.addEventListener("mousemove", getMouse, true);
    }
}
var px;
var py;
function getMouse(e) {
    px = e.pageX;
    py = e.clientY;
}
function findY(obj) {
    var y = 0;
    while(obj) {
	y += obj.offsetTop;
	obj = obj.offsetParent;
    }
    return y;
}
function findX(obj) {
    var x = 0;
    while(obj) {
	x += obj.offsetLeft;
	obj = obj.offsetParent;
    }
    return x;
}
function doPageExit(e) {
    ad = document.getElementsByTagName("iframe");
    for(i = 0; i < ad.length; i++) {
	var adLeft = findX(ad[i]);
	var adTop = findY(ad[i]);
	var inFrameX = px > adLeft - 10 && px < parseInt(adLeft) + parseInt(ad[i].width) + 15;
	var inFrameY = py > adTop - 10 && py < parseInt(adTop) + parseInt(ad[i].height) + 10;
	if(inFrameY && inFrameX)
	    track_click();
    }
}
