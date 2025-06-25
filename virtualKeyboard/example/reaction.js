let showChord = true; // whether or not the chord to be completed is shown during the count-down

let chords = [
  "FJ",
  "DK",
  "JS",
  "FK",
  "CJ",
  "GJ",
  "KX",
  "BK",
  "JQ",
  "JV",
  "JW",
  "JX",
  "KQ",
  "KV",
  "MV",
  "PQ",
  "HV",
  "MX",
  "QY",
  "HQ",
  "MQ",
  "MZ",
  "PV",
  "DF",
  "CF",
  "DX",
  "SX",
  "SZ",
  "DQ",
  "DZ",
  "FQ",
  "FZ",
  "CV",
  "FG",
  "QW",
  "XZ",
  "BC",
  "BF",
  "BG",
  "FV",
  "VZ",
  "BQ",
  "CW",
  "GQ",
  "QV",
  "JK",
  "JL",
  "HK",
  "JM",
  "IJ",
  "KP",
  "JP",
  "HJ",
  "JY",
];

let systemStates = {
  ROLLOVER: "rollover",
  SHOW_CHORD: "show_chord",
  PRIME_CHORD: "prime_chord",
  READY_CHORD: "ready_chord",
  WAITING_READY: "waiting_ready",
};

let systemState = systemStates.ROLLOVER;

let timerLength = 3;
let timeToDisplay;

let index = 0;
let chordToComplete;

let interval;
let timer;

let startTime;
let postureKeys;

function setup() {
  createCanvas(800, 150);

  textSize(20);
  chords = shuffle(chords);
  // nextTask();
}

function draw() {
  background(255);
  switch (systemState) {
    case systemStates.ROLLOVER:
      push();
      textAlign(CENTER);
      text(
        "Press as many keys as you can.\nYou have pressed " +
          maxKeysPressed +
          " keys.\nPress Enter when you have pressed as many keys as you can.",
        width / 2,
        height / 2 - 40,
      );
      pop();
      break;
    case systemStates.SHOW_CHORD:
      background(0, 220, 0);
      push();
      textAlign(CENTER);
      text(chordToComplete, width / 2, height / 2);
      pop();

      colourChord(chordToComplete);
      break;
    case systemStates.READY_CHORD:
      push();
      textAlign(CENTER);
      text(timeToDisplay, width / 2, height / 2);
      pop();
      break;
    case systemStates.PRIME_CHORD:
      push();
      textAlign(CENTER);
      let textToShow = "";
      if (showChord) {
        textToShow = chordToComplete;
        colourChord(chordToComplete);
      }
      text(
        "Release " +
          postureKeys.join("") +
          "\nin " +
          timeToDisplay +
          "s" +
          "\n\n" +
          textToShow,
        width / 2,
        height / 2,
      );
      pop();
      break;
    case systemStates.WAITING_READY:
      push();
      textAlign(CENTER);
      text("Press " + postureKeys.join(""), width / 2, height / 2);
      pop();
      break;
  }
}

let maxKeysPressed = 0;
let numPressedKeys = 0;

let keysPressed = {
  A: 0,
  S: 0,
  D: 0,
  F: 0,
  J: 0,
  K: 0,
  L: 0,
  ";": 0,
  V: 0,
  N: 0,
};

function colourPosture() {
  for (let i = 0; i < postureKeys.length; i++) {
    colourKey(postureKeys[i], "darkgray");
  }
}

function colourChord(chord) {
  for (let i = 0; i < chords.length; i++) {
    colourKey(chord[i], "green");
  }
}

function setPostureKeys(maxKeys) {
  if (maxKeys >= 8) {
    postureKeys = ["a", "s", "d", "f", "j", "k", "l", ";"];
  } else if (maxKeys >= 6) {
    postureKeys = ["s", "d", "f", "j", "k", "l"];
  } else if (maxKeys >= 4) {
    postureKeys = ["d", "f", "j", "k"];
  } else {
    postureKeys = ["f", "j"];
  }
}

function postureKeysDown() {
  for (let i = 0; i < postureKeys.length; i++) {
    if (!keyIsDown(postureKeys[i].toUpperCase().charCodeAt(0))) {
      return false;
    }
  }
  return true;
}

function keyPressed(event) {
  event.preventDefault();
  colourKey(key, "gray");
  switch (systemState) {
    case systemStates.ROLLOVER:
      numPressedKeys++;

      if (numPressedKeys > maxKeysPressed) {
        maxKeysPressed = numPressedKeys;
      }

      if (key == "Enter" && maxKeysPressed > 0) {
        setPostureKeys(maxKeysPressed);
        nextTask();
      }
      break;
    case systemStates.WAITING_READY:
      if (postureKeysDown()) {
        systemState = systemStates.PRIME_CHORD;

        timeToDisplay = timerLength;
        interval = setInterval(() => {
          timeToDisplay -= 1;
        }, 1000);

        timer = setTimeout(() => {
          clearInterval(interval);
          systemState = systemStates.SHOW_CHORD;
          startTime = millis();
        }, timerLength * 1000);
      }
      break;
    case systemStates.SHOW_CHORD:
      let key1 = chordToComplete.charCodeAt(0);
      let key2 = chordToComplete.charCodeAt(1);

      if (keyIsDown(key1) && keyIsDown(key2)) {
        console.log(chordToComplete, ":", millis() - startTime, "ms");
        nextTask();
      }
      break;
  }
}

function keyReleased(event) {
  event.preventDefault();
  colourKey(key, "default");

  switch (systemState) {
    case systemStates.ROLLOVER:
      numPressedKeys--;

      break;
    case systemStates.PRIME_CHORD:
      if (!postureKeysDown()) {
        if (timeToDisplay > 0) {
          systemState = systemStates.WAITING_READY;

          // kill timers

          colourPosture();
          clearInterval(interval);
          clearTimeout(timer);
        }
      }
      break;

    case systemStates.WAITING_READY:
      colourPosture();
      break;
  }
}

function nextTask() {
  index = (index + 1) % chords.length;
  chordToComplete = chords[index];
  systemState = systemStates.WAITING_READY;
  colourPosture();
}
