const redLight = document.querySelector('.red');
const yellowLight = document.querySelector('.yellow');
const greenLight = document.querySelector('.green');

function switchLights() {
  redLight.classList.toggle('active');
  yellowLight.classList.toggle('active');
  greenLight.classList.toggle('active');
}

const response = await fetch('http://127.0.0.1:5000/api/data', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  },
})

console.log(await response.json())

setInterval(
    switchLights(), 2000);