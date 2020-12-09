/**
 * blowup.min.js
 * Paul Krishnamurthy 2016
 *
 * https://paulkr.com
 * paul@paulkr.com
 */

$(function(a){a.fn.blowup=function(b){var c=this;if(!c.is("img"))return void console.log("%c Blowup.js Error: %cTarget element is not an image.","background: #FCEBB6; color: #F07818; font-size: 17px; font-weight: bold;","background: #FCEBB6; color: #F07818; font-size: 17px;");var d=c.attr("src"),g=(c.width(),c.height(),new Image);g.src=c.attr("src");var h={round:!0,width:200,height:200,background:"#FFF",shadow:"0 8px 17px 0 rgba(0, 0, 0, 0.2)",border:"6px solid #FFF",cursor:!0,zIndex:999999,scale:1},i=a.extend(h,b);c.on("dragstart",function(a){a.preventDefault()}),c.css("cursor",i.cursor?"crosshair":"none");var j=document.createElement("div");j.id="BlowupLens",a("body").append(j),$blowupLens=a("#BlowupLens"),$blowupLens.css({position:"absolute",visibility:"hidden","pointer-events":"none",zIndex:i.zIndex,width:i.width,height:i.height,border:i.border,background:i.background,"border-radius":i.round?"50%":"none","box-shadow":i.shadow,"background-repeat":"no-repeat"}),c.mouseenter(function(){$blowupLens.css("visibility","visible")}),c.mousemove(function(b){var e=b.pageX-i.width/2,f=b.pageY-i.height/2,h=b.pageX-a(this).offset().left,j=b.pageY-a(this).offset().top,k=-Math.floor(h/c.width()*(g.width*i.scale)-i.width/2),l=-Math.floor(j/c.height()*(g.height*i.scale)-i.height/2),m=k+"px "+l+"px",n=g.width*i.scale+"px "+g.height*i.scale+"px";$blowupLens.css({left:e,top:f,"background-image":"url("+d+")","background-size":n,"background-position":m})}),c.mouseleave(function(){$blowupLens.css("visibility","hidden")})}});
