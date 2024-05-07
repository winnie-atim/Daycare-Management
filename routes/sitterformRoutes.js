const express = require("express");
const router = express.Router();
const Sitter = require('../models/sitterModel');



router.get("/sitterform", (req,res) =>{
    res.render("sitterform.pug")
})


router.get("/sittertable", async (req, res) => {
    try {
        const sitters = await Sitter.find();

        res.render("sittertable", { sitters });
    } catch (error) {
        console.log(error);
        res.status(500).send("Internal Server Error");
    }
});




router.post('/regsitter',async(req,res) =>{
    try{
        const sitter = new Sitter(req.body);
        await sitter.save();
        console.log(req.body);
        res.redirect("/api/sittertable");
    }
    catch(error) {
        console.log(error);
        return res.status(400).send({message: "sorry could not find sitterform"})
    }
})



module.exports = router;