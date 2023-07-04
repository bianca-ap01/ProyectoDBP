const pendingForms = new WeakMap();

function editUser() {
    const formEditUser = document.getElementById('formEditUser')
    formEditUser.addEventListener('submit', handlingEditUser)
  }
  
function handlingEditUser(e) {
    e.preventDefault()
    e.stopPropagation()
  
    const formEditUser = e.currentTarget
    const previousController = pendingForms.get(formEditUser)
    if (previousController) {
        previousController.abort()
    }
  
    const controller = new AbortController()
    pendingForms.set(formEditUser, controller)
    console.log('formEditUser: ', formEditUser)
  
    const formData = new FormData(formEditUser)
    fetch('/profile/edit', {
      method: 'POST',
      body: formData,
      signal: controller.signal,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok')
        }
        return response.json()
      })
      .then((data) => {
        console.log('data: ', data)
        const { message } = data
        alert(message)
        window.location.href = '/login'
      })
      .catch((error) => {
        console.error('There has been a problem with your fetch operation:', error)
      })    
  }
  