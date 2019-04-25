var imported = document.createElement('script');
imported.src = '/static/javascript/drag_drop_reordering.js';
document.head.appendChild(imported);

function addSelected(componentID) {
    let component = document.getElementById(componentID);
    let selectedComponents = document.getElementById("selectedComponents");
    if (component.checked) {
        let node = document.createElement("LI");
        node.setAttribute("id", "component" + componentID);
        node.setAttribute("draggable", "true");
        node.setAttribute("ondragover", "dragOver(event);");
        node.setAttribute("ondragStart", "dragStart(event);");
        node.setAttribute("value", componentID );
        let textNode = document.createTextNode(component.value);
        node.appendChild(textNode);
        selectedComponents.appendChild(node);
    }
    if (!component.checked) {
        let elementToRemove = document.getElementById("component" + componentID);
        selectedComponents.removeChild(elementToRemove);
    }
}


function saveOrder(operation) {
    if (operation === "existingModule")
        var moduleId = document.getElementById("moduleId");
    let positionedComponents = document.getElementsByTagName("LI");
    let courseId = document.getElementById("courseId");
    if (positionedComponents.length > 0) {
        for (var i = 0; i < positionedComponents.length; i++) {
            let xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function () {
                if (this.readyState == 4 && this.status == 200) {
                    console.log("sent");
                }
            };
            if (operation === "moduleCreate") {
                xhttp.open("GET", "/courses/new_module_save_positions/" + positionedComponents[i].value + '/' + i + '/' + courseId.value , false);
            }
            if (operation === "existingModule") {
                //xhttp.open("GET", "/courses/existing_comp_position/" + moduleId.value + "/" + positionedComponents[i].value  + "/" + i , false);
                xhttp.open("GET", "/courses/apply_element_position/"  + positionedComponents[i].value  + "/" + i +"/1/" + moduleId.value , false);
            }
            xhttp.send();
        }
    }
    return true;

}