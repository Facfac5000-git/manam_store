$.noConflict();

jQuery(document).ready(function($) {

	"use strict";

	[].slice.call( document.querySelectorAll( 'select.cs-select' ) ).forEach( function(el) {
		new SelectFx(el);
	});

	jQuery('.selectpicker').selectpicker;
    let alert_stock_products = getAlertStockProducts();
    let stock_alert_notifications = $('#stock_alert_notifications')[0];
    let stock_alert_p = document.createElement('p');
    let stock_alert_count = $('#stock_alert_count');
    if(alert_stock_products.error == 0){
        stock_alert_count.html(alert_stock_products.count);
        let message = document.createTextNode('Hay productos en alerta de stock:');
        stock_alert_p.appendChild(message);
        stock_alert_notifications.appendChild(stock_alert_p);
        for(var index in alert_stock_products.products){
            let a = document.createElement('a');
            a.classList.add('dropdown-item');
            a.classList.add('media');
            a.href = '#';
            let i = document.createElement('i');
            i.classList.add('fa');
            i.classList.add('fa-warning');
            a.appendChild(i);
            let p = document.createElement('p');
            let text = document.createTextNode('Quedan '+alert_stock_products.products[index].stock+' unidades de '+alert_stock_products.products[index].name);
            p.appendChild(text);
            a.appendChild(p);
            stock_alert_notifications.appendChild(a);
        }
    }else{
        let message = document.createTextNode('No hay ningún producto en alerta de stock.')
        stock_alert_count.addClass('d-none');
        stock_alert_p.appendChild(message);
        stock_alert_notifications.appendChild(stock_alert_p);
    }

    let alert_expire_products = getAlertExpireProducts();
    let expire_alert_notifications = $('#expire_alert_notifications')[0];
    let expire_alert_p = document.createElement('p');
    let expire_alert_count = $('#expire_alert_count');
    if(alert_expire_products.error == 0){
        expire_alert_count.html(alert_expire_products.count);
        let message = document.createTextNode('Hay productos en alerta de vencimiento:');
        expire_alert_p.appendChild(message);
        expire_alert_notifications.appendChild(expire_alert_p);
        for(var index in alert_expire_products.products){
            let a = document.createElement('a');
            a.classList.add('dropdown-item');
            a.classList.add('media');
            a.href = '#';
            let i = document.createElement('i');
            i.classList.add('fa');
            i.classList.add('fa-warning');
            a.appendChild(i);
            let p = document.createElement('p');
            let text = document.createTextNode('El producto '+alert_expire_products.products[index].name+' vence el '+alert_expire_products.products[index].expire_date);
            p.appendChild(text);
            a.appendChild(p);
            expire_alert_notifications.appendChild(a);
        }
    }else{
        let message = document.createTextNode('No hay ningún producto en alerta de vencimiento.')
        expire_alert_count.addClass('d-none');
        expire_alert_p.appendChild(message);
        expire_alert_notifications.appendChild(expire_alert_p);
    }

    $(document).keypress(
      function(event){
        if (event.which == '13') {
          event.preventDefault();
        }
    });

	$('.search-trigger').on('click', function(event) {
		event.preventDefault();
		event.stopPropagation();
		$('.search-trigger').parent('.header-left').addClass('open');
	});

	$('.search-close').on('click', function(event) {
		event.preventDefault();
		event.stopPropagation();
		$('.search-trigger').parent('.header-left').removeClass('open');
	});

	$('.equal-height').matchHeight({
		property: 'max-height'
	});

	// var chartsheight = $('.flotRealtime2').height();
	// $('.traffic-chart').css('height', chartsheight-122);


	// Counter Number
	$('.count').each(function () {
		$(this).prop('Counter',0).animate({
			Counter: $(this).text()
		}, {
			duration: 3000,
			easing: 'swing',
			step: function (now) {
				$(this).text(Math.ceil(now));
			}
		});
	});

	 
	// Menu Trigger
	$('#menuToggle').on('click', function(event) {
		var windowWidth = $(window).width();   		 
		if (windowWidth<1010) { 
			$('body').removeClass('open'); 
			if (windowWidth<760){ 
				$('#left-panel').slideToggle(); 
			} else {
				$('#left-panel').toggleClass('open-menu');  
			} 
		} else {
			$('body').toggleClass('open');
			$('#left-panel').removeClass('open-menu');  
		} 
			 
	}); 

	 
	$(".menu-item-has-children.dropdown").each(function() {
		$(this).on('click', function() {
			var $temp_text = $(this).children('.dropdown-toggle').html();
			$(this).children('.sub-menu').prepend('<li class="subtitle">' + $temp_text + '</li>'); 
		});
	});


	// Load Resize 
	$(window).on("load resize", function(event) { 
		var windowWidth = $(window).width();  		 
		if (windowWidth<1010) {
			$('body').addClass('small-device'); 
		} else {
			$('body').removeClass('small-device');  
		} 
		
	});

    $(document).on('keyup', '.add_new_product', function(e){
        let n = e.currentTarget.name.split('_')[1]
        let $div = $('#product-row-'+n);
        let remove_add = $('#barcode_'+n);
        if(remove_add.val().length >= 8){
            let data = getProductbyBarcode(remove_add.val());
            if (data.error == 0){
                let $clone = $div.clone();
                remove_add.removeClass('add_new_product');
                $('#product-row-'+n+' #product_'+(n)).val(data.product);
                $('#product-row-'+n+' #price_'+(n)).val(data.price);
                $('#product-row-'+n+' #unit_price_'+(n)).val(data.price);
                $('#product-row-'+n+' #list_price_'+(n)).val(data.list_price);
                $('#product-row-'+n+' #quantity_'+(n)).attr('max',data.stock);
                n = parseInt(n)+1;
                $clone.attr('id', 'product-row-'+n);
                $clone.appendTo($div.parent());
                createNewRow(n)
                sumUpPrice(n);
            }
        };
    });

    $(document).on('change', '.quantity-control', function(e){
        let n = e.currentTarget.name.split('_')[1]
        quantity = $('#product-row-'+n+' #quantity_'+(n)).val();
        price = $('#product-row-'+n+' #unit_price_'+(n)).val();
        $('#product-row-'+n+' #price_'+(n)).val(price*quantity);
        n = $('.add_new_product')[0].name.split('_')[1];
        sumUpPrice(n);
    })

    $(document).on('keyup', '.quantity-control', function(e){
        let max_value = e.currentTarget.max;
        let value = e.currentTarget.value;
        if(parseInt(value) > parseInt(max_value)){
            e.currentTarget.value = max_value;
        }

    })

    $(document).on('change', '.product-control', function(e){
        let product_id = e.currentTarget.value;
        let data = getProductbyId(product_id);
        let n = e.currentTarget.name.split('_')[1]
        $('#product-row-'+n+' #price_'+(n)).val(data.price);
        $('#product-row-'+n+' #unit_price_'+(n)).val(data.price);
        $('#product-row-'+n+' #list_price_'+(n)).val(data.list_price);
        $('#product-row-'+n+' #quantity_'+(n)).val(1);
        $('#product-row-'+n+' #quantity_'+(n)).attr('max',data.stock);
        let m = $('.add_new_product')[0].name.split('_')[1];
        sumUpPrice(m);
    })

    $(document).on('change', '#by_trust', function(e){
        if(e.currentTarget.checked){
            $('#to_trust').removeAttr('disabled')
            $('#to_trust').attr('required','true')
        }else{
            $('#to_trust').val('')
            $('#to_trust').attr('disabled','true')
            $('#to_trust').removeAttr('required')
        }
    })

    $(document).on('click', '#add_new_product', function(e){
        let n = $('.add_new_product')[0].name.split('_')[1];
        let $div = $('#product-row-'+n);
        let remove_add = $('#barcode_'+n);
        let $clone = $div.clone();
        remove_add.removeClass('add_new_product');
        n = parseInt(n)+1;
        $clone.attr('id', 'product-row-'+n);
        $clone.appendTo($div.parent());
        createNewRow(n);
    })

    $(document).on('change', '.make_total', function(e){
        let list_price = $('#list_price').val();
        let profit_porc = $('#profit_porc').val();
        let rounding = $('#rounding').val();
        if(list_price == ''){list_price = 0};
        if(profit_porc == ''){profit_porc = 0};
        if(rounding == ''){rounding = 0};
        $('#price').val(parseFloat(list_price)+(parseFloat(list_price)*parseFloat(profit_porc)/100)+parseFloat(rounding));
    })

/*    $(document).on('keyup', '.cash_total_control', function(e){
        let last_total = parseFloat($('#last_total').val());
        let amount = parseFloat(e.currentTarget.value);
        console.log(last_total);
        console.log(amount);
        let cash_total = last_total + amount;
        console.log(cash_total);
        $('#cash_total').val(cash_total);
    })*/

    $('#table').DataTable();

});


