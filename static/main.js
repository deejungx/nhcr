function render_output(response) 
{
    item = response['result'][0]
    console.log(item);
    document.getElementById("out1").innerHTML = item[0];
    document.getElementById("out2").innerHTML = item[1];
    document.getElementById("out3").innerHTML = item[2];
}