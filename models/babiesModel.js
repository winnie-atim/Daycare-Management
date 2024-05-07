const mongoose = require("mongoose");

const babySchema = new mongoose.Schema({
    babyname:{
        type:String
    },
    gender:{
        type:String
    },
    age:{
        type:Number
    },
    location:{
        type:String
    },
    nameofguardian:{
        type:String
    },
    time:{
        type:String
    },
    babynumber:{
        type:Number
    },
    period:{
        type:String
    },
    fee:{
        type:Number
    }
})


module.exports = mongoose.model("Baby", babySchema);