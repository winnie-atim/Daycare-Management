// Dependencies
const express = require('express');
const path =require("path");
const dotenv =  require('dotenv').config();
const passport = require("passport");
const LocalStrategy = require("passport-local").Strategy;
const bcrypt = require("bcrypt");
const session = require('express-session')
const signupModel = require ("./models/signupModel")

const connectDb = require('./config/dbConfig');
connectDb();


// Instantiations
const app = express();
const port = 5500;


app.engine("pug", require("pug").__express)
app.set("view engine","pug")
app.set("views", path.join(__dirname, "views/pug")); 
app.use(express.static(path.join(__dirname,"public")))

 app.use(express.urlencoded({extended:true}))


// importing models
const babyform = require('./models/babiesModel');
const sitterform = require('./models/sitterModel');
const Sign = require("./models/sitterModel");


// authentication

app.use(session({ secret: 'hello_world', resave: false, saveUninitialized: false }));
app.use(passport.initialize());
app.use(passport.session());

passport.use(signupModel.createStrategy())
        
    
  


passport.serializeUser(signupModel.serializeUser());
  
  passport.deserializeUser(signupModel.serializeUser());





  

// routes
const landingRoutes = require("./routes/landingRoutes");
// const loginRoutes = require("./routes/loginRoutes");
const signupRoutes = require("./routes/signupRoutes");
const babyRoutes = require("./routes/babiesRoutes");
const adminRoutes = require("./routes/adminRoutes");
const admindashRoutes = require("./routes/admindashRoutes");
const sitterformRoutes = require("./routes/sitterformRoutes");
const sittertableRoutes = require("./routes/sittertableRoutes");
const babytableRoutes = require("./routes/sittertableRoutes");


// importing routes
app.use("/api", landingRoutes);
// app.use("/api", loginRoutes);
app.use("/api", signupRoutes)
app.use("/api", babyRoutes);
app.use("/api", adminRoutes);
app.use("/api", admindashRoutes);
app.use("/api", sitterformRoutes);
app.use("/api", sittertableRoutes);
app.use("/api", babytableRoutes);


// Bootstrapping Server
// Always the last line in your code
app.listen(5500, () => console.log(`listening on ${port}`)); 