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

    //修改拖动元素的透明度
    //event.target.style.opacity = "0.2";
});

// 元素离开drop_div盒子后的处理
document.addEventListener("dragleave",function(event){
    if(event.target.className == "drop_div"){
        event.target.style.border = "1px solid";
    }
});

// 当被拖对象(node_cell)开始进入经过对象(drop_div)时触发,evnet指向的是经过对象drop_div
document.addEventListener("dragenter", function(event) {
    if ( event.target.className == "drop_div" ) {
        event.target.style.border = "2px dotted";
    }
});

// 当被拖对象(node_cell)在经过对象(drop_div)中移动时触发,evnet指向的是经过对象drop_div
// 默认情况下,数据/元素不能在其他元素中被拖放。对于drop我们必须防止元素的默认处理
document.addEventListener("dragover",function(event){
    event.preventDefault();
});

// 被拖对象被拖放在目标元素(drop_div)中放下时触发,event指向的就是目标元素(drop_div)
document.addEventListener("drop",function(event){
    event.preventDefault();

    if(event.target.className=="drop_div")
    {
        event.target.style.border = "1px solid";

        var data = event.dataTransfer.getData("Text");
        event.target.appendChild(document.getElementById(data));
    }

});