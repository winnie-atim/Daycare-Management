const express = require("express");
const router = express.Router();

function isAuthenticated(req, res, next) {
    if (req.isAuthenticated()) {
        return next();
    }
    res.render('admindashboard');
}

router.get('/admindash', isAuthenticated, (req, res) => {
    res.render('admindashboard');
});

module.exports = router;