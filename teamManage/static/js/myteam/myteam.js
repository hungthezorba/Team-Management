var contributionBar = document.getElementsByClassName("contribution-bar")

for (let i = 0; i < contributionBar.length; i++) {

	var red = Math.floor(Math.random() * 255)
	var green = Math.floor(Math.random() * 255)
	var blue = Math.floor(Math.random() * 255)
	var randomRGB = "rgb(" + red + "," + green + "," + blue + ")"
	console.log(randomRGB)
	contributionBar[i].style.backgroundColor = randomRGB;
}


//Drop down on context
window.addEventListener('click', function() {
	hideContextMenu()
})



var toggleContextMenu = document.querySelectorAll('.toggle-context-menu')
Array.prototype.forEach.call(toggleContextMenu, function(tog) {
	tog.addEventListener('contextmenu', showContextMenu) 
})

function showContextMenu(e) {
	children = this.children[1]
	children.style.display = 'block'
	e.preventDefault()
	
}

function hideContextMenu() {
	var memberContextMenu = document.querySelectorAll('.member-context-menu')
	memberContextMenu.forEach(context => context.style.display = 'none' )
}


editTasks = document.querySelectorAll('.edit-task')
editId = document.getElementById('editId')
editName = document.getElementById('editName')
editDescription = document.getElementById('editDescription')
editTasks.forEach(Task => Task.addEventListener('click', appendTaskId)) 
console.log(editName)
function appendTaskId(e) {
	taskName = document.getElementById('name' + this.id)
	taskDescription = document.getElementById('description' + this.id)
	editName.value = taskName.innerHTML
	editDescription.value = taskDescription.innerHTML
	editId.value = this.id
}