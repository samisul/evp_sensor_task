// Selektieren der Licht-Elemente (rot, gelb, grün) und des Warnungsbereichs
const redLight = document.querySelector(".red");
const yellowLight = document.querySelector(".yellow");
const greenLight = document.querySelector(".green");
const warningWrapper = document.querySelector(".warning__wrapper");

// Anfangszustand: Warnungsbereich ausgeblendet
warningWrapper.style.display = "none";

// Funktion zum Umschalten der Lichter basierend auf der empfangenen Farbe
function switchLights(color) {
  // Zurücksetzen aller Lichter auf inaktiven Zustand
  redLight.classList.remove("active");
  yellowLight.classList.remove("active");
  greenLight.classList.remove("active");
  // Warnungsbereich zunächst ausblenden
  warningWrapper.style.display = "none";

  // Umschalten der Lichter basierend auf der empfangenen Farbe
  if (color === "red") {
    // Bei roter Farbe: Anzeigen des Warnungsbereichs und Aktivieren des roten Lichts
    warningWrapper.style.display = "block";
    redLight.classList.add("active");
  } else if (color === "yellow") {
    // Bei gelber Farbe: Aktivieren des gelben Lichts
    yellowLight.classList.add("active");
  } else if (color === "green") {
    // Bei grüner Farbe: Aktivieren des grünen Lichts
    greenLight.classList.add("active");
  }
}

// Abrufen der Daten vom API-Endpunkt für die Farbinformationen
const response = await fetch("http://127.0.0.1:5000/api/data", {
  method: "GET",
  headers: {
    "Content-Type": "application/json",
  },
});

// Aktualisieren der Lichter basierend auf den empfangenen Daten in einem Intervall
setInterval(async () => {
  const response = await fetch("http://127.0.0.1:5000/api/data", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  // Extrahieren der Farbinformationen aus den empfangenen Daten
  const color = (await response.json())[0][0];
  // Umschalten der Lichter basierend auf der empfangenen Farbe
  switchLights(color);
}, 10000); // Intervall: alle 10 Sekunden
