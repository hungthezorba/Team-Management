var contributionBar = document.getElementsByClassName("contribution-bar")

for (let i = 0; i < contributionBar.length; i++) {

	var red = Math.floor(Math.random() * 255)
	var green = Math.floor(Math.random() * 255)
	var blue = Math.floor(Math.random() * 255)
	var randomRGB = "rgb(" + red + "," + green + "," + blue + ")"
	console.log(randomRGB)
	contributionBar[i].style.backgroundColor = randomRGB;
}