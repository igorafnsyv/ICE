function deleteComponent(componentID) {
      let xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange=function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("component" + componentID).innerHTML="";
        }
      };
      xhttp.open("GET", "/courses/delete_component/" + componentID, false);
      xhttp.send();
  }

function removeComponent(componentID) {
  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange=function() {
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById("component" + componentID).innerHTML="";
    }
  };
  xhttp.open("GET", "/courses/component_free/" + componentID, false);
  xhttp.send();
}