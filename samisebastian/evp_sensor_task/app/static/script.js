const redLight = document.querySelector('.red');
const yellowLight = document.querySelector('.yellow');
const greenLight = document.querySelector('.green');

function switchLights(color) {
  console.log(color)
  redLight.classList.remove('active');
  yellowLight.classList.remove('active');
  greenLight.classList.remove('active');


  if (color === 'red')
    redLight.classList.add('active');

  else if (color === 'yellow')
    yellowLight.classList.add('active');

  else if (color === 'green')
    greenLight.classList.add('active');
}

const response = await fetch('http://127.0.0.1:5000/api/data', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  },
})

setInterval(async () => {
  const response = await fetch('http://127.0.0.1:5000/api/data', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },

  })

  const _color = (await response.json())[0][0]
  switchLights(_color)

}, 10000)