function getProductbyBarcode(barcode){
        let data_response;
        jQuery.ajax({
            data: {barcode:barcode},
            url: '/store/ajax/get_product_by_barcode/',
            dataType: 'json',
            async: false,
            // on success
            success: function(response) {
                if (response.error == 0) {
                    data_response = response
                } else {
                    if(barcode.length == 13){
                        alert(response.message)
                    }
                }
            },
            // on error
            error: function(error) {
                alert('Error en Ajax')
            }
        });
        return data_response;
}

function getProductbyId(product_id){
        let data_response;
        jQuery.ajax({
            data: {product_id:product_id},
            url: '/store/ajax/get_product_by_id/',
            dataType: 'json',
            async: false,
            // on success
            success: function(response) {
                if (response.error == 0) {
                    data_response = response
                } else {
                    alert(response.message)
                }
            },
            // on error
            error: function(error) {
                alert('Error en Ajax')
            }
        });
        return data_response;
}

function getOrderData(order_id){
        let data_response;
        jQuery.ajax({
            data: {order_id:order_id},
            url: '/store/ajax/get_order_data/',
            dataType: 'json',
            async: false,
            // on success
            success: function(response) {
                if (response.error == 0) {
                    data_response = response
                } else {
                    alert(response.message)
                }
            },
            // on error
            error: function(error) {
                alert('Error en Ajax')
            }
        });
        return data_response;
}

