var contributionBar = document.getElementsByClassName("contribution-bar")

for (let i = 0; i < contributionBar.length; i++) {

	var red = Math.floor(Math.random() * 255)
	var green = Math.floor(Math.random() * 255)
	var blue = Math.floor(Math.random() * 255)
	var randomRGB = "rgb(" + red + "," + green + "," + blue + ")"
	console.log(randomRGB)
	contributionBar[i].style.backgroundColor = randomRGB;
}

//Toggle Edit Team
editTeamName = document.getElementById('editTeamName')
teamName = document.getElementById('teamName')
toggleEdit = document.getElementById('toggleEdit')
cancelEdit = document.getElementById('cancelEdit')

function showInput(){
	var teamNameWidth = teamName.offsetWidth
	editTeamName.style.width = teamNameWidth+ 25 +'px'
	editTeamName.style.display = 'block'
	editTeamName.value = teamName.innerHTML
	teamName.style.display = 'none'
	// On/Off Edit-Cancel Button
	toggleEdit.style.display = 'none'
	cancelEdit.style.display = 'block'
}

function hideInput(){
	editTeamName.style.display = 'none'
	teamName.style.display = 'block'
	toggleEdit.style.display = 'block'
	cancelEdit.style.display = 'none'

}

//Modify context-menu when right-click
window.addEventListener('click', function() {
	hideContextMenu()
})

var toggleContextMenu = document.querySelectorAll('.toggle-context-menu')
Array.prototype.forEach.call(toggleContextMenu, function(tog) {
	tog.addEventListener('contextmenu', showContextMenu) 
})

function showContextMenu(e) {
	hideContextMenu()
	children = this.children[1]
	children.style.display = 'block'
	e.preventDefault()
	console.log(this)
	
}

function hideContextMenu() {
	var memberContextMenu = document.querySelectorAll('.member-context-menu')
	memberContextMenu.forEach(context => context.style.display = 'none' )
}

//Append Task Id To Form Modal

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

completeTasks = document.querySelectorAll('.complete-task')
completeId = document.getElementById('completeId')
console.log(completeId)
completeTasks.forEach(Task => Task.addEventListener('click', appendCompleteTaskId)) 
function appendCompleteTaskId(e) {
	completeId.value = this.id
}