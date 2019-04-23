//maybe can merge all reordering in one similar file
//main function will receive a parameter -> address of the function?

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


function selectComponent(componentId) {
    let component = document.getElementById("component" + componentId);
    let selectedList = document.getElementById("selectedList");
    if (component.checked) {
        let node = document.createTextNode(component.value)
        let elem = document.createElement("LI");
        elem.setAttribute("id", "component" + componentId);
        elem.setAttribute("draggable", "true");
        elem.setAttribute("ondragover", "dragOver(event);");
        elem.setAttribute("ondragStart", "dragStart(event);");
        elem.setAttribute("value", componentId );
        elem.appendChild(node);
        selectedList.appendChild(elem);
    } else {
        let elementToRemove = document.getElementById("component" + componentId);
        selectedList.removeChild(elementToRemove);
    }

}

function componentPositioning() {
    let moduleId = document.getElementById("moduleId");
    let selectedComponents = document.getElementsByTagName("LI");
    if (selectedComponents.length > 0) {
        for (let i = 0; i < selectedComponents.length; i++) {
            let xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function () {
                if (this.readyState == 4 && this.status == 200) {
                    console.log("sent");
                }
            };
            xhttp.open("GET", "/courses/existing_comp_position/" + moduleId.value + "/" + selectedComponents[i].value  + "/" + i , false);
            xhttp.send();
        }

    }
    return true;
}
