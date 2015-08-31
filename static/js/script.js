function createAnimation()
{
    var fun = JSON.parse(JSON.stringify($("#function").data()));
    fun = fun["function"];
    fun = fun.replace(/\(/g, "[");
    fun = fun.replace(/\)/g, "]");
    var arr = JSON.parse(fun);
    var query = {};
    for (i = 0; i < arr.length; i++)
    {
        query["v"+i] = arr[i][1];
    }

    var mul = JSON.parse(JSON.stringify($("#multips").data()));
    query["multiplicity"] = mul["multiplicities"];
    var args = JSON.parse(JSON.stringify($("#args").data()));
    args = args["arguments"];
    args = args.replace(/u'/g, "'");
    args = args.replace(/'/g, "");
    args = args.replace(/\[/g, "");
    args = args.replace(/\]/g, "");
    args = args.replace(/ /g, "");
    query["names"] = args;

    $.ajax({
        type: "POST",
        async: true,
        url: "/get_animation",
        data:  query,
        success: function (msg)
            {
                updateContent(msg);
            },
        beforeSend: function()
            {
                loading();
            }
        });
}

function updateContent(picture)
{
    var re = new RegExp("^([a-zA-Z0-9]{10}\.gif)$");
    if(re.test(picture))
    {
        $("#animationDiv").html("<img class=\"center-block\"src=\"static/images/"+picture+"\" alt=\"Function Animation\">");
    }
    else
    {
        $("#animationDiv").html("<div class=\"alert alert-danger\" role=\"alert\">Error constructing animation! "+picture+"</div>");
    }
}

function loading()
{
    $("#animationDiv").html("<img class=\"center-block\"src=\"static/loading.gif\" alt=\"Loading\">");
}