function getAlertStockProducts(){
        let data_response;
        jQuery.ajax({
            data: {},
            url: '/store/ajax/get_alert_stock_products/',
            dataType: 'json',
            async: false,
            // on success
            success: function(response) {
                data_response = response;
            },
            // on error
            error: function(error) {
                alert('Error en Ajax')
            }
        });
        return data_response;
}

function getAlertExpireProducts(){
        let data_response;
        jQuery.ajax({
            data: {},
            url: '/store/ajax/get_alert_expire_products/',
            dataType: 'json',
            async: false,
            // on success
            success: function(response) {
                data_response = response;
            },
            // on error
            error: function(error) {
                alert('Error en Ajax')
            }
        });
        return data_response;
}

function createNewRow(n){
        let barcode = jQuery('#product-row-'+n+' #barcode_'+(n-1));
        barcode.attr('id','barcode_'+n);
        barcode.attr('name','barcode_'+n);
        barcode.val('');
        let product = jQuery('#product-row-'+n+' #product_'+(n-1));
        product.attr('id','product_'+n);
        product.attr('name','product_'+n);
        product.val(0);
        let quantity = jQuery('#product-row-'+n+' #quantity_'+(n-1));
        quantity.attr('id','quantity_'+n);
        quantity.attr('name','quantity_'+n);
        quantity.val(1);
        quantity.removeAttr('max');
        let price = jQuery('#product-row-'+n+' #price_'+(n-1));
        price.attr('id','price_'+n);
        price.attr('name','price_'+n);
        price.val(0);
        let unit_price = jQuery('#product-row-'+n+' #unit_price_'+(n-1));
        unit_price.attr('id','unit_price_'+n);
        unit_price.attr('name','unit_price_'+n);
        unit_price.val(0);
        let list_price = jQuery('#product-row-'+n+' #list_price_'+(n-1));
        list_price.attr('id','list_price_'+n);
        list_price.attr('name','list_price_'+n);
        list_price.val(0);
        barcode.focus();
}

function sumUpPrice(n){
    let total = 0;
    let list_total = 0;
    for(i=0;i<=n;i++){
        price = jQuery('#product-row-'+i+' #unit_price_'+(i)).val();
        list_price = jQuery('#product-row-'+i+' #list_price_'+(i)).val();
        quantity = jQuery('#product-row-'+i+' #quantity_'+(i)).val();
        total = total + (price*quantity);
        list_total = list_total + (list_price*quantity);
    }
    jQuery('#total').val(total);
    jQuery('#list_total').val(list_total);
}

function closeModal(){
    jQuery("#modal").removeClass('d-block');
    jQuery("#modal").addClass('d-none');
}

function showOrder(order_id){
    order_data = getOrderData(order_id);
    jQuery('#modal_id').html(order_data.id);
    jQuery('#modal_date').html(order_data.date);
    jQuery('#user').html(order_data.user);
    if(order_data.by_card){jQuery('#modal_by_card').html('Si')}else{jQuery('#modal_by_card').html('No')}
    if(order_data.by_trust){jQuery('#modal_by_trust').html('Si')}else{jQuery('#modal_by_trust').html('No')}
    if(order_data.to_trust){jQuery('#modal_to_trust').html(order_data.to_trust)}else{jQuery('#modal_to_trust').html('---')}
    jQuery('#modal_total').html(order_data.total);
    jQuery('#modal_list_total').html(order_data.list_total);
    jQuery('.modal-products')[0].innerHTML = '';
    jQuery('.modal-products')[0].appendChild(document.createTextNode('Productos:'));
    for (var product in order_data.products){
        var div = document.createElement('div');
        var p = document.createElement('p');
        var text = document.createTextNode(order_data.products[product].product+' x'+order_data.products[product].quantity+'.......$'+order_data.products[product].value);
        p.appendChild(text);
        div.appendChild(p);
        jQuery('.modal-products')[0].appendChild(div);
    }
    jQuery("#modal").removeClass('d-none');
    jQuery("#modal").addClass('d-block');
}

