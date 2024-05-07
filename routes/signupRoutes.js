const express = require("express");
const router = express.Router();
const Sign = require('../models/signupModel')
const bcrypt = require('bcrypt');
const signupModel = require("../models/signupModel");

router.get('/signup', (req,res)=>{
    res.render("signup")
})

router.post("/signup", async(req,res)=>{
    try{
        const user = new signupModel(req.body)
        await signupModel.register(user,req.body.password)

    } catch(error){
        console.log(error)
    }
})

module.exports = router;