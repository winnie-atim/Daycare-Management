const express = require("express");
const router = express.Router();
const passport = require('passport');

// GET route handler for rendering the login form
router.get("/adminlogin", (req, res) => {
    res.render("adminlogin");
});

// POST route handler for handling form submissions
router.post('/adminlogin', passport.authenticate('local', { 
    successRedirect: '/admindashboard', 
    failureRedirect: '/adminlogin' 
}));

module.exports = router;
