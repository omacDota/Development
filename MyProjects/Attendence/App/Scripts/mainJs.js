function Calc() {
    if (document.getElementById("inptxt").value == '') {
        alert("Please Enter Attendence")
    } else {
        var temp;
		var temp_1;
        var sum;
        var l_counter = 0;
        try {
            sum = 0;
            var str = document.getElementById("inptxt").value;
            temp = str.split("\n");

            for (i = 0; i < temp.length; i++) {
                var finalOP = temp[i].substring(temp[i].lastIndexOf("\t"), temp[i].length);
				temp_1 = finalOP.split(".");
                
                if(temp_1[0] != 0 && temp_1[1] != 0){
                    hrs = temp_1[0] * 3600000 
                    min = temp_1[1] * 60000

                    //console.log(finalOP);
                    //console.log(hrs)
                    //console.log(min)

                    sum = sum + parseInt(hrs) + parseInt(min);
                    l_counter ++;
                }
                else {
                    continue;
                }
            }
            console.log(sum);
        } catch (error) {
            console.log(error);
        } finally {
            document.getElementById("SolutionDiv").style.display = "block";


            console.log("Sum :" + sum/3600000);
            document.getElementById("Sum").value = "Sum : " + sum/3600000+" hrs";

            var Average = sum / (l_counter);
            console.log("Average :" + Average/3600000);
            document.getElementById("Average").value = "Average : " + Average/3600000 +" hrs";

            var Hours = sum - (l_counter*3600000* 9);
            console.log("Hours : " + Hours/3600000);

            if (Hours/3600000 >= 0) {
                console.log("Extra Hours : " + Hours/3600000)
                document.getElementById("SolutionDiv").style.borderColor = "darkgreen";
                document.getElementById("ThirdElementTB").value = "Extra Hours : " + Hours/3600000 +" hrs";
            } else {
                console.log("OverDue Hours : " + Math.abs(Hours/3600000))
                document.getElementById("SolutionDiv").style.borderColor = "brown";
                document.getElementById("ThirdElementTB").value = "OverDue Hours : " + Math.abs(Hours)/3600000 +" hrs";
            }
        }
    }

}