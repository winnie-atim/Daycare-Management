const express = require("express");
const router = express.Router();
const Sitter = require("../models/sitterModel");

router.get("/sittertable", async (req, res) => {
    try {
        let items = await Sitter.find();
        res.render("sittertable.pug", { sitters: items });
    } catch (error) {
        console.log(error);
        return res.status(400).send({ message: "Sorry, could not get sittertable" });
    }
});

router.get("/babytable", (req, res) => {
    res.render("babytable");
});

module.exports = router;
