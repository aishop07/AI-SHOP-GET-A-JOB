// {% load static %}
// Create the canvas
var canvas = document.createElement("canvas");
var ctx = canvas.getContext("2d");
canvas.width = 426;
canvas.height = 398;
document.getElementById("canvas").appendChild(canvas);

// Background image
var bgReady = false;
var bgImage = new Image();
bgImage.onload = function () {
	bgReady = true;
};
bgImage.src = "static/images/無人商店平面圖.png";

// Hero image
var heroReady = false;
var heroImage = new Image();
heroImage.onload = function () {
	heroReady = true;
};
heroImage.src = "static/images/hero.png";

// Monster image
// var monsterReady = false;
// var monsterImage = new Image();
// monsterImage.onload = function () {
// 	monsterReady = true;
// };
// monsterImage.src = "static/images/monster.png";

//circle image
var circleReady = false
var circleImage = new Image()
circleImage.onload = function(){
	circleReady = true
}
circleImage.src = "static/images/circle.png"

// Game objects
var hero = {
	speed: 256 // movement in pixels per second
};
// var monster = {};
var circle = {};
// var monstersCaught = 0;

// Handle keyboard controls
var keysDown = {};

addEventListener("keydown", function (e) {
	keysDown[e.keyCode] = true;
}, false);

addEventListener("keyup", function (e) {
	delete keysDown[e.keyCode];
}, false);

// Reset the game when the player catches a monster
var reset = function () {
	hero.x = 200;
	hero.y = 350;
	circle.x = 210;
	circle.y = 250;
	// Throw the monster somewhere on the screen randomly
	// monster.x = 32 + (Math.random() * (canvas.width - 64));
	// monster.y = 32 + (Math.random() * (canvas.height - 64));
};

// Update game objects
var update = function (modifier) {
	if (38 in keysDown) { // Player holding up
		hero.y -= hero.speed * modifier;
		var a = $('.wc-shellinput')
		// document.getElementsByClassName('wc-shellinput')[1].value("123")
		console.log(a)
		// console.log(a[0].attr('placeholder'))
		// document.getElementById('chat').setAttribute('value','123')
	}
	if (40 in keysDown) { // Player holding down
		hero.y += hero.speed * modifier;
	}
	if (37 in keysDown) { // Player holding left
		hero.x -= hero.speed * modifier;
	}
	if (39 in keysDown) { // Player holding right
		hero.x += hero.speed * modifier;
	}

	// Are they touching?
	if (
		hero.x <= (circle.x + 16)
		&& circle.x <= (hero.x + 16)
		&& hero.y <= (circle.y + 16)
		&& circle.y <= (hero.y + 16)
	) {
		// document.getElementById('chat').setAttribute('value','123')
		alert("123")
		
		// ++monstersCaught;
		reset();
	}
};

// Draw everything
var render = function () {
	if (bgReady) {
		ctx.drawImage(bgImage, 0, 0);
	}
	if (circleReady) {
		ctx.drawImage(circleImage, circle.x, circle.y);
	}
	if (heroReady) {
		ctx.drawImage(heroImage, hero.x, hero.y);
	}

	// if (monsterReady) {
	// 	ctx.drawImage(monsterImage, monster.x, monster.y);
	// }
	
	// Score
	// ctx.fillStyle = "rgb(250, 250, 250)";
	// ctx.font = "24px Helvetica";
	// ctx.textAlign = "left";
	// ctx.textBaseline = "top";
	// ctx.arc(215, 300, 10, 0, 2*Math.PI);
	// ctx.stroke();
	// ctx.fillText("Goblins caught: " + monstersCaught, 32, 32);
};

// The main game loop
var main = function () {
	var now = Date.now();
	var delta = now - then;

	update(delta / 1000);
	render();

	then = now;

	// Request to do this again ASAP
	requestAnimationFrame(main);
};

// Cross-browser support for requestAnimationFrame
var w = window;
requestAnimationFrame = w.requestAnimationFrame || w.webkitRequestAnimationFrame || w.msRequestAnimationFrame || w.mozRequestAnimationFrame;

// Let's play this game!
var then = Date.now();
reset();
main();
