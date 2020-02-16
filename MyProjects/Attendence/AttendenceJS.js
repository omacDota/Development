/* var str = '1 2 3' */

var str = document.getElementById("inptxt").value;
var counter = 0
while (counter !=3000) {
    var temp = str.substring(str.lastIndexOf(" "), str.length);
    counter = counter + 1;
    if (temp == null) {
        console.log("Breaked");
        break;
    }
    console.log(temp);
}


var str = document.getElementById("inptxt").value;
var temp = str.split("\n")
for(i=0;i<temp.length;i++){
    var finalOP = temp[i].substring(temp[i].lastIndexOf(" "), temp[i].length);
    console.log(finalOP);
}

/* var a = ''
while (true) {
    if(a == ''){
        console.log('If Loop');
        break;
    } else {
        console.log('Else Loop');
    }
} */