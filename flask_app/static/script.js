//Daily Weather API for the show reports page using REST API
const apiDiv = document.querySelector("#apis");
let currentCity = ""; // this holds the city we search for as a string. also gets passed in to the async function as a url parameter

function getCity(element) { // this gets the city name and stores in the variable above
    currentCity = element.value;
}

function makeCityInfo(data) { // allows us to create new HTML so we can display the API response on the page
// container for the API response. create the HTML elements inside specific to the reponse info I want to display.
    var fishingSpot =  `<div id="api">
                    <h3>${data.name} Forecast</h3>
                    <p>Feels Like: ${data.main.feels_like}</p>
                    <p>Low: ${data.main.temp_min}</p>
                    <p>High: ${data.main.temp_max}</p>
                    <p>Sky: ${data.weather[0].description}</p>
                </div>`
    return fishingSpot; // we want to return it so the HTML can be built.
}

async function showCityAsync(){
    // The await keyword lets js know that it needs to wait until it gets a response back to continue. await returns the RESOLVED value of a promise. it halts the execution of the function until the promise is resolved.
    const response = await fetch("https://api.openweathermap.org/data/2.5/weather?q="+currentCity+"&units=imperial&appid=ccabb67fa9582da15360454e1ba234f7"); // API Call (fetch by default is a GET request)
    // We then need to convert the data into JSON format.
    const cityData = await response.json(); // converts the searched info from JSON object to Javascript Object and waits for the json returned promise.
    apiDiv.innerHTML = makeCityInfo(cityData); // made the response variable equal to this because:
    //innerHTML, when given a string that looks like HTML, will try to turn the string into HTML
}


