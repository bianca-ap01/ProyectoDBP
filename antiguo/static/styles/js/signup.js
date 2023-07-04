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
    fetch('/signup', {
      method: 'POST',
      body: formData,
      signal: controller.signal,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok')
        }
        return response.json()
      }
      )
      .then((data) => {
        console.log('data: ', data)
        const { message } = data
        alert(message)
        window.location.href = '/login'
      }
      )
      .catch((error) => {
        console.error('There has been a problem with your fetch operation:', error)
      }
      )    
  }
  