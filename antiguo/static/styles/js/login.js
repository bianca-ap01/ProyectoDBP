const pendingForms = new WeakMap();

function login() {
    const formLogin = document.getElementById("formLogin");
    formLogin.addEventListener("submit", handlingLogin);
}

function handlingLogin(event) {
    event.preventDefault();
    event.stopPropagation();
    
    const formLogin = event.currentTarget;
    const previousControl = pendingForms.get(formLogin);
    if (previousControl) {
        previousControl.abort();
    }

    const control = new AbortController();
    pendingForms.set(formLogin, control);
    console.log("handlingLogin")

    const formData = new FormData(formLogin);

    fetch('/login', {
        method: 'POST',
        body: formData,
        signal: control.signal,
    })
        .then(response => {
            console.log('response', response)
            return response.json();
        })
        .then(responseJson => {
            if(!responseJson.success){
                const error = document.getElementById("error");
                error.innerHTML = responseJson.message;
            }else{
                window.location.href = "/home";
            }
        })
        .catch(error => {
            console.log('error', error);
        }
        )
        .finally(() => {
            pendingForms.delete(formLogin);
        }
    );
}
