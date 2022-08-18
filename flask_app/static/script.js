//Daily Weather API for the show reports page
var apiDiv = document.querySelector("#apis");
var currentCity = ""; // this holds the city we search for as a string. also gets passed in to the async function as a url parameter

function getCity(element) { // this gets the city name and stores in the variable above
    console.log(element.value);
    currentCity = element.value;
}

function makeCityInfo(data) { // allows us to create new HTML so we can display the API response on the page
// our container for the API response. create the HTML elements inside specific to the reponse info we want to display.
    var spot =  `<div id="api">
                    <h3>${data.name} Forecast</h3>
                    <p>Feels Like: ${data.main.feels_like}</p>
                    <p>Low: ${data.main.temp_min}</p>
                    <p>High: ${data.main.temp_max}</p>
                    <p>Sky: ${data.weather[0].description}</p>
                </div>`
    console.log(spot)
    return spot; // we want to return it so the HTML can be built.
}

async function showCityAsync(){ // this was used before the functions below 
    // The await keyword lets js know that it needs to wait until it gets a response back to continue.
    var response = await fetch("https://api.openweathermap.org/data/2.5/weather?q="+currentCity+"&units=imperial&appid=ccabb67fa9582da15360454e1ba234f7"); // API Call
    // We then need to convert the data into JSON format.
    var cityData = await response.json(); // converts the searched info to a JSON format
    console.log(cityData);
    apiDiv.innerHTML = makeCityInfo(cityData); // made the response variable equal to this because:
    //innerHTMl, when given a string that looks like HTML, will try to turn the string into HTML.
}


