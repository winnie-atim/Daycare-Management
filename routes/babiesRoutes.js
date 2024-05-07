const express = require("express");
const router = express.Router();
const Baby = require("../models/babiesModel");



router.get("/babyform", (req,res) =>{
    res.render("babiesform")
})


router.get("/babytable", async (req, res) => {
    try {
        const babies = await Baby.find();

        res.render("babytable", { babies });
    } catch (error) {
        console.log(error);
        res.status(500).send("Internal Server Error");
    }
});

router.post('/babyregister', async (req, res) => {
    try {
        console.log(req.body); 
        const register = new Baby(req.body);
        await register.save();
        res.redirect('/api/babytable')
    } catch (error) {
        console.log(error);
        return res.status(400).send({ message: "Sorry, could not register baby" });
    }
});


router.post('/babytable/delete', async(req,res)=>{
    try{
        await Baby.deleteOne({_id:req.body.id})
        res.redirect('/api/babytable')
    }
    catch(error){
        res.status(400).send({message: "unable to delete "})
    }
})

router.post('/search', async (req, res) => {
    try {
        const searchTerm = req.body.search.toLowerCase();
        const babies = await Baby.find({
            $or: [
                { babyname: { $regex: searchTerm, $options: 'i' } },
                { gender: { $regex: searchTerm, $options: 'i' } },
                { age: { $regex: searchTerm, $options: 'i' } },
                { location: { $regex: searchTerm, $options: 'i' } },
                { nameofguardian: { $regex: searchTerm, $options: 'i' } },
                { time: { $regex: searchTerm, $options: 'i' } },
                { babynumber: { $regex: searchTerm, $options: 'i' } },
                { period: { $regex: searchTerm, $options: 'i' } },
                { fee: { $regex: searchTerm, $options: 'i' } }
            ]
        });

        res.render('babytable', { babies });
    } catch (error) {
        console.log(error);
        return res.status(400).send({ message: "Could not perform search" });
    }
})


module.exports = router;