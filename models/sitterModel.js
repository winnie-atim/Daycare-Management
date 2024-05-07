const mongoose = require("mongoose");

const sitterschema = new mongoose.Schema({
   sittername:{
    type:String
   },
   dob:{
    type:Date
   },
   gender:{
    type:String
   },
   location:{
    type:String
   },
   recommendername:{
    type:String
   },
   nin:{
    type:String
   },
   religion:{
    type:String
   },
   levelofeducation:{
    type:String
   },
   contacts:{
    type:Number
   },
   sitternumber:{
    type:Number
   },
   nextofkin:{
    type:String
   },
   
})

module.exports = mongoose.model("Sitter", sitterschema);
