function norm(str) {
    return str.normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .replace(/ç/g, "c")
        .replace(/[^\w\s-]/g, "")
        .trim()
        .replace(/\s+/g, '-')
        .toLowerCase()
}

function form(name, values, buttons, url, message, popupStatus) {
    let box = document.getElementById('box')
    if (popupStatus)
        box = document.querySelector('.form-content').querySelector('#box')

    box.innerHTML = `
        <form action="/${url}" method="post">
            <div class="form-inputs"></div>
            <div class="form-buttons"></div>
        </form>
    `;
    if (message !== '') {
        const span = document.createElement('span')
        span.textContent = message
        document.querySelector('form').insertAdjacentElement('afterbegin', span)
    }

    let inputsContainer = document.querySelector('.form-inputs')
    let buttonsContainer = document.querySelector('.form-buttons')

    if (popupStatus) {
        inputsContainer = document.querySelector('.form-content').querySelector('.form-inputs')
        buttonsContainer = document.querySelector('.form-content').querySelector('.form-buttons')
    }

    const inputsFragment = document.createDocumentFragment()
    if (name.length <= 5) {
        inputsContainer.style.width = '360px'
    }
    name.forEach(({label, type}, index) => {
        const div = document.createElement('div')
        const labelElement = document.createElement('label')
        let inputElement = document.createElement('input')

        const id = label.toLowerCase()

        if (type === 'select') {
            inputElement = document.createElement('select')
            name[index].options.forEach(value => {
                const option = document.createElement('option')
                option.value = norm(value)
                option.textContent = value
                inputElement.appendChild(option)
            })
            if (values[index] !== undefined) {
                inputElement.value = norm(values[index])
            }
        } else if (type === 'textarea') {
            inputElement = document.createElement('textarea')
        } else {
            inputElement.type = type
        }
        inputElement.required = true
        labelElement.htmlFor = inputElement.id = inputElement.name = norm(id)
        if (values[index] !== undefined && type !== 'select') {
            if (type === 'date') {
                 const [day, month, year] = values[index].split('-');
                 values[index] = `${year}-${month}-${day}`
            }
            inputElement.value = values[index]
        }
        labelElement.textContent = label

        div.append(labelElement, inputElement)
        inputsFragment.appendChild(div)
    })
    inputsContainer.appendChild(inputsFragment)
    if ((name.length % 2) !== 0 && name.length > 5) {
        const div = inputsContainer.querySelectorAll('div')
        div[div.length - 1].style = `flex: 0 0 740px; display: flex; flex-direction: column; flex-wrap: wrap;`
    }

    buttons.forEach(buttonText => {
        const button = document.createElement('button')
        button.type = "submit"
        button.textContent = buttonText
        buttonsContainer.appendChild(button)
    })

    if (!locale && document.querySelector('.option') === null) {
        const forgotPasswordButton = document.createElement("button")
        forgotPasswordButton.type = 'button'
        forgotPasswordButton.className = 'option'
        forgotPasswordButton.textContent = 'Esqueceu a senha?'
        forgotPasswordButton.addEventListener('click', () => {
            popup([{label: 'Email', type: 'email'}], [],['Enviar'], 'Esqueci a senha', 'esqueciSenha', true)
        })
        inputsContainer.insertAdjacentElement('afterend', forgotPasswordButton)
    }
}
