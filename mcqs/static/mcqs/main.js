console.log('hello world')

const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('start-button')

const url = window.location.href

modalBtns.forEach(modalBtn=> modalBtn.addEventListener('click', ()=>{
    const pk = modalBtn.getAttribute('data-pk')
    const name = modalBtn.getAttribute('data-test')
    const topic = modalBtn.getAttribute('data-topic')
    const numQuestions = modalBtn.getAttribute('data-questions')
    const scoreToPass = modalBtn.getAttribute('data-pass')
    const time = modalBtn.getAttribute('data-time')

    modalBody.innerHTML = `
        <div class="h5 mb-3">Are you sure you want to begin "<b>${name}</b>"?</div>
        <div class="text-muted">
            <ul>
                <li>Topic: <b>${topic}</b></li>
                <li>Number of Questions: <b>${numQuestions}</b></li>
                <li>Minuimum Score to Pass: <b>${scoreToPass}%</b></li>
                <li>Time: <b>${time} Min</b></li>
            </ul>
        <!-- <div class='h6 mb-3'>After starting the test do not try to reload or close the page, doing this action will submit your test</div> -->
        </div>
    `

    startBtn.addEventListener('click', ()=>{
        window.location.href = url + pk
    })
}))
