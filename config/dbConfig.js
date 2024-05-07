const mongoose = require('mongoose');

const connectDb = async ()=>{
    try{
        const conn = await mongoose.connect(process.env.DATABASE)
        console.log(`MongoDB Connected at: ${conn.connection.host}`)
    }
    catch{
        console.log('MongoDB connection error: ${error}')
        process.exit(1)
    }

}

module.exports = connectDb;