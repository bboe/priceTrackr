//httprequest
var xmlhttp=false;
/*@cc_on @*/
/*@if (@_jscript_version >= 5)
// JScript gives us Conditional compilation, we can cope with old IE versions.
// and security blocked creation of the objects.
 try {
  xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
 } catch (e) {
  try {
   xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
  } catch (E) {
   xmlhttp = false;
  }
 }
 @end @*/
if (!xmlhttp && typeof XMLHttpRequest!='undefined') {
    try {
	xmlhttp = new XMLHttpRequest();
    } catch (e) {
	xmlhttp=false;
    }
}
if (!xmlhttp && window.createRequest) {
    try {
	xmlhttp = window.createRequest();
    } catch (e) {
	xmlhttp=false;
    }
}
//astrack
function track_click () {
    xmlhttp.open("HEAD", "/naive_click_tracking.png", false);
    xmlhttp.send(null);
}

// incredibly funky onload add-event scripting, for all browsers

		 if(typeof window.addEventListener != 'undefined')
		 {
		 	//.. gecko, safari, konqueror and standard
		 	window.addEventListener('load', adsense_init, false);
		 }
		 else if(typeof document.addEventListener != 'undefined')
		 {
		 	//.. opera 7
		 	document.addEventListener('load', adsense_init, false);
		 }
		 else if(typeof window.attachEvent != 'undefined')
		 {
		 	//.. win/ie
		 	window.attachEvent('onload', adsense_init);
		 }

		 //** remove this condition to degrade older browsers
		 else
		 {
		 	//.. mac/ie5 and anything else that gets this far

		 	//if there's an existing onload function
		 	if(typeof window.onload == 'function')
		 	{
		 		//store it
		 		var existing = onload;

		 		//add new onload handler
		 		window.onload = function()
		 		{
		 			//call existing onload function
		 			existing();

		 			//call adsense_init onload function
		 			adsense_init();
		 		};
		 	}
		 	else
		 	{
		 		//setup onload function
		 		window.onload = adsense_init;
		 	}
		 }
function adsense_init () {

	if (document.all) {  //ie
		var el = document.getElementsByTagName("iframe");
	
		for(var i = 0; i < el.length; i++) {
			if(el[i].src.indexOf('sample.html') > -1) {

				el[i].onfocus =  track_click;
			}
		}
	
	} else {   // firefox
		window.addEventListener('beforeunload', doPageExit, false);
		window.addEventListener('mousemove', getMouse, true);
	
	}
		
}

//for firefox
var px;
var py;

function getMouse(e) {
	px=e.pageX;
	py=e.clientY;
}

function findY(obj) {
	var y = 0;
	while (obj) {
		y += obj.offsetTop;
		obj = obj.offsetParent;
	}
	return(y);
}

function findX(obj) {
	var x = 0;
	while (obj) {
		x += obj.offsetLeft;
		obj = obj.offsetParent;
	}
	return(x);
}

