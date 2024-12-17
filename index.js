const express = require("express");
const mongoose = require("mongoose");
const app = express();
const bodyParser = require("body-parser");
const { SerialPort } = require('serialport');
const { ReadlineParser } = require('@serialport/parser-readline');
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);

mongoose.connect("mongodb+srv://pedroalves700:8dNIp4h6bNVMF6UY@cluster0.afo8cn1.mongodb.net/paperTactileSensationsDB", {useNewUrlParser: true});
const conn2 = mongoose.createConnection("mongodb+srv://pedroalves700:8dNIp4h6bNVMF6UY@cluster0.afo8cn1.mongodb.net/tactileProjectDataDB", {useNewUrlParser: true});

const highPulseLowPulseMsDataSchema = {
   hp_ms: Number,
   lp_ms: Number,
   t: Number,
   d: Number
}

const HighPulseLowPulseMsData = conn2.model('HighPulseLowPulseMsData', highPulseLowPulseMsDataSchema);

const paperTactileSensationsSchema = {
   tactile_sensation_ID: String,
   tactile_sensation_name: String,
   texture_type: String, 
   frequency_low_speed: Number,
   duty_cycle_low_speed: Number, 
   frequency_high_speed: Number,
   duty_cycle_high_speed: Number 
}

const PaperTactileSensation = mongoose.model('PaperTactileSensation', paperTactileSensationsSchema);

const absence_of_sensation = new PaperTactileSensation({
   tactile_sensation_ID: "0",
   tactile_sensation_name: "Absence of Sensation",
   texture_type: "External movements, in texture regions, represent absence of tactile sensation", 
   frequency_low_speed: 0,
   duty_cycle_low_speed: 0, 
   frequency_high_speed: 0,
   duty_cycle_high_speed: 0
});

const coarse_roughness = new PaperTactileSensation({
   tactile_sensation_ID: "1",
   tactile_sensation_name: "Coarse Roughness",
   texture_type: "Similar to contact with different thicknesses boulders", 
   frequency_low_speed: 4,
   duty_cycle_low_speed: 32, 
   frequency_high_speed: 7,
   duty_cycle_high_speed: 32
});

const fine_roughness = new PaperTactileSensation({
   tactile_sensation_ID: "2",
   tactile_sensation_name: "Fine Roughness",
   texture_type: "Similar to contact with different thicknesses boulders",
   frequency_low_speed: 12,
   duty_cycle_low_speed: 34, 
   frequency_high_speed: 40,
   duty_cycle_high_speed: 34
});

const softness = new PaperTactileSensation({
   tactile_sensation_ID: "3",
   tactile_sensation_name: "Softness",
   texture_type: "Similar to the experience of running fingers over cotton",
   frequency_low_speed: 167,
   duty_cycle_low_speed: 17, 
   frequency_high_speed: 167,
   duty_cycle_high_speed: 24
});

const smoothness = new PaperTactileSensation({
   tactile_sensation_ID: "4",
   tactile_sensation_name: "Smoothness",
   texture_type: "It indicates contact with materials similar to polished wood",
   frequency_low_speed: 333,
   duty_cycle_low_speed: 46, 
   frequency_high_speed: 333,
   duty_cycle_high_speed: 67
});

/*
absence_of_sensation.save();
coarse_roughness.save();
fine_roughness.save();
softness.save();
smoothness.save();
*/

/*
TactileSensation.findByIdAndRemove("63f129da82a3bea1e2691429", function(err){
   if(!err){
     console.log("Tactile sensation successfully deleted.");
   }
});
*/

var oldMouseSpeedValue = 0;

var GyX;
var GyY;

var S_GyX;
var S_GyY;

var roll;
var pitch;

var pixelPositionX;
var pixelPositionY;

var id_on_off;
var id_on_off_1 = "0";

var oldValue_X = 0;
var oldValue_Y = 0;

var aux_X;
var aux_Y;

var lock_X = false;
var lock_Y = false;

var lock_t_init_x = false;
var lock_t_init_y = false;

var displacement_x = false;
var displacement_y = false;

var Si_x;
var Si_y;

var Sf_x;
var Sf_y;

var velX;
var velY;

var leftValue;
var bottomValue;

