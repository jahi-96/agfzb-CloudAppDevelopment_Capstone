/**
 * Get all dealerships
 */

 const Cloudant = require('@cloudant/cloudant');


 async function main(params) {
     const cloudant = Cloudant({
         url: params.COUCH_URL,
         plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
     });
 
    const db = cloudant.db.use('dealerships')
    try {
        const response = await db.list({ include_docs: true })
        // response.rows is an array with a 'doc' attribute for each document
        let dealerships = response.rows.map((r) => { return {
                id: r.doc.id,
                city: r.doc.city,
                state: r.doc.state,
                st: r.doc.st,
                address: r.doc.address,
                zip: r.doc.zip,
                lat: r.doc.lat,
                long: r.doc.long
                }
            })
        if(!params.state){
            return {dealerships}; 
        } else{
            dealerships = dealerships.filter( x => x.st == params.state);
            if (Array.isArray(dealerships) && dealerships.length) {
                // array exists and is not empty
                return {dealerships}
            } else{
                return {error: 'The state does not exist'};
            }
        }
        
     } catch (error) {
        return { error: error.description };
     }
 
 }
