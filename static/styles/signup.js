const pendingForms = new WeakMap();

function SignUp(){
    const formSignUp = document.getElementById("formSignUp");
    formSignUp.addEventListener("submit", handlingSignUp);
}

function handlingSignUp(event) {
    event.preventDefault();
    event.stopPropagation();

    const formSignUp = event.currentTarget;
    const previousControl = pendingForms.get(formSignUp);
    if (previousControl) {
        previousControl.abort();
    }

    const control = new AbortController();
    pendingForms.set(formSignUp, control);
    console.log("handlingSignUp")

    const formData = new FormData(formSignUp);

    fetch('/signup', {
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
                window.location.href = "/login";
            }
        })
        .catch(error => {
            console.log('error', error);
        }
        )
        .finally(() => {
            pendingForms.delete(formSignUp);
        }
        );   
}