var velMaxActive = 2.08;//2.56;
var velMinActive = 1;//2.56;
var velMaxPassive = 106;
var velMinPassive = 24;

var f; 
var d; 

var frequency_low_speed;
var frequency_high_speed;
var duty_cycle_low_speed; 
var duty_cycle_high_speed;

var cursorVel

// /dev/ttyUSB0
// COM3

app.use(bodyParser.urlencoded({extended: true}));
app.set('view engine', 'ejs');

//#######################################################################

app.post("/on", function(req, res){
   id_on_off = Number(req.body.btn_on_id);
   id_on_off_1 = id_on_off.toString();
   
   var activeTouch = "6\n";
   console.log("activeTouch: ", activeTouch);
   arduino.write(activeTouch); 
});

//---------------------------------------------------

app.post("/off", function(req, res){
   id_on_off = Number(req.body.btn_off_id);
   id_on_off_1 = id_on_off.toString();

   var passiveTouch = "7\n";
   console.log("passiveTouch: ", passiveTouch);
   arduino.write(passiveTouch); 
});

//#######################################################################

app.post("/zero", function(req, res){
   var num0 = Number(req.body.id_zero);
   var idTactile0 = num0.toString();
   console.log("idTactile: ", idTactile0);
   
   if(lock_X == false && lock_Y == true){ 
      activeTouchMovement(velX, idTactile0);         
   }
      
   if(lock_X == true && lock_Y == false){ 
      activeTouchMovement(velY, idTactile0);      
   }
});

//---------------------------------------------------

app.post("/one", function(req, res){
   var num1 = Number(req.body.id_one);
   var idTactile1 = num1.toString();
   console.log("idTactile: ", idTactile1);

   if(lock_X == false && lock_Y == true){ 
      activeTouchMovement(velX, idTactile1);         
   }
      
   if(lock_X == true && lock_Y == false){ 
      activeTouchMovement(velY, idTactile1);      
   }            
});

//---------------------------------------------------

app.post("/two", function(req, res){
   var num2 = Number(req.body.id_two);
   var idTactile2 = num2.toString();
   console.log("idTactile: ", idTactile2);

   if(lock_X == false && lock_Y == true){
      activeTouchMovement(velX, idTactile2); 
   }

   if(lock_X == true && lock_Y == false){
      activeTouchMovement(velY, idTactile2);   
   }       
});

//---------------------------------------------------

app.post("/three", function(req, res){
   var num3 = Number(req.body.id_three);
   var idTactile3 = num3.toString();
   console.log("idTactile: ", idTactile3);

   if(lock_X == false && lock_Y == true){
      activeTouchMovement(velX, idTactile3);
   }
      
   if(lock_X == true && lock_Y == false){
      activeTouchMovement(velY, idTactile3);
   }              
});

//---------------------------------------------------

app.post("/four", function(req, res){
   var num4 = Number(req.body.id_four);
   var idTactile4 = num4.toString();
   console.log("idTactile: ", idTactile4);

   if(lock_X == false && lock_Y == true){
      activeTouchMovement(velX, idTactile4);
   }

   if(lock_X == true && lock_Y == false){
      activeTouchMovement(velY, idTactile4);   
   }        
});

//#######################################################################

function readFromDatabase(tactile_id){
   PaperTactileSensation.find({tactile_sensation_ID: tactile_id}, function(err, papertactilesensations){
      if (err) {
         console.log(err);
      }else{
         papertactilesensations.forEach(function(papertactilesensation){
            frequency_low_speed = papertactilesensation.frequency_low_speed;
            frequency_high_speed = papertactilesensation.frequency_high_speed;
            duty_cycle_low_speed = papertactilesensation.duty_cycle_low_speed;
            duty_cycle_high_speed = papertactilesensation.duty_cycle_high_speed;
         });
      }    
   });
}
//-------------------------------------------------------------------------
function frequency(vel, velMin, velMax, frequency_low_speed, frequency_high_speed){
   cursorVel = limitedVel(vel, velMin, velMax);
   var f_t = ((frequency_high_speed-frequency_low_speed)/(velMax-velMin))*(cursorVel-velMin)+frequency_low_speed;
   return f_t;
}
//-------------------------------------------------------------------------
function dutyCycle(vel, velMin, velMax, duty_cycle_low_speed, duty_cycle_high_speed){
   cursorVel = limitedVel(vel, velMin, velMax);
   var d_t = ((duty_cycle_high_speed-duty_cycle_low_speed)/(velMax-velMin))*(cursorVel-velMin)+duty_cycle_low_speed;
   return d_t;
}
//-------------------------------------------------------------------------
function limitedVel(vel, velMin, velMax){
   var auxLimitedVel;
   if(vel >= 0 && vel <= velMin){
      auxLimitedVel = velMin;
   }
   if(vel >= velMax){
      auxLimitedVel = velMax;
   }
   if(vel > velMin && vel < velMax){
      auxLimitedVel = vel;
   }
   return auxLimitedVel;
}

