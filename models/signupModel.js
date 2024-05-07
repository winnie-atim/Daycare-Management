const mongoose = require("mongoose");
const passportLocalMongoose = require("passport-local-mongoose")
const signSchema = new mongoose.Schema({
    username:{
        type:String
    },
    password:{
        type:String
    },
    
})

signSchema.plugin(passportLocalMongoose)
module.exports = mongoose.model("Sign", signSchema);