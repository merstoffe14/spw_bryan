async function main() {
    setInterval(async () => {
        console.log("loop example"); 
    }, 5000);
    example();  
}

async function example() {
    console.log("example!");
    let result = await fetch("/api/example");
    document.getElementById("example_header").innerHTML = await result.text();
}

async function sendCommand(command) {
    await fetch(`/api/sendcommand?command=${command}`)
    
}

// Example function to send a goto command to the server
async function goTo() {

    x = document.getElementById("x_input").value;
    y = document.getElementById("y_input").value;
    z = document.getElementById("z_input").value;
    console.log(x)
    console.log(x, y, z);
    await fetch(`/api/goto?x=${x}&y=${y}&z=${z}&sys=${0}`);

}


main();
