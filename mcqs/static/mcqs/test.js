// window.addEventListener('beforeunload', function (e) {
//   // Cancel the event
//   e.preventDefault(); // If you prevent default behavior in Mozilla Firefox prompt will always be shown
//   // Chrome requires returnValue to be set
//   e.returnValue = 'Test will be submitted if you reload the page';
//   // set sessions value on reloading of page
//   sessionStorage.setItem("reloading","reloading")
//   console.log('onbeforeunload');
// });
// window.onload = function() {
//     var reloading = sessionStorage.getItem("reloading");
//     if (reloading) {
//         sessionStorage.removeItem("reloading");
//         sendData(); //will submit test if user reloads the page
//     }
//     console.log(reloading);
// }
//
// window.addEventListener('unload', function(event) {
//         sendData();
//         console.log('Beware from closing the tab');
//       });
console.log("Hello test")
const url = window.location.href

const quizBox = document.getElementById('quiz-box')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')
const timerBox = document.getElementById('timer-box')
const back_button = document.getElementById('go_back_btn')

var timer //global variable
const activateTimer = (time) => {
    if (time.toString().length < 2) {
        timerBox.innerHTML = `<b>0${time}:00</b>`
    } else {
        timerBox.innerHTML = `<b>${time}:00</b>`
    }

    let minutes = time - 1
    let seconds = 60
    let displaySeconds
    let displayMinutes

    timer = setInterval(()=>{
        seconds --
        if (seconds < 0) {
            seconds = 59
            minutes --
        }
        if (minutes.toString().length < 2) {
            displayMinutes = '0'+minutes
        } else {
            displayMinutes = minutes
        }
        if(seconds.toString().length < 2) {
            displaySeconds = '0' + seconds
        } else {
            displaySeconds = seconds
        }
        if (minutes === 0 && seconds === 0) {
            timerBox.innerHTML = "<b>00:00</b>"
            setTimeout(()=>{
                clearInterval(timer)
                alert('Time over')
                sendData()
            }, 500)
        }

        timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`
    }, 1000)
}
back_button.style.display='none' //hide back button before submission
$.ajax({
  type: 'GET',
  url: `${url}data`,
  success: function(response){
    const data = response.data
        data.forEach(el => {
            for (const [question, answers] of Object.entries(el)){
                quizBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>
                `
                answers.forEach(answer=>{
                   quizBox.innerHTML += `
                       <div>
                           <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                           <label for="${question}">${answer}</label>
                       </div>
                   `
               })
          }
          });
          activateTimer(response.time)
  },
  error: function(error) {
    console.log(error)
  }
})

const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(el=>{
        if (el.checked) {
            data[el.name] = el.value
        } else {
            if (!data[el.name]) {
                data[el.name] = null
            }
        }
    })

    $.ajax({
        type: 'POST',
        url: `${url}save/`,
        data: data,
        success: function(response){
          const results = response.results
          console.log(results)
          quizForm.style.display='none' //will hide form after submission

          scoreBox.innerHTML = `${response.passed ? 'Congratulations! Pass: ' : 'Sorry, Fail: '}Your result is ${response.score.toFixed(2)}%`

            results.forEach(res=>{
                const resDiv = document.createElement("div")
                for (const [question, resp] of Object.entries(res)){

                    resDiv.innerHTML += question
                    const cls = ['container', 'p-3', 'text-light', 'h6']
                    resDiv.classList.add(...cls)

                    if (resp=='not answered') {
                        resDiv.innerHTML += '- not answered'
                        resDiv.classList.add('bg-danger')
                    }
                    else {
                        const answer = resp['answered']
                        const correct = resp['correct_answer']

                        if (answer == correct) {
                            resDiv.classList.add('bg-success')
                            resDiv.innerHTML += ` answered: ${answer}`
                        } else {
                            resDiv.classList.add('bg-danger')
                            resDiv.innerHTML += ` | correct answer: ${correct}`
                            resDiv.innerHTML += ` | answered: ${answer}`
                        }
                    }
                }

                resultBox.append(resDiv)
            })
            back_button.style.display='' //display go back button after submission
          },
          error: function(error){
            console.log(error)
          }
        })
}

quizForm.getElementById("idOfButton").addEventListener('submit', e=>{
    e.preventDefault()
    e.disabled = true;
    sendData()
    timerBox.innerHTML = "<b>00:00</b>"

    clearInterval(timer) //set timer to 0 after submission
})

// document.getElementById("idOfButton").onclick = function() {
//     //disable
//     this.disabled = true;
//
//     //do some validation stuff
// }
