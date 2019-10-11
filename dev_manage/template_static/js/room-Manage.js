var Xcoord = 0;
var Ycoord = 0;
var mouseX;
var mouseY;
var original_X;
var original_Y;

document.addEventListener("dragstart", function(event) {
    //dataTransfer.setData()方法设置数据类型和拖动的数据
	var e = event;

    event.dataTransfer.setData("Text", event.target.id);

    mouseOver(event);

    Xcoord = mouseX;
    Ycoord = mouseY;

    var temp_Left = document.getElementById("test").style.marginLeft;
    var temp_Top = document.getElementById("test").style.marginTop;

    if(temp_Left!=="")
    {
       original_X = parseInt(temp_Left);
       original_Y = parseInt(temp_Top);
    }
    else
    {
       original_X = 0;
       original_Y = 0;
    }

    document.getElementById("before_text").innerHTML = "Before Mouse: ( " + Xcoord + "px , " + Ycoord + "px )";
    document.getElementById("before_margin_text").innerHTML = "Before Margin: ( " + original_X + "px , " + original_Y + "px )";
    // 拖动 p 元素时输出一些文本
    //document.getElementById("test").innerHTML =  e.screenY + "px";

    //修改拖动元素的透明度
    //event.target.style.opacity = "0.2";
});

document.addEventListener("dragend", function(event) {
    //dataTransfer.setData()方法设置数据类型和拖动的数据
	var e = event;
    mouseOver(event);

    var testDiv = document.getElementById("test");

    var offert_x = mouseX - Xcoord;
    var offert_y = mouseY - Ycoord;

    var temp_X = original_X + offert_x;
    var temp_Y = original_Y + offert_y;

    testDiv.style.marginLeft = temp_X + 'px';
    testDiv.style.marginTop = temp_Y + 'px';

    document.getElementById("after_text").innerHTML = "After Mouse: ( " + mouseX + "px , " + mouseY + "px )";
    document.getElementById("after_margin_text").innerHTML = "After Margin: ( " + temp_X + "px , " + temp_Y + "px )";

    document.getElementById("offset_text").innerHTML = "Offset: ( " + offert_x + "px , " + offert_y + "px )";
    document.getElementById("test").innerHTML = "X:" + testDiv.style.marginLeft + "px; Y:" + testDiv.style.marginTop + "px";


    //修改拖动元素的透明度
});

function mouseOver(obj){
    e = obj || window.event;

    mouseX = e.layerX||e.offsetX;
    mouseY = e.layerY||e.offsetY;
};

//function show(event) {
//
// mouseOver(event);
//  document.getElementById("test").innerHTML = mouseX+" "+mouseY ;
//};