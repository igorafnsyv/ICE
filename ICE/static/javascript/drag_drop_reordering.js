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