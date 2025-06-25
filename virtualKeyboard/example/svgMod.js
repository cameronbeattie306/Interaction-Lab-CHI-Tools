function getKeyID(key) {
  let numReg = /^\d+$/;
  if (numReg.test(key)) {
    return "Digit" + key;
  }

  let letterReg = /[a-zA-Z]/;
  if (letterReg.test(key) && key.length == 1) {
    return "Key" + key.toUpperCase();
  }

  let keyMapping = {
    ",": "Comma",
    ".": "Period",
    ";": "Semicolon",
    "/": "Slash",
    "-": "Minus",
    "[": "BracketLeft",
    "'": "Quote",
    "=": "Equal",
    "]": "BrackeRight",
    "\\": "Backslash",
    Control: "ControlLeft",
    " ": "Space",
    Backspace: "Backspace",
    Tab: "Tab",
    CapsLock: "CapsLock",
    "`": "Backquote",
    Shift: "ShiftLeft",
    Alt: "AltLeft",
    Fn: "Fn",
  };

  return keyMapping[key];
}

function colourKey(key, colour) {
  if (key) {
    const obj = document.getElementById("keyboardOBJ");
    const svgDoc = obj.getSVGDocument();

    const keyID = getKeyID(key);
    const keyElem = svgDoc.getElementById(keyID);

    if (keyElem) {
      if (colour == "default") {
        keyElem.setAttribute("fill", "#f7f7f7");
      } else {
        keyElem.setAttribute("fill", colour);
      }
    }
  }
}
