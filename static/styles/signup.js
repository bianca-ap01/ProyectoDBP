const pendingForms = new WeakMap();

function createUser() {
    const formCreateUserId = document.getElementById('formSignUp')
    formCreateUserId.addEventListener('submit', handlingCreateUser)
  }
  
  function handlingCreateUser(e) {
    e.preventDefault()
    e.stopPropagation()
  
    const formCreateUser = e.currentTarget
    const previousController = pendingForms.get(formCreateEmployee)
    if (previousController) {
      previousController.abort()
    }
  
    const controller = new AbortController()
    pendingForms.set(formCreateUser, controller)
    console.log('formCreateUser: ', formCreateUser)
  
    const formData = new FormData(formCreateUser)
    fetch('/create-employee', {
      method: 'POST',
      body: formData,
      signal: controller.signal,
    })
  }
  