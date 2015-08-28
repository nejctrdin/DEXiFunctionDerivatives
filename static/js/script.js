function createAnimation(){
    var fun = JSON.parse(JSON.stringify($("#function").data()));
    var mul = JSON.parse(JSON.stringify($("#multips").data()));
    var args = JSON.parse(JSON.stringify($("#args").data()));
    fun = fun["function"];
    fun = fun.replace(/\(/g, "[")
    fun = fun.replace(/\)/g, "]")
    console.log(fun);
    var arr = JSON.parse(fun);
    var query = {};
    for (i = 0; i < arr.length; i++)
    { 
        console.log(arr[i][1]);
    }
}
