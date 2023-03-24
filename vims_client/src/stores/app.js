import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAppStore = defineStore('app', () => {
  // * APP STATE
  // App Views: search, profile, login, signup
  const currentView = ref('search')

  // * USER DATA
  const userData = ref({})


  // * APP AUTHENTICATION
  const userToken = ref('') // ex: "Token 032579768a98dda5da05a6fedf28ea2786adddb1"

  async function getTokenFromCookies() {
    const cookies = document.cookie.split(';')
    // Loop through each cookie to find the authentication token
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      // If the cookie starts with 'accessToken=', try to get user data
      if (cookie.startsWith('accessToken=')) {
        const accessToken = cookie.substring('accessToken='.length, cookie.length)
        try {
          // Get user data
          const responseUserData = await axios.get('http://127.0.0.1:8000/api/user/details/', {
            headers: {
              Authorization: accessToken
            }
          })
          // Assign data only if success
          userToken.value = accessToken
          userData.value = responseUserData.data
        } catch (error) {
          return null
        }
      }
    }
    // If no authentication token is found, return null
    return null
  }

  function saveTokenToCookies(accessToken) {
    // Set the expiry date to one year from now
    const expiryDate = new Date();
    expiryDate.setFullYear(expiryDate.getFullYear() + 1);
    // Save the token
    document.cookie = `accessToken=${accessToken}; expires=${expiryDate.toUTCString()}; path=/`;
  }

  function removeTokenFromCookies() {
    // Set the expiry date to a date in the past
    const expiryDate = new Date();
    expiryDate.setDate(expiryDate.getDate() - 5);
    // Remove the authentication token cookie by setting its expiry time to a date in the past
    document.cookie = `accessToken=; expires=${expiryDate.toUTCString()}; path=/`;
  }


  async function signup(formData) {
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/auth/register/', formData)
      const accessToken = `Token ${response.data.token}`

      // Get user data
      const responseUserData = await axios.get('http://127.0.0.1:8000/api/user/details/', {
        headers: {
          Authorization: accessToken
        }
      })

      // Assign data only if success the two requests
      userToken.value = accessToken
      saveTokenToCookies(accessToken)
      userData.value = responseUserData.data
      return response
    } catch (error) {
      return error.response
    }
  }

  async function login(formData) {
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/auth/token/', formData)
      const accessToken = `Token ${response.data.token}`

      // Get user data
      const responseUserData = await axios.get('http://127.0.0.1:8000/api/user/details/', {
        headers: {
          Authorization: accessToken
        }
      })

      // Assign data only if success the two requests
      userToken.value = accessToken
      saveTokenToCookies(accessToken)
      userData.value = responseUserData.data
      return response
    } catch (error) {
      return error.response
    }
  }

  async function logout() {
    try {
      await axios.post(
        'http://127.0.0.1:8000/api/auth/logout/',
        {},
        {
          headers: {
            Authorization: userToken.value
          }
        }
      )
      // * On Success, clear user data
      userToken.value = ''
      removeTokenFromCookies()
      userData.value = {}
    } catch (error) {
      if (error.response.status === 403) {
        // * On Invalid Token, clear user data
        userToken.value = ''
        removeTokenFromCookies()
        userData.value = {}
      }
      console.log(error.response.data)
    }

    // * Go to search view
    currentView.value = 'search'
  }

  return {
    currentView,
    userData,
    userToken,
    getTokenFromCookies,
    signup,
    login,
    logout
  }
})
