const home = async() => {
    const resp = await fetch(process.env.REACT_APP_API_URL, {
      method:'GET'
    })
    const data = await resp.json()
    console.log("Server health response: ", data)
  }
export default home; 