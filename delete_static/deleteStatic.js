function deleteSinglePage() {
    // Get the [x] buttons that initialization assest deletion
    initialDeleteButtons = $(".remove-asset-button.action-button")
    for (var j=0; j < initialDeleteButtons.length; j++){
        console.log(j)
        // Click the jth [x]
        initialDeleteButtons[j].click()
        // Click to confirm deletion
        $(".action-primary:contains('Delete')").click()
    }
}

function deleteManyPages(pages){
    // This function deletes everything on a page, waits a while for page to load more assets, then deletes everything again.
    wait = 10*1000 // milliseconds
    for (var i=0;i<=pages;i++) {
       (function(ind) {
           setTimeout(function(){
               console.log("Page", ind);
               deleteSinglePage()
           }, 1000 + (wait * ind));
       })(i);
    }
}