//#######################################################################

function sendTactileSensation(vel, velMin, velMax, idTactile){
   readFromDatabase(idTactile);
         
   f = Math.round(frequency(vel, velMin, velMax, frequency_low_speed, frequency_high_speed));
   d = Math.round(dutyCycle(vel, velMin, velMax, duty_cycle_low_speed, duty_cycle_high_speed));

   if (f != 0 && d !=0){
      var T = 1/f;
      var hp_value = T*(d/100);
      var lp_value = T-hp_value;

      var T_send = Math.round(T*1000)
      var hp_value_send = Math.round(hp_value*1000);
      var lp_value_send = Math.round(lp_value*1000);
   }else{
      var T = 0;
      var hp_value = 0;
      var lp_value = 0;
   
      var T_send = 0;
      var hp_value_send = hp_value;
      var lp_value_send = lp_value;
   }
 
   var hp = hp_value_send.toString() + "\n";
   var lp = lp_value_send.toString() + "\n";
   var T_ms = T_send.toString() + "\n";

   HighPulseLowPulseMsData.findByIdAndUpdate("66b427edbaa0ce5782e956d0", { hp_ms: hp_value_send }, function(err){
      if (err){
         console.log(err);
      }
   });

   HighPulseLowPulseMsData.findByIdAndUpdate("66b427edbaa0ce5782e956d0", { lp_ms: lp_value_send }, function(err){
      if (err){
         console.log(err);
      }
   });
   
   HighPulseLowPulseMsData.findByIdAndUpdate("66b427edbaa0ce5782e956d0", { t: T_send }, function(err){
      if (err){
         console.log(err);
      }
   });

   HighPulseLowPulseMsData.findByIdAndUpdate("66b427edbaa0ce5782e956d0", { d: d }, function(err){
      if (err){
         console.log(err);
      }
   });
/*
   console.log("f: ", f.toString());
   console.log("d: ", d.toString());
   console.log("T_ms: ", T_ms);
   console.log("hp: ", hp);
   console.log("lp: ", lp);
   console.log("cursorSpeed: ", Math.round(cursorVel) + "\n");
   */

   console.log("hp: ", hp_value_send);
   console.log("lp: ", lp_value_send);
   console.log("T_ms: ", T_send);
   console.log("d: ", d);

}

//#######################################################################

function activeTouchMovement(vel, idTactile){
   console.log("speedValue: ", vel);

   sendTactileSensation(vel, velMinActive, velMaxActive, idTactile);
}
//-------------------------------------------------------------------------
io.on('connection', (socket) => {
   socket.on('mouse_speed_track', function(speed_value, idTactile, x_passive, y_passive){
      if(oldMouseSpeedValue == 0 || speed_value == oldMouseSpeedValue){
         oldMouseSpeedValue = speed_value;
      }else if(speed_value != oldMouseSpeedValue){
         oldMouseSpeedValue = speed_value;
         //console.log("speedValue: ", speed_value);
         console.log("x: ", x_passive);
         console.log("y: ", y_passive);
         console.log("idTactile: ", idTactile);

         sendTactileSensation(speed_value, velMinPassive, velMaxPassive, idTactile);
      }
   });
     
   socket.on('disconnect', function(){
      //console.log('user disconnected');
   });
});       

//#######################################################################

