let previousElement;

function dragOver(e) {
  if (isBefore(previousElement, e.target))
    e.target.parentNode.insertBefore(previousElement, e.target);
  else
    e.target.parentNode.insertBefore(previousElement, e.target.nextSibling);
}

function dragStart(e) {
  e.dataTransfer.effectAllowed = "move";
  e.dataTransfer.setData("text/plain", null);
  previousElement = e.target;
}

function isBefore(elementOne, elementTwo) {
    if (elementTwo.parentNode === elementOne.parentNode)
        for (let currentElement = elementOne.previousSibling; currentElement && currentElement.nodeType !== 9; currentElement = currentElement.previousSibling)
            if (currentElement === elementTwo)
                return true;
    return false;

}
function savePosition() {
    let element_type = document.getElementById("element_type");
    let elements = document.getElementsByTagName('li');
    for (var i = 0; i < elements.length; i++) {
      let xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange=function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log("sent");
        }
      };
      xhttp.open("GET", "/courses/apply_element_position/" + elements[i].id +'/' + i +'/' + element_type.value +'/' , false);
      xhttp.send();
    }
    return true;
}