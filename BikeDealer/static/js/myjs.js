$(document).ready(function () {
    var NPR = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'NPR',
    });
    $("#datepicker").daterangepicker({
        autoUpdateInput: false,
        minDate:new Date(),
        
        locale: {
            cancelLabel: 'Clear',
            format: 'YYYY-MM-DD'
        }
    });
    var all_rented_dates = []
    if($('#total_rented').val() > 0){
        for(var i=1; i<=parseInt($('#total_rented').val()); i++){
            all_rented_dates.push.apply(all_rented_dates, getDatesInRange($('#rent_pickup_date_'+i).val(), $('#rent_dropoff_date_'+i).val() ))
        }
    }
    $("#rent_datepicker").daterangepicker({
        autoUpdateInput: false,
        minDate:new Date(),
        isInvalidDate: function(ele) {
            var currDate = moment(ele._d).format('YYYY-MM-DD');
            return all_rented_dates.indexOf(currDate) != -1;
        },
        locale: {
            cancelLabel: 'Clear',
            format: 'YYYY-MM-DD'
        }
    });
    $("#datepicker").on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('YYYY-MM-DD') + ' - ' + picker.endDate.format('YYYY-MM-DD'));
    });
    $("#rent_datepicker").on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('YYYY-MM-DD') + ' - ' + picker.endDate.format('YYYY-MM-DD'));
        var rent_price_per_day = $('#rent_price').val()
        var rent_days = picker.endDate.diff(picker.startDate, 'days')+1;
        var rent_total_price = rent_price_per_day * rent_days;
        
        
        $('#rent_price_cal').text(NPR.format(rent_total_price));
    });

   

    function getDatesInRange(startDate, EndDate){
        var date = new Date(new Date(startDate).getTime());
        var dates = [];
        while (date <= new Date(EndDate)) {
            var yourDate = new Date(date);
            const offset = yourDate.getTimezoneOffset()
            yourDate = new Date(yourDate.getTime() - (offset*60*1000))
            dates.push(yourDate.toISOString().split('T')[0]);
            date.setDate(date.getDate() + 1);
        }
        return dates; 
        
    }
    
$('.btn-number').click(function(e){
    e.preventDefault();
    
    fieldName = $(this).attr('data-field');
    type      = $(this).attr('data-type');
    var input = $("input[name='"+fieldName+"']");
    var currentVal = parseInt(input.val());
    if (!isNaN(currentVal)) {
        if(type == 'minus') {
            
            if(currentVal > input.attr('min')) {
                input.val(currentVal - 1).change();
            } 
            if(parseInt(input.val()) == input.attr('min')) {
                $(this).attr('disabled', true);
            }

        } else if(type == 'plus') {

            if(currentVal < input.attr('max')) {
                input.val(currentVal + 1).change();
            }
            if(parseInt(input.val()) == input.attr('max')) {
                $(this).attr('disabled', true);
            }

        }
    } else {
        input.val(0);
    }
});
$('.input-number').focusin(function(){
   $(this).data('oldValue', $(this).val());
});
$('.input-number').change(function() {
    
    minValue =  parseInt($(this).attr('min'));
    maxValue =  parseInt($(this).attr('max'));
    valueCurrent = parseInt($(this).val());
    var pricePerPiece = parseInt($('#pricePerPiece').val());
    var total_price = valueCurrent * pricePerPiece;
    $('#parts_order_price_cal').text(NPR.format(total_price));
    name = $(this).attr('name');
    if(valueCurrent >= minValue) {
        $(".btn-number[data-type='minus'][data-field='"+name+"']").removeAttr('disabled')
    } else {
        alert('Sorry, the minimum value was reached');
        $(this).val($(this).data('oldValue'));
    }
    if(valueCurrent <= maxValue) {
        $(".btn-number[data-type='plus'][data-field='"+name+"']").removeAttr('disabled')
    } else {
        alert('Sorry, the maximum value was reached');
        $(this).val($(this).data('oldValue'));
    }
});

$(".input-number").keydown(function (e) {
    // Allow: backspace, delete, tab, escape, enter and .
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 190]) !== -1 ||
         // Allow: Ctrl+A
        (e.keyCode == 65 && e.ctrlKey === true) || 
         // Allow: home, end, left, right
        (e.keyCode >= 35 && e.keyCode <= 39)) {
             // let it happen, don't do anything
             return;
    }
    // Ensure that it is a number and stop the keypress
    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
        e.preventDefault();
    }
});

})
