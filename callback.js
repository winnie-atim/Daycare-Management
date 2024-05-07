let order = (call_production) =>{

    console.log("Order placed. Please call production")
    
    // function 👇 is being called 
      call_production();
    };
    
    let production = () =>{
    
    console.log("Production has started")
    
    };
    // name 👇 of our second function
order(production);