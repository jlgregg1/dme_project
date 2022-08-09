function magnifyImage(element){
    element.style.width = "300px";
    element.style.height = 'auto';
}
function revertImage(element){
    element.style.width = "100px";
    element.style.height = "auto";
}
function displayInfo(element){
    element.innerHTML = "<p>For wheelchair include seat width and seat depth. For canes and walkers include manufacturer's recommended height range for person using the device.</p>";
}