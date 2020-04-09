let box = document.getElementsByClassName('logo')[0];
const canvas = document.querySelector('canvas');
let w = canvas.width = box.clientWidth;
let h = canvas.height = box.clientHeight;

let ctx = canvas.getContext("2d");
			
let x_o = w/2;
let y_o = h/2;
let logo = {x :w/2,y:h/2};

let numParticles = 150;
		
let phi = 1.618;
let scale = 10;

if(window.innerWidth > window.innerHeight) { 
    w = canvas.width = window.innerWidth/2;
    h = canvas.height = window.innerHeight;
    x_o = w/2;
    y_o = h/2;
    logo = {x :w/2,y:h/2};

} 

let coords = new Array(5).fill(1).map((x,i)=>scale*Math.pow(phi,i));

let colorArr = ["#ffff00a3","#ffffffa6"]
let particles = new Array(numParticles).fill(1).map(x=>{return{x:x_o,y:y_o,r:Math.random()*3,dx:1.5*(Math.random()-0.5),dy:Math.random()-0.5,color:colorArr[Math.floor(Math.random()*3)]}});

let update = (parts) =>{
    return parts.map(x=>{
        if((x.x>=w-10)||(x.x-10<=0)) { x.x = x_o; x.y =y_o}
                
        if((x.y>=h-10)||(x.y-10<=0)) { x.x = x_o; x.y =y_o}

        return  {x:x.x+x.dx, y :x.y+x.dy, r : x.r, dx:x.dx,dy:x.dy,color:x.color }
    }
    );
}



let outerCircle = (radius) =>color=>{
    ctx.beginPath();
    ctx.fillStyle = color;
    ctx.arc(logo.x,logo.y,radius,0,2*Math.PI);
    ctx.fill();

}

let innerCircle = (radius) =>(lineWidth) =>(color)=>{
    ctx.lineWidth = lineWidth;
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.arc(logo.x,logo.y,radius,0,2*Math.PI);
    ctx.stroke();
    
}

let rightWhy =(x1,x2,x3)=>(color)=>{
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(x1.x,x1.y);
    ctx.lineTo(x2.x,x2.y);
    ctx.lineTo(x3.x,x3.y);
    ctx.fill();
}


let  controls = new function() {
    this.outRadius = scale*8;
    this.inRadius = this.outRadius*0.9;
    this.lineWidth = scale/2; 
    this.trx1 = {x : logo.x + coords[3] , y : logo.y - coords[3]};
    this.trx2 = {x : logo.x + coords[0], y : logo.y + coords[3]};
    this.trx3 = {x : logo.x - coords[3], y : logo.y + coords[3]};
    
    this.tlx1 = {x : logo.x - coords[3], y : logo.y - coords[3]};
    this.tlx2 = {x : logo.x  + coords[0], y : logo.y - coords[1]};
    this.tlx3 = {x : logo.x  - coords[1] , y : logo.y + coords[0]};
   
    this.background = 'yellow'; //ffff66
    this.foreground = 'black';
}





let drawParts = (parts) =>{
 parts.map(x=>{
     ctx.fillStyle = x.color;
     ctx.beginPath();
     ctx.arc(x.x,x.y,x.r,0,2*Math.PI);
     ctx.fill();
 })
}
let background =()=>{
    ctx.fillStyle = "transparent";
    ctx.fillRect(0,0,w,h);
}
let temp  = 0; 
let animate =()=>{
    temp+=0.01;
    ctx.clearRect(0,0,w,h);
    requestAnimationFrame(animate);
    background();
    particles = update(particles);
    drawParts(particles);
    outerCircle(controls.outRadius)(controls.background);
	innerCircle(controls.inRadius)(controls.lineWidth)(controls.foreground);
	rightWhy(controls.trx1,controls.trx2,controls.trx3)(controls.foreground);
	rightWhy(controls.tlx1,controls.tlx2,controls.tlx3)(controls.foreground);
	
}
animate();

// let revamp =()=>{
//     w = canvas.width = window.innerWidth;
//     h = canvas.width = window.innerHeight;
//     animate();
// }

// window.addEventListener("resize",revamp,false);


			