function doPageExit(e) {
	ad = document.getElementsByTagName("iframe");
	for (i=0; i<ad.length; i++) {
		var adLeft = findX(ad[i]);
		var adTop = findY(ad[i]);
		var inFrameX = (px > (adLeft - 10) && px < (parseInt(adLeft) + parseInt(ad[i].width) + 15));
		var inFrameY = (py > (adTop - 10) && py < (parseInt(adTop) + parseInt(ad[i].height) + 10));
		
		if (inFrameY && inFrameX) {
		    track_click()
		}
	}

}
// niftycube
var niftyOk=(document.getElementById&&document.createElement&&Array.prototype.push);var niftyCss=false;String.prototype.find=function(what){return(this.indexOf(what)>=0?true:false);}
var oldonload=window.onload;if(typeof(NiftyLoad)!='function')NiftyLoad=function(){};if(typeof(oldonload)=='function')
window.onload=function(){oldonload();AddCss();NiftyLoad()};else window.onload=function(){AddCss();NiftyLoad()};function AddCss(){niftyCss=true;var l=CreateEl("link");l.setAttribute("type","text/css");l.setAttribute("rel","stylesheet");l.setAttribute("href","/style/niftyCorners.css");l.setAttribute("media","screen");document.getElementsByTagName("head")[0].appendChild(l);}
function Nifty(selector,options){if(niftyOk==false)return;if(niftyCss==false)AddCss();var i,v=selector.split(","),h=0;if(options==null)options="";if(options.find("fixed-height"))
h=getElementsBySelector(v[0])[0].offsetHeight;for(i=0;i<v.length;i++)
Rounded(v[i],options);if(options.find("height"))SameHeight(selector,h);}
function Rounded(selector,options){var i,top="",bottom="",v=new Array();if(options!=""){options=options.replace("left","tl bl");options=options.replace("right","tr br");options=options.replace("top","tr tl");options=options.replace("bottom","br bl");options=options.replace("transparent","alias");if(options.find("tl")){top="both";if(!options.find("tr"))top="left";}
else if(options.find("tr"))top="right";if(options.find("bl")){bottom="both";if(!options.find("br"))bottom="left";}
else if(options.find("br"))bottom="right";}
if(top==""&&bottom==""&&!options.find("none")){top="both";bottom="both";}
v=getElementsBySelector(selector);for(i=0;i<v.length;i++){FixIE(v[i]);if(top!="")AddTop(v[i],top,options);if(bottom!="")AddBottom(v[i],bottom,options);}}
function AddTop(el,side,options){var d=CreateEl("b"),lim=4,border="",p,i,btype="r",bk,color;d.style.marginLeft="-"+getPadding(el,"Left")+"px";d.style.marginRight="-"+getPadding(el,"Right")+"px";if(options.find("alias")||(color=getBk(el))=="transparent"){color="transparent";bk="transparent";border=getParentBk(el);btype="t";}
else{bk=getParentBk(el);border=Mix(color,bk);}
d.style.background=bk;d.className="niftycorners";p=getPadding(el,"Top");if(options.find("small")){d.style.marginBottom=(p-2)+"px";btype+="s";lim=2;}
else if(options.find("big")){d.style.marginBottom=(p-10)+"px";btype+="b";lim=8;}
else d.style.marginBottom=(p-5)+"px";for(i=1;i<=lim;i++)
d.appendChild(CreateStrip(i,side,color,border,btype));el.style.paddingTop="0";el.insertBefore(d,el.firstChild);}
function AddBottom(el,side,options){var d=CreateEl("b"),lim=4,border="",p,i,btype="r",bk,color;d.style.marginLeft="-"+getPadding(el,"Left")+"px";d.style.marginRight="-"+getPadding(el,"Right")+"px";if(options.find("alias")||(color=getBk(el))=="transparent"){color="transparent";bk="transparent";border=getParentBk(el);btype="t";}
else{bk=getParentBk(el);border=Mix(color,bk);}
d.style.background=bk;d.className="niftycorners";p=getPadding(el,"Bottom");if(options.find("small")){d.style.marginTop=(p-2)+"px";btype+="s";lim=2;}
else if(options.find("big")){d.style.marginTop=(p-10)+"px";btype+="b";lim=8;}
else d.style.marginTop=(p-5)+"px";for(i=lim;i>0;i--)
d.appendChild(CreateStrip(i,side,color,border,btype));el.style.paddingBottom=0;el.appendChild(d);}
function CreateStrip(index,side,color,border,btype){var x=CreateEl("b");x.className=btype+index;x.style.backgroundColor=color;x.style.borderColor=border;if(side=="left"){x.style.borderRightWidth="0";x.style.marginRight="0";}
else if(side=="right"){x.style.borderLeftWidth="0";x.style.marginLeft="0";}
return(x);}
function CreateEl(x){return(document.createElement(x));}
function FixIE(el){if(el.currentStyle!=null&&el.currentStyle.hasLayout!=null&&el.currentStyle.hasLayout==false)
el.style.display="inline-block";}
function SameHeight(selector,maxh){var i,v=selector.split(","),t,j,els=[],gap;for(i=0;i<v.length;i++){t=getElementsBySelector(v[i]);els=els.concat(t);}
for(i=0;i<els.length;i++){if(els[i].offsetHeight>maxh)maxh=els[i].offsetHeight;els[i].style.height="auto";}
for(i=0;i<els.length;i++){gap=maxh-els[i].offsetHeight;if(gap>0){t=CreateEl("b");t.className="niftyfill";t.style.height=gap+"px";nc=els[i].lastChild;if(nc.className=="niftycorners")
els[i].insertBefore(t,nc);else els[i].appendChild(t);}}}
function getElementsBySelector(selector){var i,j,selid="",selclass="",tag=selector,tag2="",v2,k,f,a,s=[],objlist=[],c;if(selector.find("#")){if(selector.find(" ")){s=selector.split(" ");var fs=s[0].split("#");if(fs.length==1)return(objlist);f=document.getElementById(fs[1]);if(f){v=f.getElementsByTagName(s[1]);for(i=0;i<v.length;i++)objlist.push(v[i]);}
return(objlist);}
else{s=selector.split("#");tag=s[0];selid=s[1];if(selid!=""){f=document.getElementById(selid);if(f)objlist.push(f);return(objlist);}}}
if(selector.find(".")){s=selector.split(".");tag=s[0];selclass=s[1];if(selclass.find(" ")){s=selclass.split(" ");selclass=s[0];tag2=s[1];}}
var v=document.getElementsByTagName(tag);if(selclass==""){for(i=0;i<v.length;i++)objlist.push(v[i]);return(objlist);}
for(i=0;i<v.length;i++){c=v[i].className.split(" ");for(j=0;j<c.length;j++){if(c[j]==selclass){if(tag2=="")objlist.push(v[i]);else{v2=v[i].getElementsByTagName(tag2);for(k=0;k<v2.length;k++)objlist.push(v2[k]);}}}}
return(objlist);}
function getParentBk(x){var el=x.parentNode,c;while(el.tagName.toUpperCase()!="HTML"&&(c=getBk(el))=="transparent")
el=el.parentNode;if(c=="transparent")c="#FFFFFF";return(c);}
function getBk(x){var c=getStyleProp(x,"backgroundColor");if(c==null||c=="transparent"||c.find("rgba(0, 0, 0, 0)"))
return("transparent");if(c.find("rgb"))c=rgb2hex(c);return(c);}
function getPadding(x,side){var p=getStyleProp(x,"padding"+side);if(p==null||!p.find("px"))return(0);return(parseInt(p));}
function getStyleProp(x,prop){if(x.currentStyle)
return(x.currentStyle[prop]);if(document.defaultView.getComputedStyle)
return(document.defaultView.getComputedStyle(x,'')[prop]);return(null);}
function rgb2hex(value){var hex="",v,h,i;var regexp=/([0-9]+)[, ]+([0-9]+)[, ]+([0-9]+)/;var h=regexp.exec(value);for(i=1;i<4;i++){v=parseInt(h[i]).toString(16);if(v.length==1)hex+="0"+v;else hex+=v;}
return("#"+hex);}
function Mix(c1,c2){var i,step1,step2,x,y,r=new Array(3);if(c1.length==4)step1=1;else step1=2;if(c2.length==4)step2=1;else step2=2;for(i=0;i<3;i++){x=parseInt(c1.substr(1+step1*i,step1),16);if(step1==1)x=16*x+x;y=parseInt(c2.substr(1+step2*i,step2),16);if(step2==1)y=16*y+y;r[i]=Math.floor((x*50+y*50)/100);r[i]=r[i].toString(16);if(r[i].length==1)r[i]="0"+r[i];}
return("#"+r[0]+r[1]+r[2]);}