function main(){

   app.use('/Tactile_Glove_Experiment_QoE', express.static(__dirname + '/Tactile_Glove_Experiment_QoE'));
   app.use('/dist', express.static(__dirname + '/dist'));
   app.get("/", function(req, res){
      res.render("indeex", {});
   });
   app.get("/views/indeex.ejs", function(req, res){
      res.render("indeex", {}); 
   });
   app.get("/views/camisabasica.ejs", function(req, res){
      res.render("camisabasica", {val_X: GyX, val_Y: GyY, val_ON_OFF: id_on_off_1, S_val_X: S_GyX, S_val_Y: S_GyY});  
   });
   app.get("/views/camisapolo.ejs", function(req, res){
      res.render("camisapolo", {val_X: GyX, val_Y: GyY, val_ON_OFF: id_on_off_1, S_val_X: S_GyX, S_val_Y: S_GyY});  
   });
   app.get("/views/casacoalgodao1.ejs", function(req, res){
      res.render("casacoalgodao1", {val_X: GyX, val_Y: GyY, val_ON_OFF: id_on_off_1, S_val_X: S_GyX, S_val_Y: S_GyY}); 
   });
   app.get("/views/casacoalgodao2.ejs", function(req, res){
      res.render("casacoalgodao2", {val_X: GyX, val_Y: GyY, val_ON_OFF: id_on_off_1, S_val_X: S_GyX, S_val_Y: S_GyY});  
   });
   app.get("/views/casacocroche1.ejs", function(req, res){
      res.render("casacocroche1", {val_X: GyX, val_Y: GyY, val_ON_OFF: id_on_off_1, S_val_X: S_GyX, S_val_Y: S_GyY});  
   });
   app.get("/views/casacocroche2.ejs", function(req, res){
      res.render("casacocroche2", {val_X: GyX, val_Y: GyY, val_ON_OFF: id_on_off_1, S_val_X: S_GyX, S_val_Y: S_GyY});  
   });
   app.get("/views/casacocroche3.ejs", function(req, res){
      res.render("casacocroche3", {val_X: GyX, val_Y: GyY, val_ON_OFF: id_on_off_1, S_val_X: S_GyX, S_val_Y: S_GyY});  
   });
   app.get("/views/casacocroche4.ejs", function(req, res){
      res.render("casacocroche4", {val_X: GyX, val_Y: GyY, val_ON_OFF: id_on_off_1, S_val_X: S_GyX, S_val_Y: S_GyY});  
   });
   app.get("/views/roupajeans.ejs", function(req, res){
      res.render("roupajeans", {val_X: GyX, val_Y: GyY, val_ON_OFF: id_on_off_1, S_val_X: S_GyX, S_val_Y: S_GyY});  
   });
   app.get("/views/salto.ejs", function(req, res){
      res.render("salto", {val_X: GyX, val_Y: GyY, val_ON_OFF: id_on_off_1, S_val_X: S_GyX, S_val_Y: S_GyY});  
   });
   app.get("/views/sandalia_amarela.ejs", function(req, res){
      res.render("sandalia_amarela", {val_X: GyX, val_Y: GyY, val_ON_OFF: id_on_off_1, S_val_X: S_GyX, S_val_Y: S_GyY});  
   });
   app.get("/views/sueter1.ejs", function(req, res){
      res.render("sueter1", {val_X: GyX, val_Y: GyY, val_ON_OFF: id_on_off_1, S_val_X: S_GyX, S_val_Y: S_GyY});  
   });
   app.get("/views/sueter2.ejs", function(req, res){
      res.render("sueter2", {val_X: GyX, val_Y: GyY, val_ON_OFF: id_on_off_1, S_val_X: S_GyX, S_val_Y: S_GyY});  
   });
   app.get("/views/sueter3.ejs", function(req, res){
      res.render("sueter3", {val_X: GyX, val_Y: GyY, val_ON_OFF: id_on_off_1, S_val_X: S_GyX, S_val_Y: S_GyY});  
   });
   app.get("/views/tenis.ejs", function(req, res){
      res.render("tenis", {val_X: GyX, val_Y: GyY, val_ON_OFF: id_on_off_1, S_val_X: S_GyX, S_val_Y: S_GyY});  
   });   
}

// set an interval to update 2 times per second:
setInterval(main, 500);

//#######################################################################

server.listen(3000, function(){   
  console.log("Server is running on port 3000");
});














