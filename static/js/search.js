/* references
    https://www.w3schools.com/jquery/ajax_get.asp
    https://stackoverflow.com/questions/15688313/how-can-i-populate-a-select-dropdown-list-from-a-json-feed-with-angularjs 
*/ 

function set_years(min,max){

      // set min and max year
      $('#minrange').attr('min',min)
      $('#minrange').attr('max',max)
      $('#minrange').val(min)
      $('#mintext').val(min)
      
      $('#maxrange').attr('min',min)
      $('#maxrange').attr('max',max)
      $('#maxrange').val(max)
      $('#maxtext').val(max)     

}


$(document).ready(function(){

    /************* INITIAL LOADING ************/
    
    // first get the makes to populate make list    
    $.get("/getcardata", function(data, status){  
      console.log(data)
      
      // populate make list
      $.each(data.makes, function(i,val){
          //console.log(val)
          $("#make").append($('<option></option>').val(val).html(val));
      })
      
      $("#model").append($('<option></option>').val('ALL').html('ALL'))
      $("#type").append($('<option></option>').val('ALL').html('ALL'))
      
     set_years(data.years[0], data.years[1])
      
    });


    // when they select a make, update the others
    $("#make").change(function(){
    
      val = $("#make").val()
    
      $.get("/getcardata", { make: val }, function(data, status){
        
        console.log(data.models)
        // populate make list
        
        // remove all the options
        $('#model').find('option').remove()
        $.each(data.models, function(i,val){
            //console.log(val)
            $("#model").append($('<option></option>').val(val).html(val));
        })
        
        $('#type').find('option').remove()
        $("#type").append($('<option></option>').val('ALL').html('ALL'))
              
        set_years(data.years[0], data.years[1])
        
      });
    });
    
    // when they change a model, update body-type list
    $("#model").change(function(){
    
      makeval = $("#make").val()
      val = $("#model").val()
    
      $.get("/getcardata", { make: makeval, model:val }, function(data, status){
        
        console.log(data.types)
        // populate make list
        
        // remove all the options
        $('#type').find('option').remove()
        
        $.each(data.types, function(i,val){
            //console.log(val)
            $("#type").append($('<option></option>').val(val).html(val));
        })
        
      });
    });    
    
    
    $('#minrange').change(function(){
        $('#mintext').val($(this).val())
    })
    
    $('#maxrange').change(function(){
        $('#maxtext').val($(this).val())
    })    
});
        